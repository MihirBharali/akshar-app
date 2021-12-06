import math
import re
from django.db import transaction
from django.db.models import Q
from kolibri.core.auth.models import FacilityUser, Classroom
from kolibri.utils.main import update


from ..models import MatchUpDetails

MAX_PAIRS_PER_COACH = 10

'''
Processes a ``PUT`` request to update the matchups for a given 
subject and facility
'''
@transaction.atomic
def update_matchups(request):
  print("Processing matchup update request.")
  facility_id = request['facility_id']
  subject = request['subject']
  # this list ``existing_supervisors`` is used to track supervisors which are not in the Request payload
  # All matchups under the supervisors that remain in the list after processing of the request is completed 
  # will be deleted
  existing_supervisors = [supervisor['id'] for supervisor in get_supervisors(facility_id)]
  for item in request['match_up_details']:
    print("Processing a match_up_detail")
    supervisor = item['supervisor']
    supervisor_id = supervisor['id']
    existing_supervisors.remove(supervisor_id)


    # Existing mentors under the supervisor.
    existing_mentors_queryset =  MatchUpDetails.objects.filter(facility_id = facility_id,
          subject = subject,
          supervisor_id = supervisor['id']).distinct().values_list("mentor_id", flat=True) 
    # This is used to track the mentors which are removed from this mentor in the Request payload.
    existing_mentors_id = list(existing_mentors_queryset)      

    # Go through each matchup in the Request and process accordingly
    for matchup in item['match_up']:
      print("Processing a match_up")
      mentor = matchup['mentor']
      mentor_id = mentor['id']
      if mentor_id in existing_mentors_id:
        existing_mentors_id.remove(mentor_id)
      
      # Remove the mentor from the fixed unassignment pool
      MatchUpDetails.objects.filter(
        facility_id = facility_id,
        subject = subject,
        mentor_id = mentor_id,
        keepUnassigned = True).delete()

      # existing mentees having the same supervisor and mentor
      existing_mentees_queryset = MatchUpDetails.objects.filter(facility_id = facility_id,
          subject = subject,
          mentor_id = mentor['id'],
          supervisor_id = supervisor['id']).distinct().values_list("mentee_id", flat=True)

      # this list ``existing_mentees_id`` is used to track existing mentees which are not in the Requet payload
      existing_mentees_id = list(existing_mentees_queryset)    
      
      # If no mentees are provided in the request for the supervisor and mentor pair,
      # Delete all existing pairs that exist for them and add a row with mentee_id == None
      # A null mentee_id is added to display a blank matchup card on UI
      if 'mentee_list' not in matchup or len(matchup['mentee_list']) == 0:
        if len(existing_mentees_id) > 0:
          MatchUpDetails.objects.filter(
            facility_id = facility_id,
            subject = subject,
            mentor_id = mentor['id'],
            supervisor_id = supervisor['id']).delete()
          
          MatchUpDetails.objects.create(
            facility_id = facility_id,
            subject = subject,
            mentor_id = mentor['id'],
            supervisor_id = supervisor['id'],
            mentor_name = mentor['name'],
            supervisor_name = supervisor['name'],
            mentee_id = None,
            mentee_name = None
            )
      else:
        # Remove any matchup entry thats present in the db with mentee_id == None
        # for the specific supervisor-mentor pair
        remove_any_matchup_with_null_mentee(subject, facility_id, supervisor_id, mentor_id)      
        # add the mentees passed in the request      
        for mentee in matchup['mentee_list']:
            # if the mentee passed in request is an existing one, remove it from the list
            # and no action to be performed on DB for that mentee
            if mentee['id'] in existing_mentees_id:
              existing_mentees_id.remove(mentee['id'])  
              continue 
            # Remove the mentee from the fixed unassignment pool
            MatchUpDetails.objects.filter(
              facility_id = facility_id,
              subject = subject,
              mentee_id = mentee['id'],
              keepUnassigned = True).delete()
            MatchUpDetails.objects.create(
              facility_id = facility_id,
              subject = subject,
              mentor_id = mentor['id'],
              supervisor_id = supervisor['id'],
              mentor_name =  mentor['name'],
              supervisor_name = supervisor['name'],
              mentee_id = None if mentee is None else mentee['id'],
              mentee_name = None if mentee is None else mentee['name']
              ) 
      # After processing of the mentee_list, the ``existing_mentees_id`` list will 
      # be left with mentees which are removed from the supervisor-mentor pair
      for mentee_id in existing_mentees_id:
          MatchUpDetails.objects.filter(facility_id = facility_id,
          subject = subject,
          mentor_id = mentor['id'],
          supervisor_id = supervisor['id'],
          mentee_id = mentee_id).delete()
    
    # After process all mentee_list, delete any matchups for a mentor who have been
    # removed from the supervisor
    for mentor_id in existing_mentors_id:
      MatchUpDetails.objects.filter(facility_id = facility_id,
          subject = subject,
          mentor_id = mentor_id,
          supervisor_id = supervisor['id']).delete()

  # After process all match_up for the subject, delete any matchups for a supervisor who have been
  # removed from the subject
  for supervisor_id in existing_supervisors:
    MatchUpDetails.objects.filter(facility_id = facility_id,
          subject = subject,
          supervisor_id = supervisor_id).delete()
  # After processing the insertion and updates of the matchups,
  # finally, need to clean all the matchup rows that exist in db
  # for the users passed in the ``unassigned_pool`` section of the request.
  # Also, update db to add any user that needs to be ignored during automated
  # matchup reassignment
  update_unassigned_pool(request, facility_id, subject)  

  print("Finished updating matchups.")          



