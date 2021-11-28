from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action

from kolibri.core.auth.permissions.base import lookup_field_with_fks

from .models import MatchUpDetails
from .serializer import AdminMatchUpPayloadSerializer
from .serializer import CoachMatchUpPayloadSerializer
from .serializer import LearnerMatchUpPayloadSerializer
from .admin_matchup_helper import get_matchup


class AdminMatchUpViewset(viewsets.GenericViewSet, ListModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = AdminMatchUpPayloadSerializer
    lookup_field = 'subject'
    

    def __get_query_param_cache(self, value):
        if value is None or value.lower() == 'true':
           return True
        if value.lower() == 'false':
            return False  

    def list(self, request):
        cache = self.__get_query_param_cache(request.GET.get('cache', None))
        subject = request.GET.get('subject', None)
        if subject is None:
           return Response("Mandatory param: subject is missing", status=status.HTTP_400_BAD_REQUEST)

        result = []
        result.append(get_matchup(subject=subject, retrieveFromCache=cache))   
        return Response(result, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        return Response("Success", status=status.HTTP_200_OK)      

  


class CoachMatchUpViewset(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = CoachMatchUpPayloadSerializer  

class LearnerMatchUpViewset(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = LearnerMatchUpPayloadSerializer        