import json

from rest_framework import serializers

from .models import (
	RiskType,
)

FIELD_TYPES = ['text', 'date', 'number']


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.IntegerField(read_only=True)
	class Meta:
		model = RiskType
		fields = '__all__'

	# field types validation
	def validate_fields(self, value):
		field_names = value.keys()
		try:
			if (len(field_names) == 0):
				message = "Insufficient data"
				raise serializers.ValidationError(message)
			for field_name, field_type in value.items():

				try:
					if (
						(not (
							(field_type[0] == '[') and (field_type[-1] == ']')
						)) and field_type not in FIELD_TYPES):
						message = field_name + ": Invalid field type ("
						message += field_type + ")"
						raise serializers.ValidationError(message)
					# check for enum too
					elif (field_type[0] == '[') and (field_type[-1] == ']'):
						try:
							json.loads(field_type)
						except ValueError:
							message = field_name + ": Invalid JSON ("
							message += field_type + ")"
							raise serializers.ValidationError(message)
				except IndexError:
					if field_type != "":
						message = field_name + ": Invalid field type ("
						message += field_type + ")"
						raise serializers.ValidationError(message)
		except AttributeError:
			message = "Insufficient data"
			raise serializers.ValidationError(message)

		return value

	def update(self, instance, validated_data):
		method = str(self.context['request'].method)
		if (method == "PATCH"):
			try:
				data_fields = validated_data.pop('fields')
				new_fields = instance.fields
				for field_name, field_type in data_fields.items():
					if field_type:
						new_fields[field_name] = field_type
					else:
						new_fields.pop(field_name)
				instance.fields = new_fields
				instance.save()
			except KeyError:
				pass

		instance = super(RiskTypeSerializer, self).update(
			instance,
			validated_data
		)
		return instance
