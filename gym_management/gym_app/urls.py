from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication URLs
    path('', views.home, name='home'),
    path('user_login', views.user_login, name='user_login'),
    path('trainer_login', views.trainer_login, name='trainer_login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('logout', views.logout, name='logout'),
    path('new_registration', views.new_registration, name='new_registration'),
    
    # User/Member Portal URLs
    path('user_portal', views.user_portal, name='user_portal'),
    path('request_trainer', views.request_trainer, name='request_trainer'),
    path('update_user_info', views.update_user_info, name='update_user_info'),
    
    # Trainer Portal URLs
    path('trainer_portal', views.trainer_portal, name='trainer_portal'),
    path('create_workout_plan', views.create_workout_plan, name='create_workout_plan'),
    path('create_diet_plan', views.create_diet_plan, name='create_diet_plan'),
    path('assign_plan_to_member', views.assign_plan_to_member, name='assign_plan_to_member'),
    
    # Admin Portal URLs
    path('admin_portal', views.admin_portal, name='admin_portal'),
    path('approve_payment/<int:user_id>', views.approve_payment, name='approve_payment'),
    path('reject_payment/<int:user_id>', views.reject_payment, name='reject_payment'),
    
    # Admin - Trainers
    path('add_trainer', views.add_trainer, name='add_trainer'),
    path('all_trainers', views.all_trainers, name='all_trainers'),
    path('delete_trainer/<int:trainer_id>', views.delete_trainer, name='delete_trainer'),
    path('assign_trainer_to_member', views.assign_trainer_to_member, name='assign_trainer_to_member'),
    
    # Admin - Members
    path('all_members', views.all_members, name='all_members'),
    path('delete_member/<int:member_id>', views.delete_member, name='delete_member'),
    path('search_members', views.search_members, name='search_members'),
    
    # Admin - Attendance
    path('trainer_attendance', views.trainer_attendance, name='trainer_attendance'),
    path('attendance_history', views.attendance_history, name='attendance_history'),
    
    # Admin - Progress Charts
    path('progress_charts', views.progress_charts, name='progress_charts'),
]