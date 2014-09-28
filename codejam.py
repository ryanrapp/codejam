import numpy as np
import scipy
import pprint

from codejam import trainer, dispatcher
from codejam import mockcrawler
from codejam import judge
from codejam.models import arima, exponential, tree, ols

def jam():
  mytrainer = trainer.Trainer()
  mytrainer.train()

  #mytrainer.draw_hist('254130')

  arima_model = arima.ArimaModel(3, 5)
  exponential_model = exponential.ExponentialModel(.8, 20)
  tree_model = tree.TreeModel()
  ols_model = ols.OLSModel()

  current_model = tree_model

  #mymodels = [arima_model, exponential_model, tree_model, ols_model]
  mymodels = [exponential_model]
  myfeeds = ['254130', '649380', '703143']

  f = myfeeds[0]

  mydata = mytrainer.get_data()

  total_score = 0
  total_article_score = 0
  total_missed_penalty = 0
  total_efficiency_bonus = 0

  for feed_id in mydata:
    m = exponential.ExponentialModel(.8, 20)
    print "Model: %s" % m.description
    mycrawler = mockcrawler.MockCrawler(mytrainer)
    myjudge = judge.Judge(mycrawler)
    d = dispatcher.Dispatcher(mycrawler, myjudge)
    score, article_score, missed_penalty, efficiency_bonus = d.process_feed(feed_id, m)
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
