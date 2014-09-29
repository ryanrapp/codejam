# Displays performance outcomes. Rules are reverse-engineered from the
# API endpoint

from codejam.views import baseperformance
from codejam import utils
import pprint
import requests

class APIPerformance(baseperformance.BasePerformance):
  """Returns and displays performance information from API."""

  def __init__(self, crawler, endpoint='http://codejam.airpr.com/score'):
    super(APIPerformance, self).__init__()
    self.dateutil = utils.CJDateUtil()
    self.endpoint = endpoint

  def score_results(self, feed_id, start_time, end_time, poll_seconds, found_articles = None):
    poll_times = []
    for poll_second in poll_seconds:
      poll_time = self.dateutil.from_seconds_to_datetime(poll_second)
      poll_time.isoformat()
      poll_times.append(poll_time)

    params = {'feed_id': str(feed_id), 'poll_times': poll_times}
    pprint.pprint(params)
    r = requests.post(self.endpoint, data=params)

    response = r.json()

    score = float(response.get('total_score'))
    article_score  = float(response.get('article_score'))
    missed_penalty  = float(response.get('missed_article_penalty'))
    efficiency_bonus = float(response.get('efficiency_bonus'))

    APIPerformance.print_results(
        feed_id, score, article_score, missed_penalty, efficiency_bonus)

    return (score, article_score, missed_penalty, efficiency_bonus)
