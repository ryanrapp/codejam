import dateutil.parser
from dateutil import tz
import datetime

class CJDateUtil(object):
  _INPUT_TIMEZONE = tz.gettz('UTC')
  # Normally feed "timezone" should be inferred from the data,
  # but will simply assume ET as primary timezone for this data
  _TIMEZONE_ASSUMPTION = tz.gettz('America/New_York')
  _EARLIEST_DATETIME = datetime.datetime(2014,7,3, tzinfo=_INPUT_TIMEZONE)

  def to_datetime(self, date_str):
    date_utc = dateutil.parser.parse(date_str)
    return date_utc.replace(tzinfo=self._INPUT_TIMEZONE)

  def to_et(self, date_utc):
    date_utc.replace(tzinfo=self._INPUT_TIMEZONE)
    return date_utc.astimezone(self._TIMEZONE_ASSUMPTION)

  def to_elapsed_seconds(self, date_utc):
    return (date_utc - self._EARLIEST_DATETIME).total_seconds()

  def to_daily_seconds(self, dt):
    return dt.hour * 60 * 60 + dt.minute * 60 + dt.second

  def to_daily_minutes(self, dt):
    return dt.hour * 60 + dt.minute

  def from_seconds_to_datetime(self, seconds):
    date_utc = self._EARLIEST_DATETIME + datetime.timedelta(seconds=seconds)
    date_utc.replace(tzinfo=self._INPUT_TIMEZONE)
    return date_utc
