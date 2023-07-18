from django.urls import path
from .views import *


urlpatterns = [
    path('add_task/', AssigneTask.as_view()),
    path('one_task/<pk>/', TaskAPIVeiw.as_view()),
    path('all_task/', AllTask.as_view()),
    path("response_task/<pk>/", TaskResponse.as_view()),
    path('problem_task/<pk>/', TaskProblem.as_view()),
    path('participant_task/', ParticipantTask.as_view(),),
    path('assigner_task/', AssignerTask.as_view(),),
    path('comment/<pk>/', TaskComment.as_view()),
    path('comment/change/<pk>/', CommentView.as_view())

]
