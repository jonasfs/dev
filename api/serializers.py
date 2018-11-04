import json

from rest_framework import serializers

from .models import (
	GenericField,
	TextField,
	NumberField,
	DateField,
	EnumField,
	RiskType,
)

FIELD_TYPES = ['text', 'date', 'number']

class EnumFieldSerializer(serializers.ModelSerializer):
	field_type = serializers.SerializerMethodField(read_only=True)


	class Meta:
		model = EnumField
		exclude = ('risktype',)


	def get_field_type(self, obj):
		obj_with_class = GenericField.objects.get_subclass(id=obj.id)
		return type(obj_with_class).__name__

class FieldSerializer(serializers.ModelSerializer):
	field_type = serializers.SerializerMethodField(read_only=True)


	class Meta:
		model = GenericField
		exclude = ('risktype',)
	

	def get_field_type(self, obj):
		obj_with_class = GenericField.objects.get_subclass(id=obj.id)
		return type(obj_with_class).__name__


	def to_representation(self, obj):
		# Every 'try, except' here is checking for the field type in order to 
		# use the correct serializer.
		# Since the only special serializer is the enum type one, we left all 
		# the others using the default FieldSerializer.
		try:
			enum_field_obj = EnumField.objects.get(id=obj.id)
			return EnumFieldSerializer(
				enum_field_obj,
				context=self.context
			).to_representation(enum_field_obj)
		except EnumField.DoesNotExist:
			pass

		return super(FieldSerializer, self).to_representation(obj)


class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.IntegerField(read_only=True)
	fields = FieldSerializer(
		many=True,
		read_only=True
	)


	class Meta:
		model = RiskType
		fields = '__all__'


	# field types validation
	def validate_fields(self, value):
		try:
			field_names = value.keys()
			if (len(field_names) == 0):
				message = "Insufficient data"
				raise serializers.ValidationError(message)
			for field_name, field_type in value.items():

				try:
					if (
						(not isinstance(field_type, (list,)))
						   and (field_type not in FIELD_TYPES)
					):
						message = field_name + ": Invalid field type ("
						message += str(field_type) + ")"
						raise serializers.ValidationError(message)
				except IndexError:
					if field_type != "":
						message = field_name + ": Invalid field type ("
						message += str(field_type) + ")"
						raise serializers.ValidationError(message)
		except AttributeError:
			message = "Insufficient data"
			raise serializers.ValidationError(message)

		return value

	def create(self, validated_data):
		fields_data = self.context.get('fields')
		self.validate_fields(fields_data)
		risktype = RiskType.objects.create(**validated_data)

		for field_name, field_type in fields_data.items():
			if field_type == 'text':
				TextField.objects.create(
					name=field_name,
					risktype=risktype
				)
			elif field_type == 'number':
				NumberField.objects.create(
					name=field_name,
					risktype=risktype
				)
			elif field_type == 'date':
				DateField.objects.create(
					name=field_name,
					risktype=risktype
				)
			elif isinstance(field_type, (list,)):
				EnumField.objects.create(
					name=field_name,
					choices=field_type,
					risktype=risktype
				)
		return risktype

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
