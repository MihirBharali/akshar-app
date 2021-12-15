from datetime import date
from enum import Enum, unique
from django.db import models
from django.utils.translation import gettext as _
from morango.models import UUIDField


from kolibri.core.auth.models import FacilityUser
from kolibri.core.fields import DateTimeTzField
from kolibri.utils.time_utils import local_now

class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class UserType(Enum):
    LEARNER = "learner"
    COACH = "coach"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)

class TransactionStatus(Enum):
    CREATED = "created"
    COACH_APPROVED = "coach_approved"
    COACH_DENIED = "coach_denied"
    COMPLETED = "completed"
    DENIED = "denied"
    DENIED_INSUFFICIENT_FUND = "denied_insufficient_fund"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class UserWageAccount(models.Model):

    # Morango syncing settings
    morango_model_name = "userWageAccount"
    #the owner of the account
    user = models.ForeignKey(FacilityUser, unique=True, blank=False, null=False)
    #the timestamp when owner had last interaction with the account
    last_interaction_timestamp = DateTimeTzField(null=True, blank=True, default=local_now)
    #amount that the user has currently
    amount_available = models.FloatField(default=0)
    #the type of the user - learner, coach or admin
    userType = models.CharField(max_length=25, choices=UserType.choices(), blank = False)


class UserWageTransactions(models.Model):
    #Morango syncing settings
    morango_model_name = "userWageTransaction"
    id = (
        models.AutoField(
            auto_created=True, primary_key=True, serialize=True, verbose_name="ID"
        ),
    ) 
    #the user for whom the request is raised
    user_id = UUIDField(null=False, unique=False)
    #the name of the user for whom the request is raised
    user_name =  models.CharField(null=False, max_length=200)
    #the timestamp when transaction was created
    created_timestamp = models.DateTimeField(null=False, blank=True, default=local_now)
    #the date of transaction
    transaction_date = models.DateField(_("Date"), default=date.today, null=False)
    #the user who raised the transaction request
    created_by_id = UUIDField(null=False, unique=False)
    #the name of the user who raised the transaction request
    created_by_name = models.CharField(null=False, max_length=200)
    #the coach who approved the transaction
    coach_approver_id = UUIDField(null=True, unique=False)
    #the name of the coach who approved the transaction
    coach_approver_name = models.CharField(null=True, max_length=200)
    #the admin who approved the transaction
    admin_approver_id = UUIDField(null=True, unique=False)
    #the name of the admin who approved the transaction
    admin_approver_name = models.CharField(null=True, max_length=200)
    #the amount involved in the transaction
    transaction_amount = models.FloatField(default=0, null=False)
    #the balance available at the start of the transaction
    before_balance = models.FloatField(default=0, null=False)
    #the balance available when the transaction was completed
    after_balance = models.FloatField(default=0, null=True)
    #the type 0f request - credit or debit
    request_type = models.CharField(max_length=25, choices=TransactionType.choices(), blank = False)
    #reason for the transaction - mentoring, penalty etc
    reason = models.CharField(max_length=200, null=False)
    #status of the transaction
    status = models.CharField(max_length=25, choices=TransactionStatus.choices(), blank = False)
    #additional description regarding the transaction
    description = models.CharField(max_length=500, null=True, blank=True)

