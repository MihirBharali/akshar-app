from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers
from .api import UserWageAccountViewset, UserWageAccountTransactionViewset

router = routers.SimpleRouter()
router.register(
    r"account", UserWageAccountViewset, base_name="account"
)
router.register(
    r"transactions", UserWageAccountTransactionViewset, base_name="transactions"
)

urlpatterns = [url(
                  r"^", 
                  include(router.urls)
               ),
        ]