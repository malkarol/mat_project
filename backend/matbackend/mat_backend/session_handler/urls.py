from django.urls import path
from session_handler import views


urlpatterns=[
    path('sessions/',views.sessions_list),
    path('session/<int:pk>',views.session_detail),
    path('participants/',views.participants_list),
    path('participant/<int:pk>',views.participant_detail),
    path('upload/', views.storage_files_view),
    path('download/<int:pk>', views.storage_file_detail),

    path('generate-zip/<int:pk>',views.generate_zip),
    # upload global weights
    path('upload-initial-global-weights/', views.upload_initial_global_weights),
    path('upload-local-weights-json/', views.upload_local_weights_json),

    path('upload-local-results-json/', views.upload_local_results_json),
    # generate script for global weights
    path('generate-weights-script/<int:pk>', views.generate_global_weights),

    path('get-global-weights/<int:pk>', views.get_global_weights),
    # generate local model script for session
    path('upload-local-model/', views.upload_local_model),
    # generate local model script for session
    path('generate-local-model/<int:pk>', views.local_model_script),
    # generate global model script for session
    path('generate-global-model/<int:pk>', views.global_model_script),
     # generate aggregate script for session
    path('generate-aggregate-script/<int:pk>', views.aggregate_script),

    path('create-filled-session/', views.add_many_participants),
    # join session
    path('join-session/', views.join_session),
    path('getparameters/<str:name>', views.get_parameters_list_for_model),
    path('get-available-models/', views.get_available_models),
    # check in which sessions user is
    path('participants/filter/<int:pk>', views.get_joined_sessions),
    path('session/<int:spk>/participant/<int:ppk>', views.participant_for_session),
    # return list of usernames for a single sessint
    path('participants/session/<int:pk>', views.get_participants_for_session),

    path('validateprivatekey', views.validate_private_key),
    path('mysessions/<str:name>', views.get_managed_sessions),
    path('leavesession/<int:spk>', views.leave_session),
    path('getzip/<int:pk>', views.get_zip),
    path('testmodel/', views.test_model),
    path('participantstrainingprocess/<int:spk>', views.get_session_model_progress),
    # instructions
    path('instructions/lm/', views.get_instructions_local_model),
    path('results-for-chart/<int:pk>',views.get_results_for_participants)


    # add session and participants with filed usernames
    # path('sessions/add-filled/', views.add_filled_session),
    # path('user/<int:pk>',views.user_details)
]
