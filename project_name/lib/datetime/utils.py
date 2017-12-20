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
        #TODO: Later, this function should receive the client timezone and based on that, determine the format
        return datetime.datetime.strptime(self._date, format_str)