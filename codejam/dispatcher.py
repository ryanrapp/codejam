import datetime
from matplotlib import pyplot as plt
import dateutil.parser
from dateutil import tz
import json
import numpy as np
import matplotlib.mlab as mlab
import pdb
import pprint


class Dispatcher(object):
  _START_TIME = 0
  _END_TIME = 86381

  def __init__(self, crawler, judge):
    self.crawler = crawler
    self.judge = judge

  def _analyze_result(self, feed_id, t, result):
    """Analyze result and set next poll interval"""
    if result is not None and len(result):
      staleness = result[-1][0]

      for post in result:
        staleness = t - post[0]
        myid = (feed_id, post[0])
        if (myid not in self.scraped_articles or
            staleness < self.scraped_articles[myid]):
          self.scraped_articles[(feed_id, post[0])] = staleness

      self.interval = self.model.predict_interval(result)
      #print self.interval

  def process_feed(self, feed_id, model):
    t = self._START_TIME
    self.start_interval = 1000
    self.interval = 100
    self.scraped_articles = {}
    self.arima_q = 10
    self.result_paces = []
    self.model = model

    article_target = 0

    t += self.start_interval

    while t < self._END_TIME:
      result = self.crawler.crawl(feed_id, t)
      self._analyze_result(feed_id, t, result)
      t += self.interval

    self.judge.score_results(feed_id, self.scraped_articles)
