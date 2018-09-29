from django.contrib.postgres.fields import JSONField
from django.db import models


class RiskType(models.Model):
	name = models.TextField(unique=True)
	fields = JSONField()

	def __str__(self):
		return self.name