'''
Gets the matchups for a facility and a subject.
Even though it generates response for a ``GET`` request,
it does more than simply. If new users are added to the facility, 
they are added to the matchup pool before returning the response 
'''
def get_matchup_for_admin(facility_id, subject):
  
    # list of all prospective mentees and mentors who may or may not be in any matchup  
    # These are just exhaustive lists created by dividing all learners for the
    # specific subject into two list with equal learners after sorting them based on their level.       
    unassigned_mentors, unassigned_mentees = get_learners(subject, facility_id)    
  
    # list of all supervisors for the facility who may or may not be in any matchup 
    unassigned_supervisors = get_supervisors(facility_id)
    
    # Tries to perform a matchup.
    if len(unassigned_mentees) > 0 and len(unassigned_mentors) > 0 and len(unassigned_supervisors) > 0:
      print("Re-assigning")
      assign_matchups(subject, facility_id, unassigned_mentees, unassigned_mentors, unassigned_supervisors)

    queryset = MatchUpDetails.objects.filter(
            subject = subject, facility_id = facility_id, keepUnassigned = False).distinct().values(
                "id",
                "mentee_id",
                "mentee_name",
                "mentor_id",
                "mentor_name",
                "subject",
                "supervisor_id",
                "supervisor_name",
                "facility_id",
                "keepUnassigned"
            )

    #group the pairs by supervisor
    matchup_details_by_supervisor = {}
    #To store matchups which doesnt have any supervisor assigned
    matchup_details_by_supervisor["NO_SUPERVISOR"] = []
    for item in queryset:
      supervisor_id = item['supervisor_id']
      if supervisor_id is None:
        matchup_details_by_supervisor["NO_SUPERVISOR"].append(item)
        continue
      if supervisor_id not in matchup_details_by_supervisor:
        matchup_details_by_supervisor[supervisor_id] = []  

      # remove the supervisor from the unassigned list as they appear in any matchup  
      remove_item_from_list(supervisor_id, unassigned_supervisors)  
      matchup_details_by_supervisor[supervisor_id].append(item)  

    matchup_details = []
    for supervisor_id, pairs in matchup_details_by_supervisor.items():
      if not pairs:
        continue

      matchup_by_mentor = {}
      #grouping by mentor
      for pair in pairs:
        mentor_id = pair['mentor_id']
        if mentor_id not in matchup_by_mentor:
          matchup_by_mentor[mentor_id] = []
        matchup_by_mentor[mentor_id].append(pair)  
        # remove the mentor from the unassigned list as they appear in any matchup 
        remove_item_from_list(mentor_id, unassigned_mentors)
        if pair['mentee_id'] is not None:
          # remove the mentee from the unassigned list as they appear in any matchup 
          remove_item_from_list(pair['mentee_id'], unassigned_mentees)
      
      matchups_for_supervisor = []

      for mentor_id, pairs in matchup_by_mentor.items():
        mentees_for_mentor = []
        mentor = {
          "id": pairs[0]["mentor_id"],
          "name": pairs[0]["mentor_name"]
        }
        for mentee in pairs:
          mentees_for_mentor.append({
            "id": mentee["mentee_id"],
            "name": mentee["mentee_name"]
          })
        matchups_for_supervisor.append({
          "mentor": mentor,
          "mentee_list": mentees_for_mentor
        })    

      supervisor = {
        "id": pairs[0]['supervisor_id'],
        "name": pairs[0]['supervisor_name']
      }
      matchup_for_supervisor = {
        "supervisor": supervisor,
        "match_up": matchups_for_supervisor

      }
      matchup_details.append(matchup_for_supervisor)
     

    # Determine the users which are not part of any matchups 
    mentees_without_matchup = [] 
    mentors_without_matchup = []
    supervisors_without_matchup = []
    for mentor in unassigned_mentors:
      mentors_without_matchup.append({
        "id": mentor['id'],
        "name": mentor['full_name']
      })   
    for mentee in unassigned_mentees:
      mentees_without_matchup.append({
        "id": mentee['id'],
        "name": mentee['full_name']
      })  
    for supervisor in unassigned_supervisors:
      supervisors_without_matchup.append({
        "id": supervisor['id'],
        "name": supervisor['full_name']
      })  
    
    result = {
      "facility_id": facility_id,
      "subject": subject,
      "match_up_details": matchup_details,
      "unassigned_pool": {
        "mentor_list": mentors_without_matchup,
        "mentee_list": mentees_without_matchup,
        "supervisor_list": supervisors_without_matchup
      }
    }
    return result

