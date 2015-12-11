import models

from DocumentProcessing import IDFProvider


class TwittosProvider:

	@staticmethod
	def can_update_from_timeline(timeline, username):
		if len(timeline) > 0:
		    lastTweet = timeline[0].id
		    try:
		        twittos = models.Twittos.objects.get(username = username)
		        return twittos.lastTweet < lastTweet
		    except models.Twittos.DoesNotExist:
		        return True
		else:
			return False

	@staticmethod
	def update_twittos_and_idf(timeline, username, tweets):
		if len(timeline) > 0:
			lastTweet = timeline[0].id
			models.Twittos(username = username, lastTweet = lastTweet).save()
			idf = IDFProvider()
			idf.update_with_document(tweets)
		else:
			print "[update_twittos_and_idf]: timeline must not be empty"
