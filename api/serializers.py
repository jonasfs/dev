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


def translate_field_type(field_obj):
	field_class = type(field_obj).__name__
	if field_class == 'GenericField':
		return 'generic'
	elif field_class == 'TextField':
		return 'text'
	elif field_class == 'NumberField':
		return 'number'
	elif field_class == 'DateField':
		return 'date'
	elif field_class == 'EnumField':
		return str(field_obj.choices)


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
	def validate_fields(self, fields):
		try:
			if (len(fields) == 0):
				message = "Insufficient data"
				raise serializers.ValidationError(message)
			for field in fields:
				field_type = field['field_type']
				field_name = field['name']

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

		return fields

	def create(self, validated_data):
		fields_data = self.context.get('fields')
		if fields_data:
			self.validate_fields(fields_data)
		risktype = RiskType.objects.create(**validated_data)

		if fields_data:
			for field in fields_data:
				field_type = field['field_type']
				field_name = field['name']
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
		fields_data = self.context.get('fields')
		method = str(self.context['request'].method)

		if (method == "PATCH"):
			if fields_data:
				for field in fields_data:
					field_id = None
					try:
						if field['id']:
							field_id = field['id']
					except KeyError:
						pass
					# if id exists, patch existing field
					if field_id:
						try:
							field_to_update = instance.fields.get_subclass(
								id=field_id
							)

							field_type = None
							try:
								field_type = field['field_type']

							except KeyError:
								pass

							# patch if the field type is the same or none
							if field_type == translate_field_type(
								field_to_update
							) or field_type is None:
								field_name = field['name']
								field_to_update.name = field_name
								field_to_update.save()
							else:
								message = 'Can\'t patch a field with a different'
								message += ' type (' + field_to_update.name + ')'
								raise serializers.ValidationError(message)

						except GenericField.DoesNotExist:
							message = 'Could fidnt a field with the referenced id'
							message += ' (' + str(field_id) + ')'
							raise serializers.ValidationError(message)
					# otherwise, create a whole new field
					else:
						try:
							self.validate_fields(fields_data)
						except KeyError:
							message = "Insufficient data"
							raise serializers.ValidationError(message)

						field_type = field['field_type']
						field_name = field['name']
						risktype = instance
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

		elif (method == "PUT"):
			try:
				if not validated_data['name']:
					message = "RiskType name missing"
					raise serializers.ValidationError(message)
			except KeyError:
				message = "RiskType name missing"
				raise serializers.ValidationError(message)

			if fields_data:
				instance.fields.all().delete()
				risktype = instance
				for field in fields_data:
					field_type = field['field_type']
					field_name = field['name']
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

		instance = super(RiskTypeSerializer, self).update(
			instance,
			validated_data
		)
		return instance