# Gets all learners for a subject and divides them into mentees and mentors
def get_learners(subject, facility_id):
  learners = get_learners_by_subject(subject, facility_id)
  if len(learners) == 0:
    print("No learners found.")
    return ([], [])
  # Sort the learners by class  
  learners.sort(key=lambda x:x.get('memberships__collection__name'), reverse=True)

  # split learners into equal size groups of mentees and mentors
  mentees, mentors = split_learners(learners) 
  
  return mentees, mentors

# Gets all the supervisors in the facility
def get_supervisors(facility_id):
  supervisors_queryset = FacilityUser.objects.filter(roles__kind__in = ['coach', 'classroom assignable coach'], facility_id =  facility_id).distinct().values(
    "id",
    "full_name"
  )
  supervisors = [supervisor for supervisor in supervisors_queryset]
  return supervisors

# Creates matchup pairs for the given list of mentees, mentors and supervisors
# if no matchup exists currently, performs a full matchup
# in case matchup pairs already exist, performs a PATCH operation to ensure
# that all unassigned mentees, mentors and supervisors are assigned some matchups
# and no existing matchups are updated.
def assign_matchups(subject, facility_id, mentees, mentors, supervisors):
  if len(mentees) == 0 or len(mentors) == 0:
    print("No mentees or mentors found")
    return
  # optimal number of pairs that can be assigned to a supervisor so that they are not overwhelmed
  max_pairs_per_supervisor = get_optimal_pairs_per_supervisor(len(mentees), len(supervisors))

  # existing matchups from DB. 
  existing_matchups = get_matchups_by_subject(subject, facility_id)

  # list of all users who are manually added to the unassigned pool.
  fixed_unassigned_pool = get_users_in_unassignment_pool(facility_id, subject)
  
  # Current count of pairs assigned to each supervisor
  pairs_count_by_supervisor = matchups_count_by_supervisors(existing_matchups, supervisors)

  # prepare the data for matchup processing. 
  incomplete_matchups, unassigned_mentees, unassigned_mentors = get_data_for_matchup(existing_matchups, mentees, mentors)
  process( 
    subject,
    facility_id,
    supervisors,
    max_pairs_per_supervisor,
    pairs_count_by_supervisor,
    incomplete_matchups,
    unassigned_mentees,
    unassigned_mentors,
    fixed_unassigned_pool
  )

