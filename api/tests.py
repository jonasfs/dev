from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import RiskType


class RiskTypeTests(APITestCase):
	def setUp(self):
		self.url = reverse('risktype-list')
		data = {
			'name': 'House',
			'fields': {
				'owner': 'text',
				'purchased_in': 'date'
			}
		}
		self.response = self.client.post(self.url, data, format='json')

	def test_create_empty_name_risktype(self):
		url = self.url
		data = {
			'name': '',
			'fields': {
				'owner': 'text',
				'purchased_in': 'date'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_empty_fields_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': {
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_name_missing_risktype(self):
		url = self.url
		data = {
			'fields': {
				'owner': 'text',
				'purchased_in': 'date'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_fields_missing_risktype(self):
		url = self.url
		data = {
			'name': 'Car'
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_illegal_fields_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': {
				'owner': 'illegal',
				'purchased_in': 'whatever'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_illegal_enum_field_risktype(self):
		url = self.url
		data = {
			'name': 'Car',
			'fields': {
				'owner': 'text',
				'purchased_in': 'date',
				'price': 'number',
				'choices': ']['
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_non_unique_name_risktype(self):
		url = self.url
		data = {
			'name': 'House',
			'fields': {
				'owner': 'text',
				'purchased_in': 'date'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(RiskType.objects.count(), 1)

	def test_create_risktype(self):
		url = self.url
		response = self.response
		data = {
			'name': 'Car',
			'fields': {
				'owner': 'text',
				'purchased_in': 'date'
			}
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
			'fields': {
				'first_owner': '["yes","no"]',
				'price': 'number',
				'purchased_in': 'date'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')

	def test_multiple_create_risktype(self):
		url = self.url
		response = self.response
		data = {
			'name': 'Car',
			'fields': {
				'first_owner': '["yes","no"]',
				'price': 'number',
				'purchased_in': 'date'
			}
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(RiskType.objects.count(), 2)
		qs = RiskType.objects.all()
		self.assertEqual(qs[0].name, 'House')
		self.assertEqual(qs[1].name, 'Car')

	def test_patch_risktype(self):
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

		data = {
			'fields': {
				'owner_age': 'number'
			}
		}
		response = self.client.patch(patch_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			RiskType.objects.latest('id').fields, {
				'owner_age': 'number',
				'owner': 'text',
				'purchased_in': 'date'
			}
		)

	def test_put_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		put_url = url + rt_id + '/'

		data = {
			'name': 'Car',
			'fields': {
				'owner_age': 'number',
			}
		}
		response = self.client.put(put_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(RiskType.objects.count(), 1)
		self.assertEqual(RiskType.objects.latest('id').name, 'Car')
		self.assertEqual(
			RiskType.objects.latest('id').fields, {
				'owner_age': 'number',
			}
		)

	def test_delete_risktype(self):
		url = self.url
		response = self.response
		rt_id = str(response.data['id'])
		delete_url = url + rt_id + '/'
		response = self.client.delete(delete_url, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(RiskType.objects.count(), 0)
