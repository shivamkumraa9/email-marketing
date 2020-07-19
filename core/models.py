from django.db import models

class Template(models.Model):
	name = models.CharField(max_length = 20)
	html = models.TextField()

	def __str__(self):
		return self.name