from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q, Count
from .models import *
import datetime
from datetime import timedelta
from collections import defaultdict
import json
from datetime import date



ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123',
    'first_name': 'Admin',
    'last_name': 'User',
    'email': 'admin@gym.com',
    'phone_number': '03001234567'
}

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def home(request):
    return render(request, 'home.html')

def user_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("u_username")
        password = request.POST.get("u_password")
        user_data = Gym_user.get_user_by_username(username)
        
        if user_data:
            if check_password(password, user_data.password):
                if not user_data.is_approved:
                    data["error"] = "Your account is pending admin approval."
                elif user_data.membership_end_date and user_data.membership_end_date < datetime.date.today():
                    if not user_data.is_blocked:
                        user_data.is_blocked = True
                        user_data.save()
                    data["error"] = "Your membership has expired! Please renew your membership to continue."
                elif user_data.is_blocked:
                    data["error"] = "Your membership has expired! Please renew your membership to continue."
                else:
                    request.session['user_id'] = user_data.id
                    request.session['user_type'] = 'member'
                    return redirect('/user_portal')
            else:
                data["error"] = "Password is incorrect!"
        else:
            data["error"] = "Incorrect username or password!"
    
    return render(request, 'user_login.html', data)

def trainer_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("t_username")
        password = request.POST.get("t_password")
        trainer_data = Trainer.get_trainer_by_username(username)
        
        if trainer_data:
            if check_password(password, trainer_data.password):
                request.session['trainer_id'] = trainer_data.id
                request.session['user_type'] = 'trainer'
                return redirect('/trainer_portal')
            else:
                data["error"] = "Password is incorrect!"
        else:
            data["error"] = "Incorrect username or password!"
    
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
            data["error"] = "Incorrect username or password!"
    
    return render(request, 'admin_login.html', data)

def logout(request):
    request.session.flush()
    return redirect('/')

def new_registration(request):
    data = {}
    membership_plans = MembershipPlan.objects.all()
    genders = Gender.objects.all()
    data['membership_plans'] = membership_plans
    data['genders'] = genders
    
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        dob = request.POST.get("dob")
        phone_number = request.POST.get("phone_number")
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")
        gender_id = request.POST.get("gender")
        email = request.POST.get("email")
        membership_plan_id = request.POST.get("membership_plan")
        payment_proof = request.FILES.get("payment_proof")
        
        error = ""
        
        if len(first_name) < 2 or len(last_name) < 2 or len(username) < 2:
            error = "Name and username fields cannot be empty"
        elif len(password) < 5:
            error = "Password length should be at least 5 characters"
        elif password != c_password:
            error = "Both passwords should match"
        elif Gym_user.get_user_by_username(username):
            error = "Username already exists"
        elif not payment_proof:
            error = "Please upload payment proof"
        else:
            user = Gym_user()
            user.first_name = first_name.strip()
            user.last_name = last_name.strip()
            user.dob = dob
            user.phone_number = phone_number
            user.username = username.strip()
            user.password = make_password(password)
            user.email = email
            user.gender_id = gender_id
            user.membership_plan_id = membership_plan_id
            user.payment_proof = payment_proof
            user.is_approved = False
            user.save()
            
            data["msg"] = "Registration successful! Please wait for admin approval (within 24 hours)."
            data["success"] = True
        
        data["error"] = error
    
    return render(request, 'new_registration.html', data)

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
    
    all_workout_plans = WorkoutPlan.objects.all()
    all_diet_plans = DietPlan.objects.all()
    
    data = {
        'user': user,
        'bmi': bmi,
        'bmi_status': bmi_status,
        'all_workout_plans': all_workout_plans,
        'all_diet_plans': all_diet_plans
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

def trainer_portal(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')
    
    trainer = Trainer.objects.get(id=request.session['trainer_id'])
    workout_plans = WorkoutPlan.objects.filter(trainer=trainer).prefetch_related('workout_days')
    diet_plans = DietPlan.objects.filter(trainer=trainer).prefetch_related('diet_days')
    assigned_members = Gym_user.objects.filter(assigned_trainer=trainer)
    
    data = {
        'trainer': trainer,
        'workout_plans': workout_plans,
        'diet_plans': diet_plans,
        'assigned_members': assigned_members,
        'days_of_week': DAYS_OF_WEEK
    }
    
    return render(request, 'trainer_portal.html', data)

def create_workout_plan(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')
    
    if request.method == "POST":
        trainer = Trainer.objects.get(id=request.session['trainer_id'])
        
        workout = WorkoutPlan()
        workout.trainer = trainer
        workout.name = request.POST.get("name")
        workout.description = request.POST.get("description")
        workout.difficulty_level = request.POST.get("difficulty_level")
        workout.save()
        
        for day in DAYS_OF_WEEK:
            exercises = request.POST.get(f"exercises_{day}")
            if exercises and exercises.strip():
                WorkoutDay.objects.create(
                    workout_plan=workout,
                    day_name=day,
                    exercises=exercises,
                    notes=request.POST.get(f"notes_{day}", "")
                )
    
    return redirect('/trainer_portal')

def create_diet_plan(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')
    
    if request.method == "POST":
        trainer = Trainer.objects.get(id=request.session['trainer_id'])
        
        diet = DietPlan()
        diet.trainer = trainer
        diet.name = request.POST.get("name")
        diet.description = request.POST.get("description")
        diet.total_calories = request.POST.get("total_calories")
        diet.save()
        
        for day in DAYS_OF_WEEK:
            breakfast = request.POST.get(f"breakfast_{day}")
            if breakfast and breakfast.strip():
                DietDay.objects.create(
                    diet_plan=diet,
                    day_name=day,
                    breakfast=breakfast,
                    lunch=request.POST.get(f"lunch_{day}", ""),
                    dinner=request.POST.get(f"dinner_{day}", ""),
                    snacks=request.POST.get(f"snacks_{day}", "")
                )
    
    return redirect('/trainer_portal')

def assign_plan_to_member(request):
    if 'trainer_id' not in request.session:
        return redirect('/trainer_login')
    
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        workout_plan_id = request.POST.get("workout_plan_id")
        diet_plan_id = request.POST.get("diet_plan_id")
        
        if member_id:
            try:
                member = Gym_user.objects.get(id=member_id)
                
                if workout_plan_id:
                    member.assigned_workout_plan_id = workout_plan_id
                if diet_plan_id:
                    member.assigned_diet_plan_id = diet_plan_id
                
                member.save()
            except Gym_user.DoesNotExist:
                pass
    
    return redirect('/trainer_portal')

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
        'today': datetime.date.today()
    }
    
    return render(request, 'admin/dashboard.html', data)

def approve_payment(request, user_id):
    if 'admin_logged_in' not in request.session:
        return redirect('/admin_login')
    
    user = Gym_user.objects.get(id=user_id)
    user.is_approved = True
    user.is_blocked = False
    user.reminder_sent = False
    user.membership_start_date = datetime.date.today()
    user.membership_end_date = datetime.date.today() + timedelta(days=user.membership_plan.duration_months * 30)
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
    'today': date.today(), 
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
    today = datetime.date.today()
    
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
    today = datetime.date.today()
    twelve_months_ago = today - timedelta(days=365)
    
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
        date_obj = datetime.datetime.strptime(month, '%Y-%m')
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