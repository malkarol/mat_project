from django.urls import path
from account import views
from session_handler import views as sessions_view


urlpatterns=[
    path('users/',views.users_list),
    path('user/<str:email>',views.user_details),
    path('sessions/',sessions_view.sessions_list)
    # path('user/<int:pk>',views.user_details)
]