def process(subject, 
    facility_id,
    supervisors,
    max_pairs_per_supervisor,
    pairs_count_by_supervisor,
    incomplete_matchups,
    unassigned_mentees,
    unassigned_mentors,
    fixed_unassigned_pool):
  print("Processing matchups.")

  #process the existing incomplete matchups first
  for item in incomplete_matchups:
    if item['mentee_id'] is None:
      print(unassigned_mentees)
      available_mentee = get_next_available_mentee(fixed_unassigned_pool, unassigned_mentees)
      print(unassigned_mentees)
      if available_mentee is None:
        continue
      item['mentee_id'] = available_mentee['id']
      item['mentee_name'] = available_mentee['full_name']
    if item['mentor_id'] is None:
      available_mentor = get_next_available_mentor(fixed_unassigned_pool, unassigned_mentors, item['mentee_id'])
      if available_mentor is None:
        continue
      item['mentor_id'] = available_mentor['id']
      item['mentor_name'] = available_mentor['full_name']
    if item['supervisor_id'] is None:
      available_supervisor = get_supervisor(max_pairs_per_supervisor, pairs_count_by_supervisor, supervisors)
      if available_supervisor is None:
        continue
      item['supervisor_id'] = available_supervisor['id']
      item['supervisor_name'] = available_supervisor['full_name']

  new_matchups = []
  #Process the remaining unassigned mentees.
  #No new incomplete matchup are to be created. 
  for mentee in unassigned_mentees:
    if is_user_in_fixed_unassigned_pool(fixed_unassigned_pool, 'mentees', mentee['id']):
      continue
    available_mentor = get_next_available_mentor(fixed_unassigned_pool, unassigned_mentors, mentee['id'])
    #Ensures that a matchup is created only when mentor  is available
    if available_mentor is None:
      print("No more mentor available for one to one pairing.")
      break
    #Ensures that a matchup is created only when supervisor is available
    available_supervisor = get_supervisor(max_pairs_per_supervisor, pairs_count_by_supervisor, supervisors)
    if available_supervisor is None:
      print("No more supervisors available.")
      break

    matchup = MatchUpDetails(
      subject = subject,
      facility_id = facility_id,
      mentee_id =  mentee['id'],
      mentee_name = mentee['full_name'],
      mentor_id = available_mentor['id'],
      mentor_name = available_mentor['full_name'],
      supervisor_id = available_supervisor['id'],
      supervisor_name = available_supervisor['full_name'])
    new_matchups.append(matchup)  
  update_db(incomplete_matchups, new_matchups)  
  print("Finished processing matchups.")    

@transaction.atomic
def update_db(existing_matchups, new_matchups):
  for matchup in existing_matchups:
    MatchUpDetails.objects.filter(id = matchup['id']).update(
      mentee_id = matchup['mentee_id'],
      mentee_name = matchup['mentee_name'],
      mentor_id = matchup['mentor_id'],
      mentor_name = matchup['mentor_name'],
      supervisor_id = matchup['supervisor_id'],
      supervisor_name = matchup['supervisor_name']
    )
  for matchup in new_matchups:
    matchup.save()


