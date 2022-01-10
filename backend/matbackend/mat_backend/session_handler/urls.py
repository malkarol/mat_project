from django.urls import path
from session_handler import views


urlpatterns=[
    path('sessions/',views.sessions_list),
    path('session/<int:pk>',views.session_detail),
    path('participants/',views.participants_list),
    path('participant/<int:pk>',views.participant_detail),
    path('upload/', views.storage_files_view),
    path('download/<int:pk>', views.storage_file_detail),
    path('generate-local-model/', views.local_model_detail),

    path('create-filled-session/', views.add_many_participants),
    # join session
    path('join-session/', views.join_session),
    # check in which sessions user is
    path('participants/filter/<int:pk>', views.get_joined_sessions),
    path('session/<int:spk>/participant/<int:ppk>', views.participant_for_session),
    # return list of usernames for a single sessint
    path('participants/session/<int:pk>', views.get_participants_for_session),
    path('validateprivatekey', views.validate_private_key),
    path('mysessions/<str:name>', views.get_managed_sessions)
    # add session and participants with filed usernames
    # path('sessions/add-filled/', views.add_filled_session),
    # path('user/<int:pk>',views.user_details)
]
