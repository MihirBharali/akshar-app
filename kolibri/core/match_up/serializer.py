from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ListField
from kolibri.core.serializers import KolibriModelSerializer

from .models import MatchUpDetails

# Common serializers

class UserSerializer(Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)

class MatchUpPairs(Serializer):
    mentor = UserSerializer()
    mentee = UserSerializer()

class UnassignedPool(Serializer):
    supervisor_list = ListField(child= UserSerializer(), required = False)
    mentor_list = ListField(child= UserSerializer(), required = False)
    mentee_list = ListField(child= UserSerializer(), required = False)

# Admin specific API serializers

class AdminMatchUpSerializer(Serializer):
    mentor = UserSerializer()
    mentee_list = ListField(child= UserSerializer(), required = False)


class AdminMatchUpDetailsSerializer(Serializer):
    supervisor = UserSerializer()
    match_up = ListField(child= AdminMatchUpSerializer(), required = False)
    


class AdminMatchUpPayloadSerializer(Serializer):
    facility_id = serializers.UUIDField()
    subject = serializers.CharField(max_length=100)
    match_up_details = ListField(child= AdminMatchUpDetailsSerializer(), required = False)
    unassigned_pool = UnassignedPool()

# Coach specifc API serializers

class CoachMatchUpDetailsSerializer(Serializer):
    subject = serializers.CharField(max_length=100)
    pairs = ListField(child= MatchUpPairs(), required = False)


class CoachMatchUpPayloadSerializer(Serializer):
    facility_id = serializers.UUIDField()
    match_up_details = ListField(child= CoachMatchUpDetailsSerializer(), required = False)

# Learner specific API serializers

class LearnerMatchUpPayloadSerializer(Serializer):
    subject = serializers.CharField(max_length=100)
    role = serializers.CharField(max_length=20) #Mentee or Mentor
    mentee_list = ListField(child= UserSerializer(), required = False)
    mentor = UserSerializer()




