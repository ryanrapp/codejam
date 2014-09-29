#Define ols regression learning
from codejam.models import basemodel
from sklearn import linear_model
import pprint

class OLSModel(basemodel.BaseModel):
  """Uses decision tree to estimate next time to crawl"""
  description = "OLS Model"
  def __init__(self):
    self.clf = linear_model.Ridge(alpha = .5)
    self.results = []

  def train(self, X, y):
    self.clf.fit(X, y)

  def adjust_prediction(self, predicted_y):
    return max(predicted_y, 1)

  def predict_interval(self, result):
    y_hat = [100]
    self.results.append(result)

    clf = linear_model.Ridge(alpha = .5)

    x_stack = []
    X = []
    y = []
    for i in range(0, len(result)):
      if i > 1:
        if i < len(result) - 1:
          X.append([i,result[i][0] - result[i-1][0]])
          y.append(result[i+1][0] - result[i][0])

    if len(X) != len(y):
      raise Exception('X and y need to be same length')
    if len(X) > 2:
      clf.fit(X, y)
      y_hat = clf.predict([len(result)])

      pprint.pprint({'X':X, 'y':y, 'y_hat':y_hat})

    return y_hat[0]
