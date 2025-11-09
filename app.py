from flask import Flask, render_template, request, jsonify
from utils.utils_pi import search_in_pi, load_context, ensure_digits_bin
from utils.utils_date import fmt_date, add_years, age_on, parse_dob
from pathlib import Path

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    choice = data.get("choice")
    dob_str = data.get("dob")
    print("DEBUG >> Received:", data) 
    try:
        my_dob = parse_dob(dob_str)
        my_age = age_on(my_dob)
        my_digits = dob_str  # The exact digit pattern we search in π

        results = {}

        # Handle partner
        if choice in ("partner", "both"):
            partner_dob = add_years(my_dob, 3)
            pos = search_in_pi(dob_str)
            snippet = load_context(pos, len(dob_str)) if pos is not None else b""

            results["partner"] = {
                "age": age_on(partner_dob),
                "dob": fmt_date(partner_dob),
                "pos": pos,
                "context": snippet.decode("ascii", errors="ignore"),
            }

        # Handle close friend
        if choice in ("friend", "both"):
            friend_dob = add_years(my_dob, 1)
            pos = search_in_pi(dob_str)
            snippet = load_context(pos, len(dob_str)) if pos is not None else b""

            results["friend"] = {
                "age": age_on(friend_dob),
                "dob": fmt_date(friend_dob),
                "pos": pos,
                "context": snippet.decode("ascii", errors="ignore"),
            }

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    ensure_digits_bin()
    app.run(debug=True)
