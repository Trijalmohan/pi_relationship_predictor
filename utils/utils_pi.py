import mmap
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PI_FILE = DATA_DIR / "external" / "pi_1billion.txt"
BIN_PI_FILE = DATA_DIR / "processed" / "pi_digits.bin"


def ensure_digits_bin():
    """Create binary π digit file if missing (digits only)."""
    if BIN_PI_FILE.exists():
        return

    if not RAW_PI_FILE.exists():
        raise FileNotFoundError(
            f"Missing raw π file:\n{RAW_PI_FILE}\n"
            "Download pi_1billion.txt and place in /data/external/"
        )

    print("[INFO] Building digits-only π file →", BIN_PI_FILE)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(RAW_PI_FILE, "r", encoding="utf-8") as fin, \
         open(BIN_PI_FILE, "wb") as fout:
        for line in fin:
            for ch in line:
                if ch.isdigit():
                    fout.write(ord(ch).to_bytes(1, "little"))


def search_in_pi(digits: str) -> int | None:
    """Return 0-based index of digits in π, or None."""
    ensure_digits_bin()
    needle = digits.encode("ascii")

    with open(BIN_PI_FILE, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        pos = mm.find(needle)
        mm.close()
        return None if pos == -1 else pos


def load_context(pos: int, dob_len: int) -> str:
    """Return snippet like: 12345[1122007]88888"""
    with open(BIN_PI_FILE, "rb") as f:
        start = max(0, pos - 5)
        f.seek(start)
        raw = f.read(5 + dob_len + 10)
        snippet = raw.decode("ascii", errors="ignore")

        left = snippet[:5]
        mid = snippet[5:5 + dob_len]
        right = snippet[5 + dob_len:]
        return f"{left}[{mid}]{right}"
