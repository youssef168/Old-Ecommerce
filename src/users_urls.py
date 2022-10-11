from django.urls import path
from .users_view import *

urlpatterns = [
    path('', get_users, name="register"),
    path('register/', register_view, name="register"),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('search/<str:name>/', search_users, name='search_users'),
    path('getby-id/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('profile/', get_user_profile, name="get_user_profile"),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('login/', MyTokenObainPairView.as_view(), name='login'),
    path('update-profile/', update_user_profile, name='update_user_profile')
]