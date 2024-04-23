import datetime


def get_period(end_date=datetime.date.today(), days=365):
    """
    return start and end dates
    """
    start_date = end_date - datetime.timedelta(days=days)
    return start_date, end_date
