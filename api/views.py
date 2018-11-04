from rest_framework import viewsets

from .models import (
	RiskType,
)
from .serializers import (
	RiskTypeSerializer,
)


class RiskTypeViewSet(viewsets.ModelViewSet):
	queryset = RiskType.objects.all()
	serializer_class = RiskTypeSerializer

	def get_serializer_context(self):
		context = super(RiskTypeViewSet, self).get_serializer_context()
		try:
			context['fields'] = self.request.data['fields']
		except KeyError:
			pass
		return context
