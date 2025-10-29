from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from collections import defaultdict
from django.contrib import messages
from django import forms
import datetime as dt
import json
from .models import (
    Gym_user, Trainer, WorkoutPlan, WorkoutDay,
    DietPlan, DietDay, TrainerAttendance, MembershipPlan, Gender, GymInfo
)

# Form for GymInfo
class GymInfoForm(forms.ModelForm):
    class Meta:
        model = GymInfo
        fields = ['address', 'phone_number', 'email', 'operating_hours']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter gym address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'operating_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mon-Fri: 6AM-10PM, Sat-Sun: 8AM-8PM'
            }),
        }


# ----------------- CONSTANTS -----------------
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123',
    'first_name': 'Admin',
    'last_name': 'User',
    'email': 'admin@gym.com',
    'phone_number': '03001234567'
}

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# ----------------- HOME -----------------
def home(request):
    # Get all active trainers from the Trainer model
    trainers = Trainer.objects.all()
    
    context = {
        'trainers': trainers
    }
    return render(request, 'home.html', context)

# ----------------- LOGIN & AUTH -----------------
def user_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("u_username")
        password = request.POST.get("u_password")
        user_data = Gym_user.get_user_by_username(username)
        
        if user_data and check_password(password, user_data.password):
            if not user_data.is_approved:
                data["error"] = "Your account is pending admin approval."
            elif user_data.membership_end_date and user_data.membership_end_date < dt.date.today():
                user_data.is_blocked = True
                user_data.save()
                data["error"] = "Your membership has expired! Please renew your membership."
            elif user_data.is_blocked:
                data["error"] = "Your membership has expired! Please renew your membership."
            else:
                request.session['user_id'] = user_data.id
                request.session['user_type'] = 'member'
                return redirect('/user_portal')
        else:
            data["error"] = "Invalid username or password!"
    
    return render(request, 'user_login.html', data)


def trainer_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("t_username")
        password = request.POST.get("t_password")
        trainer_data = Trainer.get_trainer_by_username(username)
        
        if trainer_data and check_password(password, trainer_data.password):
            request.session['trainer_id'] = trainer_data.id
            request.session['user_type'] = 'trainer'
            return redirect('/trainer/dashboard')
        else:
            data["error"] = "Invalid username or password!"
    
    return render(request, 'trainer_login.html', data)


def admin_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("a_username")
        password = request.POST.get("a_password")
        
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            request.session['admin_logged_in'] = True
            request.session['user_type'] = 'admin'
            return redirect('/admin_portal')
        else:
            data["error"] = "Invalid admin credentials!"
    
    return render(request, 'admin_login.html', data)


def logout(request):
    request.session.flush()
    return redirect('/')


# ----------------- REGISTRATION -----------------
def new_registration(request):
    data = {}
    data['membership_plans'] = MembershipPlan.objects.all()
    data['genders'] = Gender.objects.all()

    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        dob = request.POST.get("dob")
        gender_id = request.POST.get("gender")
        membership_plan_id = request.POST.get("membership_plan")
        payment_proof = request.FILES.get("payment_proof")

        # Keep all form data in context so we can refill fields if error occurs
        data["form_data"] = request.POST  

        if not all([first_name, last_name, username, password, c_password, email]):
            data["error"] = "All fields are required!"
        elif password != c_password:
            data["error"] = "Passwords do not match!"
        elif Gym_user.get_user_by_username(username):
            data["error"] = "Username already exists!"
        else:
            user = Gym_user(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                dob=dob,
                phone_number=phone_number,
                username=username.strip(),
                password=make_password(password),
                email=email,
                gender_id=gender_id,
                membership_plan_id=membership_plan_id,
                payment_proof=payment_proof,
                is_approved=False
            )
            user.save()
            data["msg"] = "Registration successful! Awaiting admin approval."
            data["success"] = True

    return render(request, 'new_registration.html', data)


