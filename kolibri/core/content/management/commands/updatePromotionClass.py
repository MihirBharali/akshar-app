from django.core.management.base import BaseCommand


from kolibri.core.auth.models import FacilityUser
from kolibri.core.promotion.models import PromotionQueue

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.update_classes()
    
    def update_classes(self):
        query_promotion = PromotionQueue.objects.all()
        promotion_data = self.serialize_promotions(query_promotion)
        for item in promotion_data:   
            user_queryset = FacilityUser.objects.filter(pk=item['learner_id'])
            user_data = self.serialize_user_data(user_queryset)
            print(user_data)
            if len(user_data) > 0:
                PromotionQueue.objects.filter(id = item['id']).update(classroom_name=user_data[0]['physical_facility_level'])
            else:
                PromotionQueue.objects.filter(id = item['id']).delete()      



    def serialize_promotions(self, queryset):
        return list(queryset.values(
            "id", 
            "learner_id", 
            "learner_name",
            "classroom_id",
            "classroom_name",
            "facility_id",
            "quiz_id",
            "quiz_name",
            "quiz_score",
            "lesson_completion",
            "promotion_status",
            "coach_approver",
            "admin_approver",
            "create_timestamp",
            "update_timestamp"))                  

    def serialize_user_data(self, queryset):
        return queryset.values("full_name", "physical_facility_level")            