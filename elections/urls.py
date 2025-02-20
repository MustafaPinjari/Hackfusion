from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.election_list, name='list'),
    path('create/', views.election_create, name='create'),
    path('<int:pk>/', views.election_detail, name='detail'),
    path('<int:election_id>/submit_nomination/', views.submit_nomination, name='submit_nomination'),
    path('nominations/manage/', views.manage_nominations, name='manage_nominations'),
    path('nominations/<int:nomination_id>/review/', views.review_nomination, name='review_nomination'),
    path('<int:election_id>/register/', views.register_candidate, name='register_candidate'),
    path('<int:election_id>/vote/<int:candidate_id>/', views.submit_vote, name='vote'),
    path('<int:election_id>/delete/', views.delete_election, name='delete'),
    path('<int:election_id>/edit/', views.edit_election, name='edit'),
]