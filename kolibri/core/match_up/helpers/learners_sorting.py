from kolibri.core.auth.models import FacilityDataset, FacilityUser, Classroom
import re
from django.db.models import Q
from collections import defaultdict

COLLECTION_KIND_FACILITY = 'facility'
MENTOR_PHYSICAL_CLASSES = ['8','7','6','5']

# Gets all learners for a subject and divides them into mentees and mentors
def get_learners(subject, facility_id):
  learners = get_learners_by_subject(subject, facility_id)
  if len(learners) == 0:
    print("No learners found.")
    return ([], [])
  
  mentors, mentees = split_learners(learners) 
  mentors.sort(key=lambda x:x.get('memberships__collection__name'), reverse=True) 

  for mentor in mentors:
    print(mentor['memberships__collection__name'] + ' --- ' + mentor['physical_facility_level'])

  print("---------------------------------------")  
  for mentee in mentees:
    print(mentee['memberships__collection__name'] + ' --- ' + mentee['physical_facility_level'])
  return mentees, mentors


def get_learners_by_subject(subject, facility_id):
  classroom_queryset = Classroom.objects.filter(name__iregex=r'^' + re.escape(subject) + '\s[0-9]+$', 
  parent_id = facility_id).values_list('id', flat=True)
  classrooms = list(classroom_queryset)
  learners_queryset = FacilityUser.objects.filter(Q(memberships__collection__in=classrooms)).distinct().values(
        "id",
        "username",
        "full_name",
        "physical_facility_level",
        "gender",
        "memberships__collection__id",
        "memberships__collection__name"
    )
  learners = [learner for learner in learners_queryset] 
  return learners  

def __sort_learners_by_physical_facility_level(learners):
 # result = []
# learners_by_Level = {}
 # for learner in learners:
  #  level = learner['memberships__collection__name']
  #  if level not in learners_by_Level:
   #   learners_by_Level[level] = []
  #  learners_by_Level[level].append(learner)  

  #for level, learners_in_level in learners_by_Level.items():
  learners.sort(key=lambda x:x.get('physical_facility_level'), reverse=True)
  print(learners)
  return learners
   # result += learners_in_level

  #result.sort(key=lambda x:x.get('memberships__collection__name'), reverse=True)  
 # return result


#Spliting students strictly on the basis of physical facility class
def split_learners(learners):
  number_of_learners = len(learners)
  if number_of_learners == 1:
    return ([], learners)
  mentors = []
  mentees = []
  for learner in learners:
    if learner['physical_facility_level'] in MENTOR_PHYSICAL_CLASSES:
      mentors.append(learner)
    else:
      mentees.append(learner)  
  return (mentors, mentees)  


def sort_match_up_by_physical_facility_level(facility_id):
    queryset = get_facility_dataset(facility_id)
    return queryset[0]['sort_match_up_by_physical_facility_level']


def get_facility_dataset(facility_id):
    dataset = FacilityDataset.objects.filter(
            collection__kind=COLLECTION_KIND_FACILITY,
            collection__id=facility_id
        ).distinct().values("allow_match_up_same_gender", "sort_match_up_by_physical_facility_level")  
    return dataset      