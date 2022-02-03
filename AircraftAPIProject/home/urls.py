from django.urls import path
from .views import *
from knox import views as knox_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', home, name='home'),
    ################# API ################# API ################# API ################# API
    path('login',login_api,name='login_api'),
    path('user',get_user_data,name='get_user_data'),
    path('register',register_api,name='register_api'),
    path('task',get_task,name='get_task'),
    path('addtask',add_task,name='add_task'),
    path('look/<str:task>',look_task,name='look_task'),
    path('task/<int:id>',update_task,name='update_task'),
    path('myowntask',myowntask,name='myowntask'),
    path('myowntask_reviewed',myowntask_reviewed,name='myowntask_reviewed'),
    path('myowntask_wait_review',myowntask_wait_review,name='myowntask_wait_review'),
    path('task_over',get_task_over,name='get_task_over'),
    path('get_mechanic',get_mechanic,name='get_mechanic'),
    path('logout',csrf_exempt(knox_views.LogoutView.as_view())),
    path('logoutall',csrf_exempt(knox_views.LogoutAllView.as_view())),
    ################# API ################# API ################# API ################# API
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
]
