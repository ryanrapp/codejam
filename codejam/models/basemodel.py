# BaseModel for calculating

class BaseModel(object):
  """Abstract base model to estimate next interval"""
  def predict_interval(self, result):
    raise NotImplementedError
