from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status

from kolibri.core.auth.models import FacilityUser, Classroom
from kolibri.core.auth.constants import role_kinds
from kolibri.core.auth.models import Collection
from kolibri.core.mixins import BulkCreateMixin
from kolibri.plugins import user

from .models import UserWageAccount, UserWageTransactions
from .serializer import UserWageAccountSerializer, UserWageAccountTransactionSerializer

class UserWageAccountViewset(
    CreateModelMixin, 
    RetrieveModelMixin, 
    DestroyModelMixin, 
    UpdateModelMixin, 
    ListModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserWageAccount.objects.all()
    serializer_class = UserWageAccountSerializer
    lookup_field = 'user'

    def create(self, request, *args, **kwargs):
        user_id = request.data['user']
        type = request.data['userType']
        facility_user =  FacilityUser.objects.filter(id = user_id)
        if facility_user is None or len(facility_user) == 0:
            return Response('User not found in facility', status.HTTP_404_NOT_FOUND)
        UserWageAccount.objects.create(
            user = facility_user[0],
            userType = type
        )    
        response = {
            'id': user_id,
            'user': user_id,
            'amount_available': 0.0,
            'userType': 'learner'
        }
        return Response(response, status.HTTP_201_CREATED)

    def retrieve(self, request, user, *args, **kwargs):
        fetch_transaction = request.GET.get("getTransactions")
        fetch_supervisors = request.GET.get("getSupervisors")
        account = UserWageAccount.objects.filter(user_id = user).distinct().values(
            'user',
            'last_interaction_timestamp',
            'amount_available',
            'userType'
        )
        if account is None or len(account) == 0:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        result = account[0]
        if fetch_transaction == 'true':
            txns = UserWageTransactions.objects.filter(user_id = user).distinct().values(
                "id",
                "user_id",
                "user_name",
                "created_by_id",
                "created_by_name",
                "created_timestamp",
                'transaction_date',
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
            if txns is not None:
                result['transactions'] = txns
        if fetch_supervisors == 'true':
            facility_id = request.GET.get("facility")
            supervisors = self.get_supervisors(facility_id) 
            result['supervisors'] = supervisors       

        return  Response(result, status=status.HTTP_200_OK) 
    
    # Gets all the supervisors in the facility
    def get_supervisors(self, facility_id):
        supervisors_queryset = FacilityUser.objects.filter(roles__kind__in = ['coach', 'classroom assignable coach'], facility_id =  facility_id).distinct().values(
            "id",
            "full_name"
            )
        supervisors = [supervisor for supervisor in supervisors_queryset]
        return supervisors
class UserWageAccountTransactionViewset(
    CreateModelMixin, 
    ListModelMixin,
    RetrieveModelMixin, 
    DestroyModelMixin, 
    UpdateModelMixin, 
    BulkCreateMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserWageTransactions.objects.all()
    serializer_class = UserWageAccountTransactionSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = [
        'created_by_id',
        'transaction_date',
        'coach_approver_id', 
        'admin_approver_id', 
        'reason', 
        'request_type', 
        'status']

    CANCELLED_STATUS = ['COACH_DENIED', 'DENIED']

    def list(self, request, *args, **kwargs):
        role = request.GET.get('role')
        type = request.GET.get('type')
        if role is not None and role == 'Coach':
            return self.get_transactions_for_coach(request)
        if role is not None and role == 'Admin':
            return self.get_transactions_for_facility(request)    
        if type is not None and type == 'Reporting':
            return self.get_transactions_for_reporting(request)        
        return super().list(request, *args, **kwargs)    


    def get_transactions_for_facility(self, request):
        is_an_admin = self.is_an_admin(request)
        if is_an_admin == False:
            return Response('Not authorised', status=status.HTTP_403_FORBIDDEN) 
        txns = UserWageTransactions.objects.filter(status = 'COACH_APPROVED').distinct().values(
                "id",
                "user_id",
                "user_name",
                "created_by_id",
                "created_by_name",
                "created_timestamp",
                'transaction_date',
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
        return Response(txns, status=status.HTTP_200_OK)

    def get_transactions_for_coach(self, request):
        txns = UserWageTransactions.objects.filter((Q(coach_approver_id = request.user.id) & Q(status='CREATED')) | Q(created_by_id=request.user.id)).distinct().values(
                "id",
                "user_id",
                "user_name",
                "created_by_id",
                "created_by_name",
                "created_timestamp",
                'transaction_date',
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
        return Response(txns, status=status.HTTP_200_OK)    

    def get_transactions_for_reporting(self, request):
        is_an_admin = self.is_an_admin(request)
        if is_an_admin == False:
            return Response('Not authorised', status=status.HTTP_403_FORBIDDEN) 
        date_range_start = request.GET.get('startDate')    
        date_range_end = request.GET.get('endDate')   
        requestStatus = request.GET.get('status')
        txns = UserWageTransactions.objects.filter(Q(transaction_date__range=[date_range_start, date_range_end]) & Q(status=requestStatus)).distinct().values(
                "id",
                "user_id",
                "user_name",
                "created_by_id",
                "created_by_name",
                "created_timestamp",
                'transaction_date',
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
        return Response(txns, status=status.HTTP_200_OK)  



    @transaction.atomic 
    def create(self, request):
        #handle bulk create request which is used to do bulk update
        isBulkUpdate = request.GET.get('isBulkUpdate')
        if isBulkUpdate is not None and isBulkUpdate == 'true':
            return self.handle_bulk_update(request)
        
        #validate and create transactions
        role = request.GET.get('role')
        isCoach = False
        isAdmin = False
        request_status = 'CREATED'
        if role is not None:
            if role == 'Coach':
                isCoach = self.is_a_coach(request)    
                request_status = 'COACH_APPROVED'
            if role == 'Admin':
                isAdmin = self.is_an_admin(request)    
                request_status = 'COMPLETED'    

        creator_id = request.user.id
        creator_name = request.user.full_name
        user_id = request.data['user_id']
        transaction_amount = float(request.data['transaction_amount'])
        request_type = request.data['request_type']
        reason = request.data['reason']
        description = None if 'description' not in request.data else request.data['description']
        coach_id = None if 'coach_approver_id' not in request.data else request.data['coach_approver_id']
        coach_name = None if 'coach_approver_name' not in request.data else request.data['coach_approver_name']
        user_wage_account = UserWageAccount.objects.filter(user_id = user_id).distinct().values(
            'user',
            'amount_available',
            'user__full_name'
        )
        amount_available = 0.0
        user_name = None
        if user_wage_account is None or len(user_wage_account) == 0:
            print('Coudnt find user wage account')
            facility_user_queryset = FacilityUser.objects.filter(id = user_id)
            if facility_user_queryset is None or len(facility_user_queryset) == 0:
                return Response('Facility user not found.', status=status.HTTP_404_NOT_FOUND)
            else:
                print("Creating a wage account for the user.")
                UserWageAccount.objects.create(
                    user = facility_user_queryset[0],
                    userType = 'LEARNER'
                    )
                user_name = facility_user_queryset[0].full_name
        else:
            amount_available = user_wage_account[0]['amount_available']
            user_name = user_wage_account[0]['user__full_name']

        # if the request is approved, calculated after balance  
        after_balance = None       
        if request_status == 'COMPLETED' and isAdmin:
            if request_type == 'DEBIT':
                print('Deducting amount')
                after_balance = amount_available - transaction_amount
            if request_type == 'CREDIT':   
                print('Adding amount')
                after_balance = amount_available + transaction_amount    
        
        (obj, isSuccess) = UserWageTransactions.objects.update_or_create(
            user_id = user_id,
            user_name = user_name,
            created_by_id = creator_id,
            created_by_name = creator_name,
            coach_approver_id = creator_id if isCoach or isAdmin else coach_id,
            coach_approver_name = creator_name if isCoach or isAdmin else coach_name,
            admin_approver_id = creator_id if isAdmin else None,
            admin_approver_name = creator_name if isAdmin else None,
            transaction_amount = transaction_amount,
            before_balance = amount_available,
            after_balance = after_balance,
            request_type = request_type,
            reason = reason,
            status = request_status,
            description = description,

        )
        if request_status == 'COMPLETED':
            UserWageAccount.objects.filter(user__id = user_id).update(
                amount_available = after_balance
                )   
        return Response(self.serialise(obj), status=status.HTTP_201_CREATED)

    def serialise(self, instance):
        return { 
                "id": instance.id,
                "user_id": instance.user_id,
                "user_name": instance.user_name,
                "created_by_id": instance.created_by_id,
                "created_by_name": instance.created_by_name,
                "created_timestamp": instance.created_timestamp,
                "transaction_date": instance.transaction_date,
                "coach_approver_id": instance.coach_approver_id,
                "coach_approver_name": instance.coach_approver_name,
                "admin_approver_id": instance.admin_approver_id,
                "admin_approver_name": instance.admin_approver_name,
                "transaction_amount": instance.transaction_amount,
                "before_balance": instance.before_balance,
                "after_balance": instance.after_balance,
                "request_type": instance.request_type,
                "reason": instance.reason,
                "status": instance.status,
                "description": instance.description,
        }    

    def update(self, request, pk):
        print("Received a update request")
        instance = self.queryset.get(pk=pk)
        #validate request to ensure that txn is processed correctly
        user_id = self.request.data['user_id']
        if user_id != instance.user_id:
            return Response('Invalid user_id in request', status=status.HTTP_400_BAD_REQUEST) 
        txn_status = self.request.data['status']
        if instance.status == txn_status:
            return Response('Database already updated with the same status', status=status.HTTP_400_BAD_REQUEST)    
        if instance.status == 'COMPLETED':
            return Response('Transaction already settled', status=status.HTTP_400_BAD_REQUEST)      
        request_type = self.request.data['request_type']
        if request_type != instance.request_type:
            return Response('Request type mismatch', status=status.HTTP_400_BAD_REQUEST)   

        #get user wage details
        user_wage_account = UserWageAccount.objects.filter(user_id = user_id).distinct().values(
                'amount_available')
        transaction_amount = self.request.data['transaction_amount']       
        before_balance = user_wage_account[0]['amount_available']        
        after_balance = 0
        # if the request is approved, calculated after balance         
        if txn_status == 'COMPLETED':
            if request_type == 'DEBIT':
                print('Deducting amount')
                after_balance = before_balance - transaction_amount
            if request_type == 'CREDIT':   
                print('Adding amount')
                after_balance = before_balance + transaction_amount
        #update all tables with correct statuses and balances        
        self.update_user_account(pk, self.request.data, after_balance, before_balance, txn_status)     
        return Response('Request successfully updated', status=status.HTTP_200_OK)
    
    @transaction.atomic
    def update_user_account(self, id, request, after_amount, before_amount, txn_status):
        UserWageTransactions.objects.filter(id = id).update(
            coach_approver_id = request['coach_approver_id'],
            coach_approver_name = request['coach_approver_name'],
            admin_approver_id = None if 'admin_approver_id' not in request else request['admin_approver_id'],
            admin_approver_name = None if 'admin_approver_name' not in request else request['admin_approver_name'],
            status = txn_status,
            before_balance = before_amount,
            after_balance = after_amount
        )  
        if txn_status == 'COMPLETED':
            facility_user = FacilityUser.objects.filter(id = request['user_id'])
            print(facility_user)
            UserWageAccount.objects.filter(user__id = request['user_id']).update(
                amount_available = after_amount
                )
   

    def create_wage_account(self, facility_user_queryset):

        UserWageAccount.objects.create(
            user = facility_user_queryset[0],
            amount_available = 0.0,
            userType = 'learner',
        ) 
   
    def get_facility_user(self, user_id):
        return FacilityUser.objects.filter(id = user_id).values('full_name')

    def has_permission(self, request):
        id = request.GET.get('facility')
        allowed_roles = [role_kinds.ADMIN, role_kinds.COACH]

        try:
            return request.user.has_role_for(
                allowed_roles, Collection.objects.get(pk=id)
            )
        except (Collection.DoesNotExist, ValueError):
            return False    

    def is_an_admin(self, request):
        id = request.GET.get('facility')
        allowed_roles = [role_kinds.ADMIN]

        try:
            return request.user.has_role_for(
                allowed_roles, Collection.objects.get(pk=id)
            )
        except (Collection.DoesNotExist, ValueError):
            return False     

    def is_a_coach(self, request):
        id = request.GET.get('facility')
        allowed_roles = [role_kinds.COACH, role_kinds.ASSIGNABLE_COACH]
        try:
            return request.user.has_role_for(
                allowed_roles, Collection.objects.get(pk=id)
            )
        except (Collection.DoesNotExist, ValueError):
            return False                 

    @transaction.atomic
    def handle_bulk_update(self, request):  
        isAuthorised = self.has_permission(request)
       # if isAuthorised == False:
       #    return Response('Not authorised', status=status.HTTP_403_FORBIDDEN)

        data = request.data  
        for val in data: 
            id = data[val]['id']
            self._perform_update(data[val], id)
        return Response(request.data, status=status.HTTP_200_OK)

    def _perform_update(self, request, pk):
        instance = self.queryset.get(pk=pk)
        #validate request to ensure that txn is processed correctly
        print(request)
        user_id = request['user_id']
        if user_id != instance.user_id:
            return Response('Invalid user_id in request', status=status.HTTP_400_BAD_REQUEST) 
        txn_status = request['status']
        if instance.status == txn_status:
            return Response('Database already updated with the same status', status=status.HTTP_400_BAD_REQUEST)    
        if instance.status == 'COMPLETED':
            return Response('Transaction already settled', status=status.HTTP_400_BAD_REQUEST)      
        request_type = request['request_type']
        if request_type != instance.request_type:
            return Response('Request type mismatch', status=status.HTTP_400_BAD_REQUEST)   

        #get user wage details
        user_wage_account = UserWageAccount.objects.filter(user_id = user_id).distinct().values(
                'amount_available')
        transaction_amount = request['transaction_amount'] 
        before_balance = user_wage_account[0]['amount_available']        
        after_balance = 0 
        # if the request is approved, calculated after balance         
        if txn_status == 'COMPLETED':
            if request_type == 'DEBIT':
                print('Deducting amount')
                after_balance = before_balance - transaction_amount
            if request_type == 'CREDIT':   
                print('Adding amount')
                after_balance = before_balance + transaction_amount
        #update all tables with correct statuses and balances        
        self.update_user_account(pk, request, after_balance, before_balance, txn_status)   
