
import re
import os
import logging
from string import Template
from datetime import datetime

logger = logging.getLogger(__name__)
class ReplaceWildcard():
    """
        Module to handle wildcard to actual parameter conversion.
        At this point it has below reserved wildcard variables. User can add additional environmental variables in the config.
        ${YYYY}: 4 character year(${YYYY}) wildcard would be replaced by actual year based on input date.
        ${MM}: 2 character month(${MM}) wildcard would be replaced by actual month.
        ${DD}: 2 character day (${DD}) wildcard would be replaced by actual day of the month.
        ${HH}: 2 character hour(${HH}) wildcard would be replaced by actual hour of the day.
        ${MI}: 2 character minute(${MI}) wildcard would be replaced by actual minute of the hour.
        ${SS}: 2 character second(${SS}) wildcard would be replaced by actual second of the minute.
    """
    def __init__(self, date: datetime=datetime.now()):
        """
        :param wildcard_string: Wildcard string.
        :param date: datetime.datetime Input date to replace wildcard with actual date values 
        """
        self._date = date
        os.environ["YYYY"], os.environ["MM"], os.environ["DD"], os.environ["HH"], os.environ["MI"], os.environ["SS"] = str(self._date.year), str(self._date.month), str(self._date.day), str(self._date.hour), str(self._date.minute), str(self._date.second)

    def replace_wildcard(self, wildcard_string):
        self.wildcard_string_template = Template(wildcard_string)
        return self.wildcard_string_template.substitute(os.environ)