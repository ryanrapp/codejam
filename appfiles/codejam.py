import numpy as np
import scipy
import pprint
import datetime

from codejam.controllers import trainer, dispatcher
from codejam.controllers import mockcrawler, apicrawler
from codejam.models import arima, exponential, tree, ols
from codejam.views import features
from codejam.views import apiperformance, mockperformance
from codejam import utils

import sys

def get_sys_params():

  lines = sys.stdin.read().rstrip().split('\n')
  api_url = lines[0]
  date = lines[1]
  feed_ids = lines[2:]

  return api_url, date, feed_ids


def jam():
  api_url, date, feed_ids = get_sys_params()

  dataview = features.Features()
  #dataview.process_training_data()

  myfeeds = ['254130', '649380', '703143']

  mydata = dataview.get_data()

  total_score = 0
  total_article_score = 0
  total_missed_penalty = 0
  total_efficiency_bonus = 0

  mydateutil = utils.CJDateUtil()

  start_date = mydateutil.to_datetime(date)
  end_date = start_date + datetime.timedelta(hours=23, minutes=59, seconds=59)
  
  print "Date range: %s -> %s" % (start_date, end_date)

  start_time = mydateutil.to_elapsed_seconds(start_date)
  end_time = mydateutil.to_elapsed_seconds(end_date)

  for feed_id in feed_ids:
    print "Processing feed %s..." % feed_id
    mymodel = exponential.ExponentialModel(.8, 10)
    mydateutil = 0

    #mycrawler = mockcrawler.MockCrawler(mydata)
    mycrawler = apicrawler.APICrawler(dataview)
    #view = mockperformance.MockPerformance(mycrawler)
    view = apiperformance.APIPerformance(mycrawler)

    # myapicrawler = apicrawler.APICrawler(dataview)
    # result = myapicrawler.crawl(feed_id, 300000)
    # pprint.pprint(result)
    # return

    hist = dataview.get_average_feeds(feed_id)
    d = dispatcher.Dispatcher(mycrawler, hist)
    found_articles, poll_seconds = d.process_feed(feed_id, mymodel, start_time, end_time)

    score, article_score, missed_penalty, efficiency_bonus = view.score_results(
        feed_id, start_time, end_time, poll_seconds, found_articles)
    total_score += score
    total_article_score += article_score
    total_missed_penalty += missed_penalty
    total_efficiency_bonus += efficiency_bonus

  pprint.pprint({
    'total_score': total_score,
    'total_article_score': total_article_score,
    'total_missed_penalty': total_missed_penalty,
    'total_efficiency_bonus': total_efficiency_bonus
  })


if __name__ == "__main__":
  jam()