# ----------------- USER PORTAL -----------------
def user_portal(request):
    if 'user_id' not in request.session:
        return redirect('/user_login')

    user = Gym_user.get_user_by_id(request.session['user_id'])
    bmi = None
    bmi_status = None

    if user.height and user.weight:
        height_m = user.height / 100
        bmi = round(user.weight / (height_m ** 2), 2)
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Normal weight"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

    data = {
        'user': user,
        'bmi': bmi,
        'bmi_status': bmi_status,
        'all_workout_plans': WorkoutPlan.objects.all(),
        'all_diet_plans': DietPlan.objects.all()
    }
    return render(request, 'user_portal.html', data)


def request_trainer(request):
    if 'user_id' not in request.session:
        return redirect('/user_login')

    user = Gym_user.get_user_by_id(request.session['user_id'])
    user.trainer_requested = True
    user.save()
    return redirect('/user_portal')


def update_user_info(request):
    if 'user_id' not in request.session:
        return redirect('/user_login')

    if request.method == "POST":
        user = Gym_user.get_user_by_id(request.session['user_id'])
        user.email = request.POST.get("email", user.email)
        user.phone_number = request.POST.get("phone_number", user.phone_number)
        user.weight = request.POST.get("weight", user.weight)
        user.height = request.POST.get("height", user.height)
        user.save()

    return redirect('/user_portal')


# ----------------- TRAINER SECTION -----------------
def trainer_dashboard(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])
    total_clients = Gym_user.objects.filter(assigned_trainer=trainer).count()
    total_workouts = WorkoutPlan.objects.filter(trainer=trainer).count()
    total_diets = DietPlan.objects.filter(trainer=trainer).count()

    data = {
        'trainer': trainer,
        'total_clients': total_clients,
        'total_workouts': total_workouts,
        'total_diets': total_diets
    }
    return render(request, 'trainer/dashboard.html', data)


def trainer_clients(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])
    query = request.GET.get('q', '')
    members = Gym_user.objects.filter(assigned_trainer=trainer)

    if query:
        members = members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    context = {
        'trainer': trainer,
        'members': members,
        'workout_plans': WorkoutPlan.objects.filter(trainer=trainer),
        'diet_plans': DietPlan.objects.filter(trainer=trainer),
        'query': query
    }
    return render(request, 'trainer/client_management.html', context)


def create_workout_plan(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])

    if request.method == "POST":
        workout = WorkoutPlan.objects.create(
            trainer=trainer,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            difficulty_level=request.POST.get("difficulty_level")
        )
        for day in DAYS_OF_WEEK:
            exercises = request.POST.get(f"exercises_{day}")
            if exercises:
                WorkoutDay.objects.create(
                    workout_plan=workout,
                    day_name=day,
                    exercises=exercises,
                    notes=request.POST.get(f"notes_{day}", "")
                )
        return redirect('/trainer/my_workout_plans')

    return render(request, 'trainer/create_workout_plan.html', {'trainer': trainer, 'days_of_week': DAYS_OF_WEEK})


def create_diet_plan(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])

    if request.method == "POST":
        diet = DietPlan.objects.create(
            trainer=trainer,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            total_calories=request.POST.get("total_calories")
        )
        for day in DAYS_OF_WEEK:
            breakfast = request.POST.get(f"breakfast_{day}")
            if breakfast:
                DietDay.objects.create(
                    diet_plan=diet,
                    day_name=day,
                    breakfast=breakfast,
                    lunch=request.POST.get(f"lunch_{day}", ""),
                    dinner=request.POST.get(f"dinner_{day}", ""),
                    snacks=request.POST.get(f"snacks_{day}", "")
                )
        return redirect('/trainer/my_diet_plans')

    return render(request, 'trainer/create_diet_plan.html', {'trainer': trainer, 'days_of_week': DAYS_OF_WEEK})


def trainer_workout_plans(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])
    plans = WorkoutPlan.objects.filter(trainer=trainer)
    return render(request, 'trainer/my_workout_plans.html', {'trainer': trainer, 'workout_plans': plans})


