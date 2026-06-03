from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api_views
router = DefaultRouter()
router.register('tasks', api_views.TaskViewSet, basename='task')

urlpatterns = [
    #---------------------------------------------------------------------from function base
    # path('tasks/', api_views.tasks_api, name='api_task_list'),
    #  path('tasks/<int:pk>', api_views.tasks_details, name='api_task_list'),
    #---------------------------------------------------------------------from class base
     path('tasks/',api_views.TaskApiView.as_view(),name='api_classview'),
     path('tasks/<int:pk>/',api_views.TaskApiDetails.as_view(),name='api_classview')
    # path('', include(router.urls)), #viewset
]