from django.urls import path
from ml_handler import views


urlpatterns=[
    path('mlmodels/',views.ml_models_list),
    path('mlmodel/<int:pk>',views.ml_model_detail)
    # path('user/<int:pk>',views.user_details)
]