from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers
from .api import AdminMatchUpViewset
from .api import CoachMatchUpViewset
from .api import LearnerMatchUpViewset

router = routers.SimpleRouter()
router.register(
    r"admin", AdminMatchUpViewset, base_name="match-up"
)

router.register(
    r"coach", CoachMatchUpViewset, base_name="match-up"
)
router.register(
    r"learner", LearnerMatchUpViewset, base_name="match-up"
)

urlpatterns = [url(
                  r"^", 
                  include(router.urls)
               ),
        ]