def get_learners_by_subject(subject, facility_id):
  classroom_queryset = Classroom.objects.filter(name__iregex=r'^' + re.escape(subject) + '\s[0-9]+$', 
  parent_id = facility_id).values_list('id', flat=True)
  classrooms = list(classroom_queryset)
  learners_queryset = FacilityUser.objects.filter(Q(memberships__collection__in=classrooms)).distinct().values(
        "id",
        "username",
        "full_name",
        "memberships__collection__id",
        "memberships__collection__name"
    )
  learners = [learner for learner in learners_queryset] 
  return learners


def split_learners(learners):
  number_of_learners = len(learners)
  if number_of_learners == 1:
    return ([], learners)
  middle_index = number_of_learners//2
  mentors = learners[:middle_index]
  mentees = learners[middle_index:]
  return (mentors, mentees)

def get_matchups_by_subject(subject, facility_id):
  queryset = MatchUpDetails.objects.filter(
            subject = subject, facility_id=facility_id, keepUnassigned = False).distinct().values(
                "id",
                "mentee_id",
                "mentee_name",
                "mentor_id",
                "mentor_name",
                "subject",
                "supervisor_id",
                "supervisor_name",
                "facility_id"
            )
  matchups = [matchup for matchup in queryset]
  return matchups        


def get_optimal_pairs_per_supervisor(no_of_mentees, no_of_supervisors):
  if no_of_supervisors == 0 or no_of_mentees == 0:
    return 0
  if no_of_mentees < no_of_supervisors:
    return 1
  count = no_of_mentees/no_of_supervisors
  return min(math.ceil(count), MAX_PAIRS_PER_COACH)


def matchups_count_by_supervisors(existing_matchups, supervisors):
  result = []
  for supervisor in supervisors:
    result.append({
      'id' : supervisor['id'],
      'count' : 0
    })

  for matchup in existing_matchups:
    supervisor_id = matchup['supervisor_id']
    if supervisor_id is not None:
      increment_matchups_count_for_supervisor(supervisor_id, pairs_count_by_supervisor=result)
  return result  


def increment_matchups_count_for_supervisor(supervisor_id, pairs_count_by_supervisor):
  for item in pairs_count_by_supervisor:
    if item['id'] == supervisor_id:
      item['count'] += 1
      return

def get_data_for_matchup(existing_matchups, mentees, mentors):
  # matchups which has either supervisor or mentor or mentee missing
  # Ideally, only mentee can be missing from a matchup. 
  # Nonetheless, we process all incomplete matchups to ensure a matchup is always complete
  incomplete_matchups = []  
  for matchup in existing_matchups:
    mentee_id = matchup['mentee_id']
    mentor_id = matchup['mentor_id']
    supervisor_id = matchup['supervisor_id']
    if mentee_id is None or mentor_id is None or supervisor_id is None:
      incomplete_matchups.append(matchup)
    if mentee_id:
      remove_item_from_list(mentee_id, mentees)
    if mentor_id:
      remove_item_from_list(mentor_id, mentors)  

  return (incomplete_matchups, mentees, mentors)      


def remove_item_from_list(id, list):  
  for index, item in enumerate(list):
    if item['id']  ==  id:
      list.pop(index)
      break

def get_supervisor(max_pairs_per_supervisor, pairs_count_by_supervisor, supervisors):    
  supervisor = next_available_supervisor(max_pairs_per_supervisor, pairs_count_by_supervisor, supervisors)
  pairs_count_by_supervisor.sort(key=lambda x:x.get('count'))
  return supervisor


def next_available_supervisor(max_pairs_per_supervisor, pairs_count_by_supervisor, supervisors):  
  for item in pairs_count_by_supervisor:
    if item['count'] < max_pairs_per_supervisor:
      item['count'] += 1
      for supervisor in supervisors:
        if supervisor['id'] == item['id']:
          return supervisor          


