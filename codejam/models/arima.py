#Calculate Arima Model
from codejam.models import basemodel

class ArimaModel(basemodel.BaseModel):
  """Uses ARIMA(p,q) to estimate next time to crawl"""
  def __init__(self, p = 3, q = 10):
    self.arima_q = 10
    self.result_paces = []

  def predict_interval(self, result):
    interval = 100
    arima_result = result[0:min(self.arima_q, len(result))]
    result_diameter = float(
        arima_result[-1][0] - arima_result[0][0])

    if result_diameter > 0:
      result_pace = round(len(result) / result_diameter,8)
      self.result_paces.append(result_pace)

      interval = (10/self.arima_q) / result_pace
    else:
      pass
      #print result_diameter

    return interval
