from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils.managers import InheritanceManager


class RiskType(models.Model):
	name = models.TextField(unique=True)

	def __str__(self):
		return self.name


class GenericField(models.Model):
	name = models.TextField()
	risktype = models.ForeignKey(
		RiskType,
		related_name='fields',
		on_delete=models.CASCADE
	)
	objects = InheritanceManager()


class TextField(GenericField):
	pass


class NumberField(GenericField):
	pass


class DateField(GenericField):
	pass


class EnumField(GenericField):
	choices = ArrayField(models.TextField())
