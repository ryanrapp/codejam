# Defines a "view" that allows dataset to be rendered
# as a set of features for the model

import datetime
from matplotlib import pyplot as plt

import json
import numpy as np
import matplotlib.mlab as mlab
import pdb
import pprint
from codejam import utils

class Features(object):
  """Renders data as features to be analyzed."""

  _TRAINING_FILE = 'data/training_data.txt'
  _WORKING_FILE = 'data/workfile.json'
  _FEED_WHITELIST = ['22425']
  _NUM_FEEDS = 100

  def __init__(self):
    self.dateutil = utils.CJDateUtil()

  def render_datapoint(self, feed_id, date_str, offset = 0):
    date_utc = self.dateutil.to_datetime(date_str)
    date_et = self.dateutil.to_et(date_utc)
    seconds = self.dateutil.to_elapsed_seconds(date_utc)

    daily_seconds = self.dateutil.to_daily_seconds(date_et)
    daily_minutes = self.dateutil.to_daily_minutes(date_et)
    is_business_day = date_et.weekday() < 5

    myid = "%s::%s::%d" % (feed_id, date_str, offset)

    datapoint = (seconds, date_et.weekday(), date_et.hour, myid, offset)

    return datapoint

  def render_datapoints(self, feed_id, data):
    """
    Converts list of date strings into data points.

    Assumes "duplicates" are intended and creates unique ids.
    Sorts the data by elapsed seconds ascending.
    """
    feed_data = []
    offset = 0
    prev_date_str = None
    weak_key_violation_count = {}

    for date_str in data:
      weak_key = (feed_id, date_str)
      if weak_key not in weak_key_violation_count:
        weak_key_violation_count[weak_key] = 0
      else:
        weak_key_violation_count[weak_key] += 1

      offset = weak_key_violation_count[weak_key]
      datapoint = self.render_datapoint(feed_id, date_str, offset)

      feed_data.append(datapoint)
      prev_date_str = date_str

    sorted_feed_data = sorted(feed_data, key=lambda datapoint: datapoint[0])

    return sorted_feed_data

  def _read_data(self):
    file = open(self._TRAINING_FILE, 'r')
    return file

  def _prepare_data(self, file):
    processed = 0
    myid = 0
    for line in file:
      data = line.split()
      feed_id = data[0]

      if processed < self._NUM_FEEDS:
        feed_data = self.render_datapoints(feed_id, data[1:])
        processed += 1

        yield {'feed_id': feed_id, 'data': feed_data}

  def _write_data(self, data):
    file = open(self._WORKING_FILE, 'r+')
    file.truncate()
    feed_hash = dict([(feed['feed_id'], feed['data']) for feed in data])
    file.write(json.dumps(feed_hash))

  def process_training_data(self):
    print "processing data from file"
    file = self._read_data()
    prepared = self._prepare_data(file)
    self._write_data(prepared)

  def get_data(self, force_refresh=False):
    try:
      file = open(self._WORKING_FILE, 'r')
    except Exception:
      self.train()
      file = open(self._WORKING_FILE, 'r')

    mydata = json.loads(file.read())

    # for item in mydata['254130']:
    #   print item

    return mydata

  def draw_hist(self, feed_id, feature=0):
    data = self.get_data().get(feed_id)
    x = []

    for article in data:
      x.append(article[feature])

    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

    #plt.show()

  def get_average_feeds(self, feed_id):
    data = self.get_data().get(feed_id)
    x = []
    for article in data:
      if article[1] < 5:
        x.append(article[2])

    n, bins = np.histogram(x, 23)

    total = len(data)

    #n = [3600 / max(1,float(i)) for i in n]

    return n
