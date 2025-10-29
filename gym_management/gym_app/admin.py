from django.contrib import admin
from .models import (
    Gender, Address, Gym_split, Muscle_strength, MembershipPlan,
    Trainer, WorkoutPlan, WorkoutDay, DietPlan, DietDay,
    Gym_user, TrainerAttendance
)

# Gender Admin
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('gender',)
    search_fields = ('gender',)

# Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('area',)
    search_fields = ('area',)

# Gym_split Admin
@admin.register(Gym_split)
class GymSplitAdmin(admin.ModelAdmin):
    list_display = ('split_name',)
    search_fields = ('split_name',)

# Muscle_strength Admin
@admin.register(Muscle_strength)
class MuscleStrengthAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

# MembershipPlan Admin
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'price')
    list_filter = ('duration_months',)
    search_fields = ('name',)

# Trainer Admin
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('created_at',)

# WorkoutPlan Admin
@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'difficulty_level', 'is_default', 'created_at')
    list_filter = ('difficulty_level', 'is_default', 'created_at')
    search_fields = ('name', 'trainer__first_name', 'trainer__last_name')
    readonly_fields = ('created_at',)

# WorkoutDay Admin
@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'day_name')
    list_filter = ('day_name',)
    search_fields = ('workout_plan__name', 'day_name')

# DietPlan Admin
@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'total_calories', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('name', 'trainer__first_name', 'trainer__last_name')
    readonly_fields = ('created_at',)

# DietDay Admin
@admin.register(DietDay)
class DietDayAdmin(admin.ModelAdmin):
    list_display = ('diet_plan', 'day_name')
    list_filter = ('day_name',)
    search_fields = ('diet_plan__name', 'day_name')

# Gym_user Admin
@admin.register(Gym_user)
class GymUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'username', 'email', 'phone_number',
        'is_approved', 'is_blocked', 'date_of_joining', 'membership_plan'
    )
    list_filter = (
        'is_approved', 'is_blocked', 'gender', 'gym_split', 
        'muscle_strength', 'date_of_joining'
    )
    search_fields = ('first_name', 'last_name', 'username', 'email', 'phone_number')
    readonly_fields = ('date_of_joining',)
    list_editable = ('is_approved', 'is_blocked')

# TrainerAttendance Admin
@admin.register(TrainerAttendance)
class TrainerAttendanceAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'date', 'present')
    list_filter = ('date', 'present')
    search_fields = ('trainer__first_name', 'trainer__last_name')
    readonly_fields = ('date',)