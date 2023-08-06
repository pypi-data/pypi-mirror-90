from datetime import datetime
import dateutil.parser

class StaticUtils(object):
    @staticmethod
    def ParseDate(x):
        if x is None:
            return None
        return dateutil.parser.parse(x)