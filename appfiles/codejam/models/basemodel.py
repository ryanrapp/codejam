# BaseModel for calculating

class BaseModel(object):
  """Abstract base model to estimate next interval"""
  description = "Unknown Model"
  do_last = True

  def predict_interval(self, t, result):
    raise NotImplementedError

  def adjust_prediction(self, t, predicted_y):
    raise NotImplementedError

  def get_interval(self, t, result):
    predicted_y = self.predict_interval(t, result)
    return self.adjust_prediction(t, predicted_y)
