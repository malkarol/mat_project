from django.urls import path
from account import views


urlpatterns=[
    path('users/',views.users_list),
    path('user/<str:email>',views.user_details),
    # path('user/<int:pk>',views.user_details)
]