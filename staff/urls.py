from django.urls import path
from .views import Profile_view, All_Team_view, PresentationView, EndTimeSet, ShowPersonalPresentation

urlpatterns = [
    path('all_profile/', Profile_view.as_view()),
    path('all_team/', All_Team_view.as_view()),
    path('presentation/', PresentationView.as_view()),
    path('end_time/<pk>/',EndTimeSet.as_view()),
    path('personal/', ShowPersonalPresentation.as_view())

]

