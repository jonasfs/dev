from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import RiskType, NumberField, DateField


class RiskTypeTests(APITestCase):
	def setUp(self):
		self.url = reverse('risktype-list')
		data = {
			'name': 'House',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		self.response = self.client.post(self.url, data, format='json')

	def test_create_empty_name_risktype(self):
		url = self.url
		data = {
			'name': '',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_no_fields_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
		}
		response = self.client.post(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')

	def test_create_empty_fields_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': []
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')

	def test_create_name_missing_risktype(self):
		url = self.url
		data = {
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_illegal_fields_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'illegal',
				},
				{
					'name': 'purchased_in',
					'field_type': 'whatever'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_illegal_enum_field_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				},
				{
					'name': 'price',
					'field_type': 'number'
				},
				{
					'name': 'choices',
					'field_type': ']['
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_non_unique_name_risktype(self):
		url = self.url
		data = {
			'name': 'House',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_risktype(self):
		url = self.url
		response = self.response
		data = {
			'name': 'Car',
			'fields': [
				{
					'name': 'owner',
					'field_type': 'text',
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')

	def test_create_risktype_with_enum(self):
		url = self.url
		response = self.response
		data = {
			'name': 'Car',
			'fields': [
				{
					'name': 'first_owner',
					'field_type': ['yes', 'no'],
				},
				{
					'name': 'price',
					'field_type': 'number'
				},
				{
					'name': 'purchased_in',
					'field_type': 'date'
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		risktype = RiskType.objects.latest('id')
		self.assertEqual(risktype.name, 'Car')
		enum_field = risktype.fields.get_subclass(name='first_owner')
		self.assertEqual(enum_field.choices, ['yes', 'no'])

	def test_patch_risktype_name(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		patch_url = url + rt_id + '/'
		data = {
			'name': 'Car'
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(RiskType.objects.count(), 1)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')

	def test_patch_existing_field_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		field_id = response.data['fields'][1]['id']
		patch_url = url + rt_id + '/'
		data = {
			'fields': [
				{
					'id': field_id,
					'name': 'owner_birthday',
					'field_type': 'date'
				},
			]
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		latest_object = RiskType.objects.latest('id')
		field = latest_object.fields.get_subclass(id=field_id)
		self.assertEqual(field.name, 'owner_birthday')
		self.assertEqual(isinstance(field, DateField), True)

	def test_patch_existing_field_risktype_without_field_type(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		field_id = response.data['fields'][1]['id']
		patch_url = url + rt_id + '/'
		data = {
			'fields': [
				{
					'id': field_id,
					'name': 'owner_birthday'
				},
			]
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		latest_object = RiskType.objects.latest('id')
		field = latest_object.fields.get_subclass(id=field_id)
		self.assertEqual(field.name, 'owner_birthday')
		self.assertEqual(isinstance(field, DateField), True)

	def test_patch_existing_field_risktype_with_diff_field_type(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		field_id = response.data['fields'][1]['id']
		patch_url = url + rt_id + '/'
		data = {
			'fields': [
				{
					'id': field_id,
					'name': 'owner_birthday',
					'field_type': 'text'
				},
			]
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_patch_new_field_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		patch_url = url + rt_id + '/'
		data = {
			'fields': [
				{
					'name': 'owner_birthday',
					'field_type': 'date'
				},
			]
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		latest_object = RiskType.objects.latest('id')
		fields = latest_object.fields.select_subclasses()
		self.assertEqual(fields.count(), 3)
		latest_field = fields.latest('id')
		self.assertEqual(latest_field.name, 'owner_birthday')
		self.assertEqual(isinstance(latest_field, DateField), True)

	def test_put_alter_fields_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		put_url = url + rt_id + '/'

		data = {
			'name': 'Car',
			'fields': [
				{
					'name': 'owner_age',
					'field_type': 'number'
				}
			]
		}
		response = self.client.put(put_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(RiskType.objects.count(), 1)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')
		fields = RiskType.objects.latest('id').fields
		self.assertEqual(fields.count(), 1)
		field = fields.get_subclass()
		self.assertEqual(field.name, 'owner_age')
		self.assertEqual(isinstance(field, NumberField), True)

	def test_delete_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		delete_url = url + rt_id + '/'
		response = self.client.delete(delete_url, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(RiskType.objects.count(), 0)
