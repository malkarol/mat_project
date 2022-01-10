from django.urls import path
from session_handler import views


urlpatterns=[
    path('sessions/',views.sessions_list),
    path('session/<int:pk>',views.session_detail),
    path('participants/',views.participants_list),
    path('participant/<int:pk>',views.participant_detail),
    path('upload/', views.storage_files_view),
    path('download/<int:pk>', views.storage_file_detail),

    # generate local model script for session
    path('generate-local-model/', views.local_model_script),
     # generate global model script for session
    path('generate-global-model/', views.global_model_script),
     # generate aggregate script for session
    path('generate-local-model/', views.aggregate_script),

    path('create-filled-session/', views.add_many_participants),
    # join session
    path('join-session/', views.join_session),
    # check in which sessions user is
    path('participants/filter/<int:pk>', views.get_joined_sessions),
    # return list of usernames for a single sessint
    path('participants/session/<int:pk>', views.get_participants_for_session),
    # add session and participants with filed usernames
    # path('sessions/add-filled/', views.add_filled_session),
    # path('user/<int:pk>',views.user_details)
]
