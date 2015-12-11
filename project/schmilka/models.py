from django.db import models

# Create your models here.
class IDF(models.Model):	
   
    token = models.CharField(max_length = 50, primary_key = True)
    nbDoc = models.IntegerField()

    def __str__(self):
        return self.token


class Twittos(models.Model):

	username  = models.CharField(max_length = 50, primary_key = True)
	lastTweet = models.BigIntegerField()

	def __str__(self):
		return self.username


class Meta(models.Model):

    key = models.CharField(max_length = 30, primary_key = True)
    value = models.IntegerField()

    def __str__(self):
        return self.key
