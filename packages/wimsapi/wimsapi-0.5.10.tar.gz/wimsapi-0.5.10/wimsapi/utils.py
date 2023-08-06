import datetime



def one_year_later():
    """Give the date one year later from now in the format yyyymmdd."""
    d = datetime.date.today()
    return d.replace(year=d.year + 1).strftime("%Y%m%d")



def default(d, k, i, default=None):
    """Returns d[k][i], defaults to default if KeyError or IndexError is raised."""
    try:
        return d[k][i]
    except (KeyError, IndexError):
        return default
