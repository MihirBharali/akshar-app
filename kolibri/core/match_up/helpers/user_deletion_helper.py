from django.db.models import Q

from ..models import MatchUpDetails


def update_matchup(user_id, facility_id):
    remove_user_from_matchup(user_id, facility_id)
            
def remove_user_from_matchup(user_id, facility_id):
    queryset = get_matchups_for_user(user_id, facility_id)
    print(queryset)
    MatchUpDetails.objects.filter(id__in = queryset).delete()


def get_matchups_for_user(user_id, facility_id):
    return MatchUpDetails.objects.filter(Q(facility_id = facility_id) &
            (Q(mentee_id = user_id) 
            | Q(mentor_id = user_id) 
            | Q(supervisor_id = user_id))).only('id').all()