from django.db.models import fields
from kolibri.core.serializers import KolibriModelSerializer
from .models import UserWageAccount, UserWageTransactions

class UserWageAccountSerializer(KolibriModelSerializer):
    class Meta:
        model = UserWageAccount
        fields = (
            "user",
            "userType",
            "last_interaction_timestamp",
            "amount_available",
        )


class UserWageAccountTransactionSerializer(KolibriModelSerializer):
    class Meta:
        model = UserWageTransactions
        fields = (
            "id",
            "user_id",
            "user_name",
            "created_by_id",
            "created_by_name",
            "created_timestamp",
            "transaction_date",
            "coach_approver_id",
            "coach_approver_name",
            "admin_approver_id",
            "admin_approver_name",
            "transaction_amount",
            "before_balance",
            "after_balance",
            "request_type",
            "reason",
            "status",
            "description",
        )        