from datetime import datetime

from click import DateTime


def get_year_range(from_: str | None, to: str | None):
    """
    Get the year range from the given date strings.
    """
    current_year: int = datetime.now().year

    to_date: datetime = (
        datetime.strptime(to, "%Y%m%d") if to else datetime(current_year, 1, 1)
    )
    from_date: datetime = (
        datetime.strptime(from_, "%Y%m%d") if from_ else datetime.now()
    )

    return to_date, from_date
