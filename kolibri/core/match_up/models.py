from django.db import models
from morango.models import UUIDField
from kolibri.core.auth.constants import role_kinds
from kolibri.core.auth.permissions.base import RoleBasedPermissions
from kolibri.core.auth.constants.demographics import choices as GENDER_CHOICES


class MatchUpDetails(models.Model):
    # Morango syncing settings
    morango_model_name = "MatchUpDetails"
    permissions = (
        RoleBasedPermissions(
            target_field="collection",  
            can_be_created_by=(role_kinds.ADMIN),
            can_be_read_by=(role_kinds.ADMIN, role_kinds.COACH, role_kinds.ASSIGNABLE_COACH),
            can_be_updated_by=(role_kinds.ADMIN, role_kinds.COACH),
            can_be_deleted_by=(role_kinds.ADMIN, role_kinds.COACH),
        )
    )
    id = (
        models.AutoField(
            auto_created=True, primary_key=True, serialize=True, verbose_name="ID"
        ),
    )  
    
    #the facility User ID of the mentee
    mentee_id = UUIDField(null=True, unique=False)
    #the name of the mentee
    mentee_name = models.CharField(null=True, max_length=200)
    #the gender of the mentee
    mentee_gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES, default="", blank=True
    )
    #the physical facility's level of the mentee
    mentee_physical_facility_level = models.CharField(max_length=64, default="", blank=True, null=True)
    #the facility User ID of the mentor
    mentor_id = UUIDField(null=True, unique=False)
    #the name of the mentor
    mentor_name = models.CharField(max_length=200, null=True)
    #the gender of the mentor
    mentor_gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES, default="", blank=True
    )
    #the physical facility's level of the mentor
    mentor_physical_facility_level = models.CharField(max_length=64, default="", blank=True, null=True)
    #the subject for which mathc up is created
    subject = models.CharField(max_length=100)
    #the facility User ID of the supervisor
    supervisor_id = UUIDField(unique=False, null=True)
    #the name of the supervisor name
    supervisor_name = models.CharField(max_length=200, null=True)
    #the ID of the facility
    facility_id = UUIDField(null=False, unique=False)
    #if set true, the user will not be part of any matchup
    #in essence, the user is considered to belong to the fixed unassignment pool
    keepUnassigned = models.NullBooleanField(null=True, default=False)