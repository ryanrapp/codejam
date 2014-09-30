#Define dispatcher class

import datetime
import dateutil.parser
from dateutil import tz
import json
import numpy as np
import pdb
import pprint
from codejam import utils


class Dispatcher(object):
  """
  Dispatches crawler and dynamically interprets results.

  Dispatching pace is fitted to time-of-day histogram.
  Pace is dynamically adjusted based on result set timings.
  """
  def __init__(self, crawler, hist):
    self.crawler = crawler
    self.feed_results = {}
    self.hist = hist
    self.dateutil = utils.CJDateUtil()
    self.last_time = 0
    self.multiplier = 0
    self.num_articles = 0
    for i in hist:
      self.num_articles += i

    self.mybase = min(1882853 / self.num_articles, 2336)

  def _analyze_result(self, feed_id, t, result):
    """Analyze result and set next poll interval"""
    if result is not None and len(result):
      staleness = result[-1][0]
      num_found = 0
      for post in result:
        staleness = t - post[0]
        myid = post[3]
        if (myid not in self.scraped_articles or
            staleness < self.scraped_articles[myid]):
          if myid not in self.scraped_articles:
            self.feed_results[feed_id].append(post)
            num_found += 1
          self.scraped_articles[myid] = staleness

      if result[-1][0] == self.last_time:
        self.multiplier = 1
      else:
        self.multiplier = .5

      self.last_time = result[-1][0]

      # Sophisticated models are currently disabled because they do not
      # uniformly improve results

      #requested_interval = self.model.get_interval(t, self.feed_results[feed_id])

      self.interval = min(self.multiplier * self.get_baseline(t), self.mybase)

  def dispatch(self, feed_id, t):
    """Dispatch crawler for timing t."""
    result = self.crawler.crawl(feed_id, t)
    self._analyze_result(feed_id, t, result)

  def get_baseline(self, t):
    """Determine the ideal pace baseline."""
    datetime_utc = self.dateutil.from_seconds_to_datetime(t)
    datetime_et = self.dateutil.to_et(datetime_utc)
    n_hat = 1
    if datetime_et.hour < len(self.hist):
      n_hat = self.hist[datetime_et.hour - 1]

    # Scale observations to a single day
    baseline = float(24 * 3600) / max(1, n_hat)

    return baseline

  def process_feed(self, feed_id, model, start_time=0, end_time=1882853):
    t = start_time
    self.interval = 2336
    self.scraped_articles = {}
    self.result_paces = []
    self.model = model
    self.feed_results[feed_id] = []
    self.end_time = end_time
    self.start_time = start_time

    article_target = 0

    t += self.interval
    poll_seconds = []

    while t < self.end_time:
      self.dispatch(feed_id, t)
      t += self.interval
      t = min(t, end_time)
      poll_seconds.append(t)

    return self.scraped_articles, poll_seconds
