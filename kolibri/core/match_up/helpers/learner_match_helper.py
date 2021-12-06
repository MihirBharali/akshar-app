from ..models import MatchUpDetails
from django.db.models import Q

def get_matchup_for_learner(user_id, facility_id):

    match_ups = get_matchups(user_id, facility_id)
    '''
      Group the matchups by subject
    '''
    match_up_by_subjects = {}
    for match_up in match_ups:
        subject = match_up['subject']
        if subject not in match_up_by_subjects:
            match_up_by_subjects[subject] = []
        match_up_by_subjects[subject].append(match_up)

    response = []
    for subject, pairs in match_up_by_subjects.items():
        isMentor = is_mentor(pairs, user_id)
        if isMentor:
            mentee_list = []
            for pair in pairs:
                mentee_list.append({
                    'name': pair['mentee_name'],
                    'id': pair['mentee_id']

                })
            output = {
                'subject': subject,
                'role': 'Mentor',
                'supervisor': {
                    'name': pairs[0]['supervisor_name'],
                    'id': pairs[0]['supervisor_id']

                },
                'mentee_list': mentee_list
            }
            response.append(output)    
        else:
            output = {
                'subject': subject,
                'role': 'Mentee',
                'supervisor': {
                    'name': pairs[0]['supervisor_name'],
                    'id': pairs[0]['supervisor_id']

                },
                'mentor': {
                    'name': pairs[0]['mentor_name'],
                    'id': pairs[0]['mentor_id']
                }
            }
            response.append(output)              
    return response


def is_mentor(pairs, user_id):
    if pairs[0]['mentor_id'] == user_id:
        return True
    return False        

def get_matchups(user_id, facility_id):
    return MatchUpDetails.objects.filter(
             Q(mentee_id = user_id, facility_id = facility_id, keepUnassigned = False) 
            | Q(mentor_id = user_id,facility_id = facility_id, keepUnassigned = False)).distinct().values(
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
   


