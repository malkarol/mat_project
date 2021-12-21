from django.urls import path
from session_handler import views


urlpatterns=[
    path('sessions/',views.sessions_list),
    path('participants/',views.participants_list),
    # path('user/<int:pk>',views.user_details)
]
