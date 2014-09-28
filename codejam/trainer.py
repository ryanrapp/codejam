import datetime
from matplotlib import pyplot as plt
import dateutil.parser
from dateutil import tz
import json
import numpy as np
import matplotlib.mlab as mlab
import pdb
import pprint

class Trainer(object):
  _INPUT_TIMEZONE = tz.gettz('UTC')
  _TRAINING_FILE = 'data/training_data.txt'
  _WORKING_FILE = 'data/workfile.json'
  # Normally feed "timezone" should be inferred from the data,
  # but will assume ET as primary timezone for this data
  _TIMEZONE_ASSUMPTION = tz.gettz('America/New_York')
  _EARLIEST_DATETIME = datetime.datetime(2014,7,3, tzinfo=_INPUT_TIMEZONE)
  _FEED_WHITELIST = ['22425']
  _NUM_FEEDS = 10

  def read_data(self):
    print "reading data"
    file = open(self._TRAINING_FILE, 'r')
    return file

  def prepare_data(self, file):
    processed = 0
    for line in file:
      data = line.split()
      feed_id = data[0]

      if processed < self._NUM_FEEDS:
        feed_data = []
        day_of_week = []
        processed += 1
        x = []

        for date_str in data[1:]:
          date_utc = dateutil.parser.parse(date_str)
          date_utc.replace(tzinfo=self._INPUT_TIMEZONE)
          date_et = date_utc.astimezone(self._TIMEZONE_ASSUMPTION)
          seconds = (date_utc - self._EARLIEST_DATETIME).seconds
          daily_seconds = date_et.hour * 60 * 60 + date_et.minute * 60 + date_et.second
          daily_minutes = date_et.hour * 60 + date_et.minute
          is_business_day = date_et.weekday() < 5
          datapoint = (seconds,date_et.weekday(), date_et.hour, )
          feed_data.append(datapoint)
          x.append(date_et.weekday())

          day_of_week.append(date_et.hour)

        sorted_feed_data = sorted(feed_data, key=lambda datapoint: datapoint[0])

        #print np.amax(sorted_feed_data, 0)

        # crawl_result = []
        # last_ten = []
        # for datapoint in sorted_feed_data:
        #   seconds = datapoint[0]
        #   last_ten.append(seconds)
        #   if len(last_ten) > 10:
        #     last_ten.pop(0)
        #
        #   crawl_result = last_ten
        #
        #

        #pprint.pprint(sorted_feed_data)
        #pprint.pprint(np.histogram(day_of_week, bins=range(0,25))[0])

        #n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

        #plt.show()



        yield {'feed_id': feed_id, 'data': sorted_feed_data}

      else:
        pass

  def write_data(self, data):
    file = open(self._WORKING_FILE, 'r+')
    file.truncate()
    feed_hash = dict([(feed['feed_id'], feed['data']) for feed in data])
    file.write(json.dumps(feed_hash))

  def get_data(self, force_refresh=False):
    try:
      file = open(self._WORKING_FILE, 'r')
    except Exception:
      self.train()
      file = open(self._WORKING_FILE, 'r')

    return json.loads(file.read())

  def train(self):
    file = self.read_data()
    prepared = self.prepare_data(file)
    self.write_data(prepared)

  def draw_hist(self, feed_id):
    data = self.get_data().get(feed_id)
    x = []

    for article in data:
      x.append(article[0])

    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

    plt.show()
