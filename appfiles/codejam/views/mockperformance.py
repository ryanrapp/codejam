# Displays performance outcomes. Rules are reverse-engineered from the
# API endpoint

from codejam.views import baseperformance

class MockPerformance(baseperformance.BasePerformance):
  """Calculates and displays performance information."""

  def __init__(self, crawler):
    self.crawler = crawler

  @classmethod
  def score_article(cls, seconds_since_scraped):
    return max(1, 15 - seconds_since_scraped / 120)

  def score_results(self, feed_id, start_time, end_time, poll_seconds,
      found_articles = None):

    total_posts = self.crawler.get_total_posts(feed_id, start_time, end_time)

    article_score = 0
    total_staleness = 0
    efficiency_bonus = 48 - self.crawler.utilization_by_feed.get(feed_id)

    for myid in found_articles:
      staleness = found_articles[myid]
      article_score += self.score_article(staleness)
      total_staleness += staleness

    uq_article_count = len(found_articles)
    missed_penalty = -100 * (total_posts - uq_article_count)

    score = article_score + missed_penalty + efficiency_bonus

    MockPerformance.print_results(
        feed_id, score, article_score, missed_penalty, efficiency_bonus,
        total_posts, uq_article_count)

    return (score, article_score, missed_penalty, efficiency_bonus)
