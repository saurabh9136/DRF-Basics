from django.urls import path, include
from home.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User

router = DefaultRouter()
router.register(r'person', PeopleViewSet, basename=person)
urlpatterns = router.urls

urlpatterns = [
    # path('', include(router.urls)),
    path('index/', index),
    path('person/', person),
    path('login1/', login ),
    path('register/', RegisterAPI.as_view() ),
    path('login/', LoginAPI.as_view()),
    path('persons/', PersonAPI.as_view()),
    path('person-modelviewset/', include(router.urls))
]
