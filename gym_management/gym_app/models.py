from django.db import models
from django.utils import timezone

class Gender(models.Model):
    gender = models.CharField(max_length=30)
    
    def __str__(self):
        return self.gender

class Address(models.Model):
    area = models.CharField(max_length=30)
    
    def __str__(self):
        return self.area

class Gym_split(models.Model):
    split_name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.split_name

class Muscle_strength(models.Model):
    type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.type

class MembershipPlan(models.Model):
    duration_months = models.IntegerField()
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.duration_months} month(s) - {self.price} PKR"

class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="trainers/", default="trainers/default.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def get_trainer_by_username(username):
        try:
            return Trainer.objects.get(username=username)
        except Trainer.DoesNotExist:
            return None

class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='workout_plans')
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} by {self.trainer.first_name}"

class WorkoutDay(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='workout_days')
    day_name = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ])
    exercises = models.TextField(help_text="Enter exercises (one per line with sets/reps)")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['day_name']
        unique_together = ['workout_plan', 'day_name']
    
    def __str__(self):
        return f"{self.workout_plan.name} - {self.day_name}"

class DietPlan(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='diet_plans')
    name = models.CharField(max_length=200)
    description = models.TextField()
    total_calories = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} by {self.trainer.first_name}"

class DietDay(models.Model):
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='diet_days')
    day_name = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ])
    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()
    snacks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['day_name']
        unique_together = ['diet_plan', 'day_name']
    
    def __str__(self):
        return f"{self.diet_plan.name} - {self.day_name}"

class Gym_user(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="users_profile_images/", default="users_profile_images/default.png", null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    date_of_joining = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    gym_split = models.ForeignKey(Gym_split, on_delete=models.CASCADE, null=True, blank=True)
    muscle_strength = models.ForeignKey(Muscle_strength, on_delete=models.CASCADE, null=True, blank=True)
    
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, null=True, blank=True)
    payment_proof = models.ImageField(upload_to="payment_proofs/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    
    assigned_trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_members')
    trainer_requested = models.BooleanField(default=False)
    
    assigned_workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_diet_plan = models.ForeignKey(DietPlan, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def get_all_users():
        return Gym_user.objects.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return Gym_user.objects.get(id=user_id)
    
    @staticmethod
    def get_searched_members(query):
        return Gym_user.objects.filter(first_name__icontains=query)
    
    @staticmethod
    def by_lastName(query):
        return Gym_user.objects.filter(last_name__icontains=query)
    
    @staticmethod
    def by_username(query):
        return Gym_user.objects.filter(username__icontains=query)
    
    @staticmethod
    def by_id(query):
        return Gym_user.objects.filter(id=int(query))
    
    @staticmethod
    def get_user_by_username(username):
        try:
            return Gym_user.objects.get(username=username)
        except Gym_user.DoesNotExist:
            return None
    
    @staticmethod
    def get_pending_approvals():
        return Gym_user.objects.filter(is_approved=False)
    
    @staticmethod
    def get_trainer_requests():
        return Gym_user.objects.filter(trainer_requested=True, assigned_trainer=None)

class TrainerAttendance(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['trainer', 'date']
    
    def __str__(self):
        return f"{self.trainer.first_name} - {self.date} - {'Present' if self.present else 'Absent'}"