def remove_any_matchup_with_null_mentee(subject, facility_id, supervisor_id, mentor_id):
  MatchUpDetails.objects.filter(facility_id = facility_id,
  subject = subject,
  supervisor_id = supervisor_id,
  mentor_id = mentor_id,
  mentee_id__isnull = True).delete()  


# Removes all matchups for users in the unassigned pool.
# Also, adds a row for user who are manually added to unassigned pool
# so that those users are ignored during automated reassignment
def update_unassigned_pool(request, facility_id, subject):
  unassigned_pool = None if 'unassigned_pool' not in request else request['unassigned_pool']
  if unassigned_pool is not None:
    for item in unassigned_pool['mentee_list']: 
      MatchUpDetails.objects.filter(
        facility_id = facility_id,
        subject = subject,
        mentee_id = item['id']).delete()  
      if 'keepUnassigned' in item and item['keepUnassigned'] == True:
          MatchUpDetails.objects.create(
            facility_id = facility_id,
            subject = subject,
            keepUnassigned = True,
            mentee_id = item['id'],
            mentee_name = item['name']
          )
    for item in unassigned_pool['mentor_list']: 
      MatchUpDetails.objects.filter(
        facility_id = facility_id,
        subject = subject,
        mentor_id = item['id']).delete()  
      if 'keepUnassigned' in item and item['keepUnassigned'] == True:
          MatchUpDetails.objects.create(
            facility_id = facility_id,
            subject = subject,
            keepUnassigned = True,
            mentor_id = item['id'],
            mentor_name = item['name']
          )  
    for item in unassigned_pool['supervisor_list']: 
      MatchUpDetails.objects.filter(
        facility_id = facility_id,
        subject = subject,
        supervisor_id = item['id']).delete()  
      if 'keepUnassigned' in item and item['keepUnassigned'] == True:
          MatchUpDetails.objects.create(
            facility_id = facility_id,
            subject = subject,
            keepUnassigned = True,
            supervisor_id = item['id'],
            supervisor_name = item['name']
          )

# list of users which were manually added to the unassignment pool
def get_users_in_unassignment_pool(facility_id, subject):
  users_queryset = MatchUpDetails.objects.filter(
    facility_id = facility_id,
    subject = subject,
    keepUnassigned = True
  ).distinct().values(
    'mentee_id',
    'mentor_id',
    'supervisor_id'
  )
  mentees = []
  mentors = []
  supervisors = [] 
  for item in users_queryset:
    if item['mentee_id'] is not None:
      mentees.append(item['mentee_id'])
    if item['mentor_id'] is not None:
      mentors.append(item['mentor_id'])  
    if item['supervisor_id'] is not None:
      supervisors.append(item['supervisor_id'])  
  result = {
    'mentees' : mentees,
    'mentors' : mentors,
    'supervisors' : supervisors
  }    
  return result


def get_next_available_mentee(fixed_unassigned_pool, unassigned_mentees):
  if unassigned_mentees is None or len(unassigned_mentees) == 0:
    return None
  for mentee in unassigned_mentees:
    if is_user_in_fixed_unassigned_pool(fixed_unassigned_pool, 'mentees', mentee['id']) == False:
      unassigned_mentees.remove(mentee)
      return mentee
  return None    

def get_next_available_mentor(fixed_unassigned_pool, unassigned_mentors, mentee_id):
  if unassigned_mentors is None or len(unassigned_mentors) == 0:
    return None
  for mentor in unassigned_mentors:
    if is_user_in_fixed_unassigned_pool(fixed_unassigned_pool, 'mentors', mentor['id']) == False and mentor['id'] != mentee_id:
      unassigned_mentors.remove(mentor)
      return mentor
  return None 
       

def is_user_in_fixed_unassigned_pool(fixed_unassigned_pool, user_type, user_id):
  if fixed_unassigned_pool is not None:
    unassigned_list =  fixed_unassigned_pool[user_type]
    if unassigned_list is not None and len(unassigned_list) > 0:
      if user_id in unassigned_list:
        return True

  return False        
 
