from django.urls import path
from session_handler import views


urlpatterns=[
    path('sessions/',views.sessions_list),
    path('session/<int:pk>',views.session_detail),
    path('participants/',views.participants_list),
    path('participant/<int:pk>',views.participant_detail),
    path('upload/', views.storage_files_view),
    path('download/<int:pk>', views.storage_file_detail),
    path('generate-local-model/', views.local_model_detail)

    # path('user/<int:pk>',views.user_details)
]