def trainer_diet_plans(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = Trainer.objects.get(id=request.session['trainer_id'])
    plans = DietPlan.objects.filter(trainer=trainer)
    return render(request, 'trainer/my_diet_plans.html', {'trainer': trainer, 'diet_plans': plans})


def assign_plan_to_member(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        workout_plan_id = request.POST.get("workout_plan_id")
        diet_plan_id = request.POST.get("diet_plan_id")

        member = Gym_user.objects.filter(id=member_id).first()
        if member:
            if workout_plan_id:
                member.assigned_workout_plan_id = workout_plan_id
            if diet_plan_id:
                member.assigned_diet_plan_id = diet_plan_id
            member.save()
    return redirect('/trainer/clients')


def workout_plan_detail(request, plan_id):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = get_object_or_404(Trainer, id=request.session['trainer_id'])
    workout_plan = get_object_or_404(WorkoutPlan, id=plan_id, trainer=trainer)
    workout_days = WorkoutDay.objects.filter(workout_plan=workout_plan)

    return render(request, 'trainer/workout_plan_detail.html', {
        'trainer': trainer,  # ✅ add this
        'workout_plan': workout_plan,
        'workout_days': workout_days
    })


def diet_plan_detail(request, plan_id):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')

    trainer = get_object_or_404(Trainer, id=request.session['trainer_id'])
    diet_plan = get_object_or_404(DietPlan, id=plan_id, trainer=trainer)
    diet_days = DietDay.objects.filter(diet_plan=diet_plan)

    return render(request, 'trainer/diet_plan_detail.html', {
        'trainer': trainer,  # ✅ add this
        'diet_plan': diet_plan,
        'diet_days': diet_days
    })


# ADMIN VIEWS
def admin_portal(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    pending_approvals = Gym_user.get_pending_approvals()
    trainer_requests = Gym_user.get_trainer_requests()
    all_members = Gym_user.objects.filter(is_approved=True).order_by('-date_of_joining')
    all_trainers = Trainer.objects.all()
    
    total_revenue = sum([member.membership_plan.price for member in all_members if member.membership_plan])
    
    pending_count = pending_approvals.count()
    trainer_request_count = trainer_requests.count()
    
    data = {
        'admin': ADMIN_CREDENTIALS,
        'pending_approvals': pending_approvals,
        'trainer_requests': trainer_requests,
        'all_members': all_members,
        'all_trainers': all_trainers,
        'total_revenue': total_revenue,
        'pending_count': pending_count,
        'trainer_request_count': trainer_request_count,
        'total_members': all_members.count(),
        'total_trainers': all_trainers.count(),
        'today': dt.date.today()
    }
    
    return render(request, 'admin/dashboard.html', data)


def approve_payment(request, user_id):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    user = Gym_user.objects.get(id=user_id)
    user.is_approved = True
    user.is_blocked = False
    user.reminder_sent = False
    user.membership_start_date = dt.date.today()
    user.membership_end_date = dt.date.today() + dt.timedelta(days=user.membership_plan.duration_months * 30)
    user.save()
    
    return redirect('/admin_portal')


def reject_payment(request, user_id):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    user = Gym_user.objects.get(id=user_id)
    user.delete()
    
    return redirect('/admin_portal')


def add_trainer(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    data = {
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    if request.method == "POST":
        error = ""
        username = request.POST.get("username")
        
        if Trainer.get_trainer_by_username(username):
            error = "Username already exists"
            data["error"] = error
        else:
            trainer = Trainer()
            trainer.first_name = request.POST.get("first_name")
            trainer.last_name = request.POST.get("last_name")
            trainer.email = request.POST.get("email")
            trainer.phone_number = request.POST.get("phone_number")
            trainer.username = username
            trainer.password = make_password(request.POST.get("password"))
            trainer.specialization = request.POST.get("specialization")
            trainer.save()
            
            data["success"] = "Trainer created successfully!"
            return redirect('/all_trainers')
    
    return render(request, 'admin/add_trainer.html', data)


def all_trainers(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    trainers = Trainer.objects.all()
    
    data = {
        'trainers': trainers,
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/all_trainers.html', data)


def delete_trainer(request, trainer_id):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    trainer = get_object_or_404(Trainer, id=trainer_id)
    trainer.delete()
    
    return redirect('/all_trainers')


def assign_trainer_to_member(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        trainer_id = request.POST.get("trainer_id")
        
        member = Gym_user.objects.get(id=member_id)
        member.assigned_trainer_id = trainer_id
        member.trainer_requested = False
        member.save()
    
    return redirect('/admin_portal')


def all_members(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    query = request.GET.get('q', '')
    
    if query:
        members = Gym_user.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(phone_number__icontains=query)
        ).filter(is_approved=True)
    else:
        members = Gym_user.objects.filter(is_approved=True)
    
    data = {
    'members': members,
    'query': query,
    'today': dt.date.today(), 
    'pending_count': Gym_user.get_pending_approvals().count(),
    'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/all_members.html', data)


def delete_member(request, member_id):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    member = get_object_or_404(Gym_user, id=member_id)
    member.delete()
    
    return redirect('/all_members')


def search_members(request):
    return redirect('/all_members')


def trainer_attendance(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    trainers = Trainer.objects.all()
    today = dt.date.today()
    
    if request.method == "POST":
        for trainer in trainers:
            present = request.POST.get(f"trainer_{trainer.id}")
            notes = request.POST.get(f"notes_{trainer.id}", "").strip()  # get notes input
            
            TrainerAttendance.objects.update_or_create(
                trainer=trainer,
                date=today,
                defaults={
                    'present': present is not None,
                    'notes': notes
                }
            )
        
        return redirect('/trainer_attendance')
    
    attendance_records = TrainerAttendance.objects.filter(date=today)
    marked_trainer_ids = [record.trainer_id for record in attendance_records]
    
    data = {
        'trainers': trainers,
        'attendance_records': attendance_records,
        'marked_trainer_ids': marked_trainer_ids,
        'today': today,
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/trainer_attendance.html', data)


def attendance_history(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    trainers = Trainer.objects.all()
    all_attendance = TrainerAttendance.objects.all().order_by('-date')
    
    trainer_filter = request.GET.get('trainer_id')
    if trainer_filter:
        all_attendance = all_attendance.filter(trainer_id=trainer_filter)
    
    data = {
        'trainers': trainers,
        'attendance_records': all_attendance,
        'selected_trainer': trainer_filter,
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/attendance_history.html', data)


def progress_charts(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    # Get all members
    all_members = Gym_user.objects.filter(is_approved=True)
    all_trainers = Trainer.objects.all()
    
    # Calculate revenue
    total_revenue = sum([member.membership_plan.price for member in all_members if member.membership_plan])
    
    # Members joined by month (last 12 months)
    today = dt.date.today()
    twelve_months_ago = today - dt.timedelta(days=365)
    
    members_by_month = defaultdict(int)
    revenue_by_month = defaultdict(int)
    
    for member in all_members:
        if member.date_of_joining.date() >= twelve_months_ago:
            month_key = member.date_of_joining.strftime('%Y-%m')
            members_by_month[month_key] += 1
            if member.membership_plan:
                revenue_by_month[month_key] += member.membership_plan.price
    
    # Sort by date
    sorted_months = sorted(members_by_month.keys())
    member_counts = [members_by_month[month] for month in sorted_months]
    revenue_counts = [revenue_by_month[month] for month in sorted_months]
    
    # Format month labels
    month_labels = []
    for month in sorted_months:
        date_obj = dt.datetime.strptime(month, '%Y-%m')
        month_labels.append(date_obj.strftime('%b %Y'))
    
    # Membership plan distribution
    plan_distribution = {}
    for member in all_members:
        if member.membership_plan:
            plan_name = member.membership_plan.name
            plan_distribution[plan_name] = plan_distribution.get(plan_name, 0) + 1
    
    # Active vs Expired memberships
    active_members = 0
    expired_members = 0
    for member in all_members:
        if member.membership_end_date:
            if member.membership_end_date >= today:
                active_members += 1
            else:
                expired_members += 1
    
    # Trainer assignment stats
    assigned_members = all_members.filter(assigned_trainer__isnull=False).count()
    unassigned_members = all_members.filter(assigned_trainer__isnull=True).count()
    
    data = {
        'total_members': all_members.count(),
        'total_trainers': all_trainers.count(),
        'total_revenue': total_revenue,
        'active_members': active_members,
        'expired_members': expired_members,
        'assigned_members': assigned_members,
        'unassigned_members': unassigned_members,
        'month_labels': json.dumps(month_labels),
        'member_counts': json.dumps(member_counts),
        'revenue_counts': json.dumps(revenue_counts),
        'plan_names': json.dumps(list(plan_distribution.keys())),
        'plan_counts': json.dumps(list(plan_distribution.values())),
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/progress_charts.html', data)
def change_gym_info(request):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    # Get or create the single GymInfo instance
    gym_info = GymInfo.objects.first()
    
    if request.method == "POST":
        if gym_info:
            form = GymInfoForm(request.POST, instance=gym_info)
        else:
            form = GymInfoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Gym information updated successfully!")
            return redirect('/change_gym_info/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        if gym_info:
            form = GymInfoForm(instance=gym_info)
        else:
            form = GymInfoForm()
    
    data = {
        'form': form,
        'gym_info': gym_info,
        'pending_count': Gym_user.get_pending_approvals().count(),
        'trainer_request_count': Gym_user.get_trainer_requests().count()
    }
    
    return render(request, 'admin/change_gym_info.html', data)

# ----------------- ENHANCED USER PORTAL VIEWS -----------------
def workout_plan_detail_user(request):
    """Enhanced workout plan page for users"""
    if 'user_id' not in request.session:
        return redirect('/user_login')

    user = Gym_user.get_user_by_id(request.session['user_id'])
    assigned_plan = user.assigned_workout_plan
    all_plans = WorkoutPlan.objects.all().prefetch_related('workout_days')
    
    # Get today's workout
    today_name = dt.datetime.now().strftime('%A')
    today_workout = None
    if assigned_plan:
        today_workout = WorkoutDay.objects.filter(
            workout_plan=assigned_plan, 
            day_name=today_name
        ).first()

    context = {
        'user': user,
        'assigned_plan': assigned_plan,
        'all_plans': all_plans,
        'today_workout': today_workout,
        'today_name': today_name
    }
    return render(request, 'workout_plan.html', context)


def diet_plan_detail_user(request):
    """Enhanced diet plan page for users"""
    if 'user_id' not in request.session:
        return redirect('/user_login')

    user = Gym_user.get_user_by_id(request.session['user_id'])
    assigned_plan = user.assigned_diet_plan
    all_plans = DietPlan.objects.all().prefetch_related('diet_days')
    
    # Get today's meals
    today_name = dt.datetime.now().strftime('%A')
    today_meals = None
    if assigned_plan:
        today_meals = DietDay.objects.filter(
            diet_plan=assigned_plan, 
            day_name=today_name
        ).first()

    context = {
        'user': user,
        'assigned_plan': assigned_plan,
        'all_plans': all_plans,
        'today_meals': today_meals,
        'today_name': today_name
    }
    return render(request, 'diet_plan.html', context)


def upload_profile_image(request):
    """Handle profile image uploads"""
    if 'user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'Not authenticated'})

    if request.method == 'POST' and request.FILES.get('image'):
        user = Gym_user.get_user_by_id(request.session['user_id'])
        user.image = request.FILES['image']
        user.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Profile image updated successfully',
            'image_url': user.image.url
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})









def change_password(request):
    if 'user_id' not in request.session:
        return redirect('/user_login')

    user = Gym_user.get_user_by_id(request.session['user_id'])

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not check_password(old_password, user.password):
            messages.error(request, "Old password is incorrect!")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('/user_portal')

    return render(request, 'change_password.html', {'user': user})


# Add this new view function to your views.py file

def upload_trainer_profile_image(request):
    """Handle trainer profile image uploads"""
    if 'trainer_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'Not authenticated'})

    if request.method == 'POST' and request.FILES.get('image'):
        trainer = Trainer.objects.get(id=request.session['trainer_id'])
        trainer.image = request.FILES['image']
        trainer.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Profile image updated successfully',
            'image_url': trainer.image.url
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})