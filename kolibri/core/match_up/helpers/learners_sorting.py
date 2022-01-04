from kolibri.core.auth.models import FacilityDataset, FacilityUser, Classroom
import re
from django.db.models import Q
from collections import defaultdict

COLLECTION_KIND_FACILITY = 'facility'

# Gets all learners for a subject and divides them into mentees and mentors
def get_learners(subject, facility_id):
  learners = get_learners_by_subject(subject, facility_id)
  if len(learners) == 0:
    print("No learners found.")
    return ([], [])
  
  # if the `sort_match_up_by_physical_facility_level` flag is True, use the physical facility's (eg: school)
  # level (eg: class or grade or standard) in the match-up sorting
  sort_by_physical_facility_level = sort_match_up_by_physical_facility_level(facility_id)  
  # Sort the learners by level in the subject  
  learners.sort(key=lambda x:x.get('memberships__collection__name'), reverse=True)

  # split learners into equal size groups of mentees and mentors
  mentees, mentors = split_learners(learners) 

  # Sort the learners by level in their physical facility (eg: school)
  mentees.sort(key=lambda x:x.get('physical_facility_level'), reverse=False)
  print(mentees)
  mentors.sort(key=lambda x:x.get('physical_facility_level'), reverse=False)
  print(mentors)
  
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

def __group_learners_by_level(learners):
  learnersByLevel = []
  for learner in learners:
    level = learner['memberships__collection__name']
    if learnersByLevel[level] is None:
      learnersByLevel[level] = {}
    learnersByLevel[level].push(level)  


def split_learners(learners):
  number_of_learners = len(learners)
  if number_of_learners == 1:
    return ([], learners)
  middle_index = number_of_learners//2
  mentors = learners[:middle_index]
  mentees = learners[middle_index:]
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