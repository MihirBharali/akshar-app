from ..models import MatchUpDetails

def get_matchup_for_coach(user_id):
    match_ups = MatchUpDetails.objects.filter(supervisor_id = user_id).distinct().values(
                "mentee_id",
                "mentee_name",
                "mentor_id",
                "mentor_name",
                "subject",
                "supervisor_id",
                "supervisor_name",
                "facility_id"
            )

    '''
       Group the matchups by subject
    '''        
    match_up_by_subjects = {}
    for match_up in match_ups:
        subject = match_up['subject']
        if subject not in match_up_by_subjects:
            match_up_by_subjects[subject] = []
        match_up_by_subjects[subject].append(match_up)
    
    response = {}
    match_up_details = []
     
    '''
       Iterate over each subject and corresponding pairs
       and convert to response object
    ''' 
    for subject, pairs in match_up_by_subjects.items():
        match_up_pairs = []
        for pair in pairs:
            match_up_pairs.append({
                'mentor': {
                    'id': pair['mentor_id'],
                    'name': pair['mentor_name']
                },
                "mentee": {
                    'id': pair['mentee_id'],
                    'name': pair['mentee_name']
                }
            })
        match_up_details.append({
            'subject': subject,
            'pairs': match_up_pairs
        })    
    
    response = {
        'match_up_details': match_up_details
    }
     
    print(response)
    return response