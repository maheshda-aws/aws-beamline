"""
        Module to handle wildcard to actual date conversion.
        At this pount it only handles below wild cards.
        {YYYY}: 4 character year({YYYY}) wildcard would be replaced by actual year based on input date.
        {MM}: 2 character month({MM}) wildcard would be replaced by actual month.
        {DD}: 2 character day ({DD}) wildcard would be replaced by actual day of the month.
        {HH}: 2 character hour({HH}) wildcard would be replaced by actual hour of the day.
        {MI}: 2 character minute({MI}) wildcard would be replaced by actual minute of the hour.
        {SS}: 2 character second({SS}) wildcard would be replaced by actual second of the minute.
"""
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DateWildcard():
    """
     Date wildcard replacement
    """

    def __init__(self, wildcard_string, date=datetime.now()):
        """
        :param wildcard_string: Wildcard string.
        :param botocore_max_retries: datetime.datetime Input date to replace wildcard with actual date values 
        """
        self.wildcard_string = wildcard_string
        self._date = date
        self._yyyy, self._mm, self._dd, self._hh, self._mi, self._ss = self._date.year, self._date.month, self._date.day, self._date.hour, self._date.minute, self._date.second

    @property
    def year(self):
        return str(self._yyyy)

    @property
    def month(self):
        return str(self._mm).zfill(2) # Zero padding

    @property
    def day(self):
        return str(self._dd).zfill(2)

    @property
    def hour(self):
        return str(self._hh).zfill(2)

    @property
    def minute(self):
        return str(self._mi).zfill(2)

    @property
    def second(self):
        return str(self._ss).zfill(2)

    @property
    def date_parts(self):
        return {"YYYY": self.year, "MM": self.month, "DD": self.day, "HH": self.hour, "MI": self.minute, "SS": self.second}

    @property
    def replace_date_wildcard(self):
        for key, value in self.date_parts.items():
            self.wildcard_string=re.sub("{{{0}}}".format(key), str(value), self.wildcard_string)
        return self.wildcard_string