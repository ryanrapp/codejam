class Judge(object):
  """Scores the performance according to the rules."""

  def __init__(self, crawler):
    self.crawler = crawler

  @classmethod
  def score_article(cls, seconds_since_scraped):
    return max(1, 15 - seconds_since_scraped / 120)

  def score_results(self, feed_id, scraped_articles):
    total_posts = self.crawler.get_total_posts(feed_id)

    article_score = 0
    total_staleness = 0
    efficiency_bonus = 48 - self.crawler.utilization_by_feed.get(feed_id)

    for myid in scraped_articles:
      staleness = scraped_articles[myid]
      article_score += self.score_article(staleness)
      total_staleness += staleness

    uq_article_count = len(scraped_articles)
    missed_penalty = -100 * (total_posts - uq_article_count)

    score = article_score + missed_penalty + efficiency_bonus

    print "[%s]" % feed_id
    print "total_articles: %d" % total_posts
    print "articles_found: %d" % uq_article_count

    print "article_score: %d" % article_score
    print "missed penalty: %d" % missed_penalty
    print "efficiency bonus: %d" % efficiency_bonus

    print "total_score: %d" % score

    print "----"
