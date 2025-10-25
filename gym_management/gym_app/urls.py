from django.urls import path
from . import views

urlpatterns = [
    # ----------------- HOME -----------------
    path('', views.home, name='home'),

    # ----------------- LOGIN & LOGOUT -----------------
    path('user_login', views.user_login, name='user_login'),
    path('trainer_login', views.trainer_login, name='trainer_login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('logout', views.logout, name='logout'),

    # ----------------- REGISTRATION -----------------
    path('new_registration', views.new_registration, name='new_registration'),

    # ----------------- USER PORTAL -----------------
    path('user_portal', views.user_portal, name='user_portal'),
    path('request_trainer', views.request_trainer, name='request_trainer'),
    path('update_user_info', views.update_user_info, name='update_user_info'),
    path('change_password', views.change_password, name='change_password'),

    
    # Enhanced User Portal URLs
    path('workout_plan', views.workout_plan_detail_user, name='workout_plan'),
    path('diet_plan', views.diet_plan_detail_user, name='diet_plan'),
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),

    
    # ----------------- TRAINER PORTAL -----------------
    path('trainer/dashboard', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/clients', views.trainer_clients, name='trainer_clients'),
    path('trainer/assign_plan', views.assign_plan_to_member, name='assign_plan_to_member'),
    path('trainer/upload_profile_image/', views.upload_trainer_profile_image, name='upload_trainer_profile_image'),


    # Trainer workout plans
    path('trainer/create_workout_plan', views.create_workout_plan, name='create_workout_plan'),
    path('trainer/my_workout_plans', views.trainer_workout_plans, name='trainer_workout_plans'),
    # Trainer diet plans
    path('trainer/create_diet_plan', views.create_diet_plan, name='create_diet_plan'),
    path('trainer/my_diet_plans', views.trainer_diet_plans, name='trainer_diet_plans'),
    # Aliases for backward compatibility
    path('trainer/create_workout_plan', views.create_workout_plan, name='create_workout_plan_page'),
    path('trainer/create_diet_plan', views.create_diet_plan, name='create_diet_plan_page'),
    # Trainer Plan Details
    path('trainer/workout_plan/<int:plan_id>/', views.workout_plan_detail, name='workout_plan_detail'),
    path('trainer/diet_plan/<int:plan_id>/', views.diet_plan_detail, name='diet_plan_detail'),


    # ----------------- ADMIN PORTAL -----------------
    path('admin_portal', views.admin_portal, name='admin_portal'),
    path('approve_payment/<int:user_id>', views.approve_payment, name='approve_payment'),
    path('reject_payment/<int:user_id>', views.reject_payment, name='reject_payment'),
    path('change_gym_info/', views.change_gym_info, name='change_gym_info'),
    
    # Trainer management
    path('add_trainer', views.add_trainer, name='add_trainer'),
    path('all_trainers', views.all_trainers, name='all_trainers'),
    path('delete_trainer/<int:trainer_id>', views.delete_trainer, name='delete_trainer'),

    # Member management
    path('assign_trainer_to_member', views.assign_trainer_to_member, name='assign_trainer_to_member'),
    path('all_members', views.all_members, name='all_members'),
    path('delete_member/<int:member_id>', views.delete_member, name='delete_member'),
    path('search_members', views.search_members, name='search_members'),

    # Attendance & Analytics
    path('trainer_attendance', views.trainer_attendance, name='trainer_attendance'),
    path('attendance_history', views.attendance_history, name='attendance_history'),
    path('progress_charts', views.progress_charts, name='progress_charts'),
]
