import datetime


class ConvertedDateTime:
    """
    DateTime object parser
    """

    def __init__(self, date_str):
        self._date = date_str

    def convert_date(self, format_str):
        """
        Given a  format, returns a datetime object
        """
        return datetime.datetime.strptime(self._date, format_str)
