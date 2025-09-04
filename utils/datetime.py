from datetime import datetime

def get_date() -> str:
    """return the date in dd_mm_yyyy format

    Returns:
        str: the returned date
    """
    return datetime.now().strftime("%d_%m_%Y")