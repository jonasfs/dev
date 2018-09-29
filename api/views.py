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
