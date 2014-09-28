#Defines decision tree model
from codejam.models import basemodel
from sklearn import tree
import pprint

class TreeModel(basemodel.BaseModel):
  """Uses decision tree to estimate next time to crawl"""
  description = "Tree Model"
  def __init__(self):
    self.clf = tree.DecisionTreeRegressor()
    self.results = []

  def train(self, X, y):
    self.clf.fit(X, y)

  def adjust_prediction(self, predicted_y):
    return max(predicted_y * .4, 1)

  def predict_interval(self, result):
    y_hat = [100]
    self.results.append(result)

    clf = tree.DecisionTreeRegressor()

    x_stack = []
    X = []
    y = []
    for i in range(0, len(result)):
      if i > 1:
        x_stack.append(result[i][0] - result[i-1][0])
        if i < len(result) - 1:
          x = [10] * (len(result) - i - 1)
          x.extend(x_stack)
          X.append(x)
          y.append(result[i+1][0] - result[i][0])

    if len(X) != len(y):
      raise Exception('X and y need to be same length')
    if len(X) > 2:
      clf.fit(X, y)
      y_hat = clf.predict(x_stack)

    return y_hat[0]
