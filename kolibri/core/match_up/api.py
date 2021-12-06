from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response

from .models import MatchUpDetails
from .serializer import AdminMatchUpPayloadSerializer, CoachMatchUpPayloadSerializer, LearnerMatchUpPayloadSerializer, MatchUpDetailsSerializer
from .helpers.admin_matchup_helper import get_matchup_for_admin, update_matchups
from .helpers.coach_matchup_helper import get_matchup_for_coach
from .helpers.learner_match_helper import get_matchup_for_learner



class AdminMatchUpViewset(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = AdminMatchUpPayloadSerializer
    lookup_field = 'subject'
    
    def list(self, request):
        subject = request.GET.get('subject', None)
        facility_id = request.GET.get("facility")
        if subject is None or facility_id is None:
           return Response("Mandatory param is missing", status=status.HTTP_400_BAD_REQUEST)

        result = []
        result.append(get_matchup_for_admin(facility_id, subject))   
        return Response(result, status=status.HTTP_200_OK)
    
    def create(self, request):
        update_matchups(request.data)
        return Response(request.data, status=status.HTTP_200_OK)      


class CoachMatchUpViewset(viewsets.GenericViewSet, RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = CoachMatchUpPayloadSerializer  
    lookup_field = 'user'
    
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        facility_id = request.GET.get("facility")
        if facility_id is None:
            return Response("Mandatory param is missing", status=status.HTTP_400_BAD_REQUEST)
        output = get_matchup_for_coach(user_id, facility_id)
        return Response(output, status=status.HTTP_200_OK)


class LearnerMatchUpViewset(viewsets.GenericViewSet, RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = LearnerMatchUpPayloadSerializer  
    lookup_field = 'user'      

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        facility_id = request.GET.get("facility")
        if facility_id is None:
            return Response("Mandatory param is missing", status=status.HTTP_400_BAD_REQUEST)
        output = get_matchup_for_learner(user_id, facility_id)
        return Response(output, status=status.HTTP_200_OK)

# SuperAdmin APIs
class MatchUpView(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = MatchUpDetails.objects.all()
    serializer_class = MatchUpDetailsSerializer        