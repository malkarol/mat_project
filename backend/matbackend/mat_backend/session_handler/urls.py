from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from session_handler import views

urlpatterns = [
    path('sessions/', views.sessions_list),

]

