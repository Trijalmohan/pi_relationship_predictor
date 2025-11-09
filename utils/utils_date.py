from datetime import datetime, timedelta

def parse_dob(dob_str: str) -> datetime:
    return datetime.strptime(dob_str, "%d%m%Y")

def fmt_date(dt: datetime) -> str:
    return dt.strftime("%d %B %Y")

def add_years(dt: datetime, years: int) -> datetime:
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        return dt.replace(month=2, day=28, year=dt.year + years)

def age_on(dob: datetime, ref: datetime | None = None) -> int:
    if ref is None:
        ref = datetime.today()
    age = ref.year - dob.year
    if (ref.month, ref.day) < (dob.month, dob.day):
        age -= 1
    return age
