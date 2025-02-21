from rest_framework import viewsets
from .models import contact_us
from .serializers import ContactUsSerializer
# Create your views here.
class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = contact_us.objects.all()
    serializer_class = ContactUsSerializer
    