from django.urls import path
from .views import index, registration_view, logout_view,favourites, skill_match, home_user, download_project, toggle_favourite

urlpatterns = [
    path('skill-match/',skill_match,name='skill_match'),
    path('',index,name='index'), 
    path('registration-view/',registration_view,name='registration_view'), 
    path('logout-view/',logout_view,name='logout_view'), 
    path('favourites/',favourites, name='favourites'),
    path('home-user/',home_user,name='home_user'),
    path('download-project/<int:project_id>/', download_project, name='download_project'),
    path('toggle-favourite/', toggle_favourite, name='toggle_favourite')
]
