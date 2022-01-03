from django.urls import path
from account import views


urlpatterns=[
    path('users/',views.users_list),
    path('user/<int:id>',views.user_details),
    # path('user/<int:pk>',views.user_details)
]