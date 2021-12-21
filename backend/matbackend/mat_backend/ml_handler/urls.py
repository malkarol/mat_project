from django.urls import path
from ml_handler import views


urlpatterns=[
    path('mlmodels/',views.ml_models_list),
    # path('user/<int:pk>',views.user_details)
]