# Displays performance outcomes. Rules are reverse-engineered from the
# API endpoint

class BasePerformance(object):
  """Abstract base class to calculate and display performance information."""

  @classmethod
  def score_article(cls, seconds_since_scraped):
    return max(1, 15 - seconds_since_scraped / 120)

  def score_results(self, feed_id, start_time, end_time, poll_seconds, found_articles = None):
    raise NotImplementedError

  @classmethod
  def print_results(cls, feed_id, score, article_score, missed_penalty,
      efficiency_bonus, total_posts=None, uq_article_count=None):
    print "[%s]" % feed_id
    if total_posts is not None:
      print "total_articles: %f" % total_posts
    if uq_article_count is not None:
      print "articles_found: %f" % uq_article_count

    print "article_score: %f" % article_score
    print "missed penalty: %f" % missed_penalty
    print "efficiency bonus: %f" % efficiency_bonus

    print "total_score: %f" % score

    print "----"
