from django.urls import path,include
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('task/<str:first_name>/<str:user_id>/<str:position>', task, name ='task'),
    path('search/<str:first_name>/<str:user_id>/<str:position>/<str:result>', search, name = 'search'),
    path('mechaniclist/<str:first_name>/<str:user_id>/<str:position>', mechaniclist, name='mechanic'),
    path('waitreview/<str:first_name>/<str:user_id>/<str:position>', waitreview, name='waitreview'),
    path('overdue/<str:first_name>/<str:user_id>/<str:position>', overdue, name='overdue'),
    path('mechanic/<str:first_name>/<str:user_id>/<str:position>', mechanic, name='mechanic'),
    path('mytask/<str:first_name>/<str:user_id>/<str:position>', mytask, name='mytask'),
    path('mytask_reviewed/<str:first_name>/<str:user_id>/<str:position>', mytask_reviewed, name='mytask_reviewed'),
    path('mytask_wait_review/<str:first_name>/<str:user_id>/<str:position>', mytask_wait_review, name='mytask_wait_review'),
    path('signout', signout, name = 'signout'),
    path('api-auth/', include('rest_framework.urls')),

]
