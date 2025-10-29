"""
Place this file in: gym_management/gym_app/management/commands/seed_professional_plans.py
Run with: python manage.py seed_professional_plans
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gym_management.gym_app.models import Trainer, WorkoutPlan, WorkoutDay, DietPlan, DietDay

class Command(BaseCommand):
    help = 'Seeds the database with professional workout and diet plans'

    def handle(self, *args, **kwargs):
        # Create a default trainer if not exists
        trainer, created = Trainer.objects.get_or_create(
            username='system_trainer',
            defaults={
                'first_name': 'System',
                'last_name': 'Trainer',
                'email': 'system@gym.com',
                'phone_number': '03001234567',
                'password': make_password('trainer123'),
                'specialization': 'All-round Fitness Expert'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created system trainer'))
        
        # Clear existing default plans
        WorkoutPlan.objects.filter(is_default=True).delete()
        DietPlan.objects.filter(is_default=True).delete()
        
        # ===== WORKOUT PLANS =====
        
        # 1. Beginner Full Body Workout
        beginner_workout = WorkoutPlan.objects.create(
            trainer=trainer,
            name='Beginner Full Body Program',
            description='Perfect for those new to fitness. 3 days per week focusing on building strength and proper form.',
            difficulty_level='beginner',
            is_default=True
        )
        
        beginner_days = {
            'Monday': '''Squats - 3 sets x 12 reps
Push-ups (knee or regular) - 3 sets x 10 reps
Dumbbell Rows - 3 sets x 12 reps
Plank - 3 sets x 30 seconds
Walking Lunges - 3 sets x 10 reps per leg''',
            
            'Tuesday': 'Rest Day - Light walking or stretching',
            
            'Wednesday': '''Goblet Squats - 3 sets x 12 reps
Dumbbell Chest Press - 3 sets x 10 reps
Lat Pulldowns - 3 sets x 12 reps
Bicycle Crunches - 3 sets x 15 reps
Leg Raises - 3 sets x 10 reps''',
            
            'Thursday': 'Rest Day - Active recovery (yoga or light cardio)',
            
            'Friday': '''Deadlifts (light weight) - 3 sets x 10 reps
Shoulder Press - 3 sets x 10 reps
Bent Over Rows - 3 sets x 12 reps
Mountain Climbers - 3 sets x 15 reps
Side Planks - 3 sets x 20 seconds each side''',
            
            'Saturday': 'Rest Day or 20 min cardio',
            'Sunday': 'Rest Day - Full recovery'
        }
        
        for day, exercises in beginner_days.items():
            WorkoutDay.objects.create(
                workout_plan=beginner_workout,
                day_name=day,
                exercises=exercises
            )
        
        # 2. Intermediate Push Pull Legs
        intermediate_workout = WorkoutPlan.objects.create(
            trainer=trainer,
            name='Intermediate Push/Pull/Legs Split',
            description='6-day program alternating between push, pull, and leg days. Great for building muscle and strength.',
            difficulty_level='intermediate',
            is_default=True
        )
        
        intermediate_days = {
            'Monday': '''PUSH DAY
Bench Press - 4 sets x 8-10 reps
Incline Dumbbell Press - 4 sets x 10 reps
Shoulder Press - 3 sets x 10 reps
Lateral Raises - 3 sets x 12 reps
Tricep Dips - 3 sets x 10 reps
Overhead Tricep Extension - 3 sets x 12 reps''',
            
            'Tuesday': '''PULL DAY
Deadlifts - 4 sets x 6-8 reps
Pull-ups - 4 sets x max reps
Barbell Rows - 4 sets x 8 reps
Face Pulls - 3 sets x 15 reps
Barbell Curls - 3 sets x 10 reps
Hammer Curls - 3 sets x 12 reps''',
            
            'Wednesday': '''LEG DAY
Squats - 4 sets x 8-10 reps
Romanian Deadlifts - 4 sets x 10 reps
Leg Press - 3 sets x 12 reps
Leg Curls - 3 sets x 12 reps
Calf Raises - 4 sets x 15 reps
Abs Rollout - 3 sets x 10 reps''',
            
            'Thursday': '''PUSH DAY
Dumbbell Bench Press - 4 sets x 10 reps
Cable Flyes - 3 sets x 12 reps
Arnold Press - 4 sets x 10 reps
Front Raises - 3 sets x 12 reps
Close Grip Bench - 3 sets x 10 reps
Cable Tricep Pushdowns - 3 sets x 15 reps''',
            
            'Friday': '''PULL DAY
Weighted Pull-ups - 4 sets x 6-8 reps
T-Bar Rows - 4 sets x 10 reps
Lat Pulldowns - 3 sets x 12 reps
Rear Delt Flyes - 3 sets x 15 reps
Preacher Curls - 3 sets x 10 reps
Cable Curls - 3 sets x 12 reps''',
            
            'Saturday': '''LEG DAY
Front Squats - 4 sets x 8 reps
Bulgarian Split Squats - 3 sets x 10 reps per leg
Leg Extensions - 3 sets x 15 reps
Walking Lunges - 3 sets x 12 reps per leg
Seated Calf Raises - 4 sets x 12 reps
Hanging Leg Raises - 3 sets x 12 reps''',
            
            'Sunday': 'Rest Day - Active recovery or light cardio'
        }
        
        for day, exercises in intermediate_days.items():
            WorkoutDay.objects.create(
                workout_plan=intermediate_workout,
                day_name=day,
                exercises=exercises
            )
        
        # 3. Advanced Athletic Performance
        advanced_workout = WorkoutPlan.objects.create(
            trainer=trainer,
            name='Advanced Athletic Performance Program',
            description='High-intensity program focusing on strength, power, and athletic performance. 6 days per week.',
            difficulty_level='advanced',
            is_default=True
        )
        
        advanced_days = {
            'Monday': '''STRENGTH - Lower Body
Back Squats - 5 sets x 5 reps (heavy)
Pause Squats - 3 sets x 5 reps
Deficit Deadlifts - 4 sets x 5 reps
Bulgarian Split Squats - 4 sets x 8 reps per leg
Nordic Curls - 3 sets x 8 reps
Weighted Planks - 3 sets x 45 seconds''',
            
            'Tuesday': '''STRENGTH - Upper Body
Bench Press - 5 sets x 5 reps (heavy)
Weighted Pull-ups - 5 sets x 5 reps
Overhead Press - 4 sets x 6 reps
Pendlay Rows - 4 sets x 6 reps
Dips - 3 sets x max reps
Pull-ups - 3 sets x max reps''',
            
            'Wednesday': '''POWER & CONDITIONING
Power Cleans - 5 sets x 3 reps
Box Jumps - 4 sets x 5 reps
Med Ball Slams - 4 sets x 10 reps
Battle Ropes - 4 sets x 30 seconds
Sprint Intervals - 8 x 100m
Core Circuit - 3 rounds''',
            
            'Thursday': '''HYPERTROPHY - Upper Body
Incline Bench Press - 4 sets x 10 reps
Cable Rows - 4 sets x 12 reps
Dumbbell Shoulder Press - 4 sets x 10 reps
Lat Pulldowns - 3 sets x 12 reps
Cable Flyes - 3 sets x 15 reps
Face Pulls - 3 sets x 20 reps
Arms Superset - 4 sets x 12 reps''',
            
            'Friday': '''HYPERTROPHY - Lower Body
Front Squats - 4 sets x 8 reps
Romanian Deadlifts - 4 sets x 10 reps
Hack Squats - 3 sets x 12 reps
Leg Curls - 4 sets x 12 reps
Walking Lunges - 3 sets x 12 per leg
Calf Circuit - 4 sets
Abs Circuit - 4 rounds''',
            
            'Saturday': '''FUNCTIONAL & MOBILITY
Turkish Get-ups - 3 sets x 3 per side
Kettlebell Swings - 5 sets x 15 reps
Single Leg Deadlifts - 3 sets x 10 per leg
Farmer's Walks - 4 sets x 50m
Sled Push/Pull - 5 sets
Mobility Work - 20 minutes''',
            
            'Sunday': 'Active Recovery - Swimming, yoga, or mobility work'
        }
        
        for day, exercises in advanced_days.items():
            WorkoutDay.objects.create(
                workout_plan=advanced_workout,
                day_name=day,
                exercises=exercises
            )
        
        # ===== DIET PLANS =====
        
        # 1. Muscle Gain Diet (3000 calories)
        muscle_gain = DietPlan.objects.create(
            trainer=trainer,
            name='Muscle Building Plan',
            description='High protein, high calorie plan designed for muscle growth. 3000 calories per day.',
            total_calories=3000,
            is_default=True
        )
        
        muscle_gain_days = {
            'Monday': {
                'breakfast': 'Oatmeal with banana, peanut butter, whey protein shake (650 cal)',
                'lunch': 'Grilled chicken breast, brown rice, mixed vegetables (800 cal)',
                'dinner': 'Beef steak, sweet potato, broccoli (850 cal)',
                'snacks': 'Greek yogurt, almonds, protein bar, apple (700 cal)'
            },
            'Tuesday': {
                'breakfast': '4 whole eggs, whole wheat toast, avocado (600 cal)',
                'lunch': 'Salmon fillet, quinoa, spinach salad (850 cal)',
                'dinner': 'Turkey meatballs, pasta, marinara sauce (800 cal)',
                'snacks': 'Cottage cheese, berries, mixed nuts (750 cal)'
            },
            'Wednesday': {
                'breakfast': 'Protein pancakes, banana, maple syrup (700 cal)',
                'lunch': 'Chicken thighs, basmati rice, chickpeas (850 cal)',
                'dinner': 'Lean ground beef, rice noodles, vegetables (800 cal)',
                'snacks': 'Protein shake, peanut butter sandwich (650 cal)'
            },
            'Thursday': {
                'breakfast': 'Scrambled eggs, bacon, hash browns, toast (750 cal)',
                'lunch': 'Tuna wrap, sweet potato fries, coleslaw (800 cal)',
                'dinner': 'Grilled lamb chops, couscous, roasted vegetables (850 cal)',
                'snacks': 'Greek yogurt parfait, protein bar, banana (600 cal)'
            },
            'Friday': {
                'breakfast': 'Breakfast burrito with eggs, cheese, beans (700 cal)',
                'lunch': 'Chicken pasta, caesar salad (850 cal)',
                'dinner': 'Pork chops, mashed potatoes, green beans (800 cal)',
                'snacks': 'Trail mix, apple with almond butter, protein shake (650 cal)'
            },
            'Saturday': {
                'breakfast': 'French toast, eggs, bacon, orange juice (750 cal)',
                'lunch': 'BBQ ribs, cornbread, coleslaw (900 cal)',
                'dinner': 'Stir-fry beef, jasmine rice, mixed vegetables (750 cal)',
                'snacks': 'Smoothie bowl, nuts, dark chocolate (600 cal)'
            },
            'Sunday': {
                'breakfast': 'Bagel with cream cheese, smoked salmon, eggs (700 cal)',
                'lunch': 'Chicken wings, rice, Caesar salad (850 cal)',
                'dinner': 'Fish tacos, beans, guacamole (750 cal)',
                'snacks': 'Protein ice cream, granola, berries (700 cal)'
            }
        }
        
        for day, meals in muscle_gain_days.items():
            DietDay.objects.create(
                diet_plan=muscle_gain,
                day_name=day,
                **meals
            )
        
        # 2. Fat Loss Diet (1800 calories)
        fat_loss = DietPlan.objects.create(
            trainer=trainer,
            name='Fat Loss Plan',
            description='Calorie deficit diet focusing on lean proteins and vegetables. 1800 calories per day.',
            total_calories=1800,
            is_default=True
        )
        
        fat_loss_days = {
            'Monday': {
                'breakfast': 'Egg white omelet, spinach, tomatoes, whole wheat toast (350 cal)',
                'lunch': 'Grilled chicken salad, olive oil dressing (450 cal)',
                'dinner': 'Baked cod, steamed broccoli, quinoa (500 cal)',
                'snacks': 'Apple, Greek yogurt, almonds (500 cal)'
            },
            'Tuesday': {
                'breakfast': 'Protein smoothie with berries, spinach, almond milk (300 cal)',
                'lunch': 'Turkey lettuce wraps, carrot sticks (400 cal)',
                'dinner': 'Lean beef, cauliflower rice, asparagus (550 cal)',
                'snacks': 'Celery with peanut butter, protein bar (550 cal)'
            },
            'Wednesday': {
                'breakfast': 'Oatmeal with berries, cinnamon (350 cal)',
                'lunch': 'Tuna salad, mixed greens, balsamic vinegar (400 cal)',
                'dinner': 'Grilled chicken breast, green beans, small sweet potato (550 cal)',
                'snacks': 'Cottage cheese, cucumber, cherry tomatoes (500 cal)'
            },
            'Thursday': {
                'breakfast': 'Scrambled egg whites, mushrooms, peppers (300 cal)',
                'lunch': 'Shrimp stir-fry with vegetables (450 cal)',
                'dinner': 'Turkey burger (no bun), side salad, roasted Brussels sprouts (500 cal)',
                'snacks': 'Protein shake, handful of berries (550 cal)'
            },
            'Friday': {
                'breakfast': 'Greek yogurt, granola, strawberries (350 cal)',
                'lunch': 'Chicken soup, side salad (400 cal)',
                'dinner': 'Grilled salmon, zucchini noodles, tomato sauce (550 cal)',
                'snacks': 'Rice cakes with almond butter, orange (500 cal)'
            },
            'Saturday': {
                'breakfast': 'Veggie omelet, half avocado (400 cal)',
                'lunch': 'Grilled chicken, mixed greens, quinoa (450 cal)',
                'dinner': 'Baked tilapia, roasted vegetables (450 cal)',
                'snacks': 'Protein bar, apple, string cheese (500 cal)'
            },
            'Sunday': {
                'breakfast': 'Protein pancakes (small serving), sugar-free syrup (350 cal)',
                'lunch': 'Chicken Caesar salad (light dressing) (450 cal)',
                'dinner': 'Lean pork tenderloin, steamed broccoli, brown rice (500 cal)',
                'snacks': 'Greek yogurt, walnuts, berries (500 cal)'
            }
        }
        
        for day, meals in fat_loss_days.items():
            DietDay.objects.create(
                diet_plan=fat_loss,
                day_name=day,
                **meals
            )
        
        # 3. Balanced Maintenance Diet (2400 calories)
        maintenance = DietPlan.objects.create(
            trainer=trainer,
            name='Balanced Maintenance Plan',
            description='Well-rounded diet for maintaining current weight and supporting fitness goals. 2400 calories per day.',
            total_calories=2400,
            is_default=True
        )
        
        maintenance_days = {
            'Monday': {
                'breakfast': 'Whole eggs, whole wheat toast, avocado, orange juice (550 cal)',
                'lunch': 'Chicken breast, brown rice, mixed vegetables (650 cal)',
                'dinner': 'Grilled salmon, quinoa, roasted asparagus (700 cal)',
                'snacks': 'Greek yogurt, granola, banana (500 cal)'
            },
            'Tuesday': {
                'breakfast': 'Oatmeal, protein powder, berries, almonds (500 cal)',
                'lunch': 'Turkey sandwich, apple, side salad (650 cal)',
                'dinner': 'Beef stir-fry, brown rice, vegetables (700 cal)',
                'snacks': 'Protein shake, mixed nuts, orange (550 cal)'
            },
            'Wednesday': {
                'breakfast': 'Scrambled eggs, bacon, whole wheat pancakes (600 cal)',
                'lunch': 'Chicken burrito bowl with rice, beans, salsa (700 cal)',
                'dinner': 'Baked cod, sweet potato, green beans (600 cal)',
                'snacks': 'Cottage cheese, crackers, berries (500 cal)'
            },
            'Thursday': {
                'breakfast': 'Protein smoothie bowl with granola, banana (550 cal)',
                'lunch': 'Tuna pasta salad, mixed greens (650 cal)',
                'dinner': 'Grilled chicken thighs, quinoa, broccoli (700 cal)',
                'snacks': 'Apple with peanut butter, protein bar (500 cal)'
            },
            'Friday': {
                'breakfast': 'French toast, eggs, turkey sausage (600 cal)',
                'lunch': 'Chicken wrap, vegetable soup (650 cal)',
                'dinner': 'Shrimp tacos, black beans, guacamole (650 cal)',
                'snacks': 'Greek yogurt parfait, almonds (500 cal)'
            },
            'Saturday': {
                'breakfast': 'Bagel with cream cheese, smoked salmon, eggs (600 cal)',
                'lunch': 'Grilled chicken pizza (homemade), side salad (700 cal)',
                'dinner': 'Pork chops, mashed sweet potato, Brussels sprouts (650 cal)',
                'snacks': 'Protein ice cream, banana (450 cal)'
            },
            'Sunday': {
                'breakfast': 'Pancakes, scrambled eggs, bacon, fruit salad (650 cal)',
                'lunch': 'Beef and vegetable stir-fry, rice noodles (700 cal)',
                'dinner': 'Roasted chicken, roasted potatoes, mixed vegetables (600 cal)',
                'snacks': 'Trail mix, protein shake (450 cal)'
            }
        }
        
        for day, meals in maintenance_days.items():
            DietDay.objects.create(
                diet_plan=maintenance,
                day_name=day,
                **meals
            )
        
        # 4. Vegetarian Muscle Gain (2800 calories)
        veg_muscle = DietPlan.objects.create(
            trainer=trainer,
            name='Vegetarian Muscle Building Plan',
            description='Plant-based high-protein diet for muscle growth. 2800 calories per day.',
            total_calories=2800,
            is_default=True
        )
        
        veg_muscle_days = {
            'Monday': {
                'breakfast': 'Tofu scramble, whole wheat toast, avocado (600 cal)',
                'lunch': 'Lentil curry, brown rice, naan bread (750 cal)',
                'dinner': 'Chickpea pasta, marinara sauce, nutritional yeast (700 cal)',
                'snacks': 'Protein smoothie, peanut butter, banana (750 cal)'
            },
            'Tuesday': {
                'breakfast': 'Protein oatmeal, berries, chia seeds, almond butter (650 cal)',
                'lunch': 'Black bean burger, sweet potato fries, salad (750 cal)',
                'dinner': 'Tempeh stir-fry, quinoa, mixed vegetables (700 cal)',
                'snacks': 'Greek yogurt, granola, nuts (700 cal)'
            },
            'Wednesday': {
                'breakfast': 'Protein pancakes, maple syrup, berries (600 cal)',
                'lunch': 'Falafel wrap, hummus, tabbouleh salad (750 cal)',
                'dinner': 'Tofu curry, basmati rice, spinach (750 cal)',
                'snacks': 'Cottage cheese, crackers, apple (700 cal)'
            },
            'Thursday': {
                'breakfast': 'Smoothie bowl with protein powder, granola, fruits (650 cal)',
                'lunch': 'Vegetable and bean burrito, guacamole, salsa (750 cal)',
                'dinner': 'Seitan stir-fry, brown rice, edamame (700 cal)',
                'snacks': 'Protein shake, trail mix, banana (700 cal)'
            },
            'Friday': {
                'breakfast': 'Egg scramble (or tofu), hash browns, beans (650 cal)',
                'lunch': 'Quinoa Buddha bowl with chickpeas, tahini dressing (750 cal)',
                'dinner': 'Lentil bolognese, whole wheat pasta (750 cal)',
                'snacks': 'Greek yogurt, almonds, dates (650 cal)'
            },
            'Saturday': {
                'breakfast': 'Protein waffles, nut butter, berries (600 cal)',
                'lunch': 'Paneer tikka, naan, rice, raita (800 cal)',
                'dinner': 'Black bean tacos, brown rice, guacamole (700 cal)',
                'snacks': 'Smoothie, protein bar, apple (700 cal)'
            },
            'Sunday': {
                'breakfast': 'Breakfast burrito with eggs, beans, cheese, avocado (700 cal)',
                'lunch': 'Vegetable lasagna, garlic bread, salad (750 cal)',
                'dinner': 'Stuffed bell peppers with quinoa, black beans (650 cal)',
                'snacks': 'Cottage cheese, berries, granola (700 cal)'
            }
        }
        
        for day, meals in veg_muscle_days.items():
            DietDay.objects.create(
                diet_plan=veg_muscle,
                day_name=day,
                **meals
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded 3 workout plans and 4 diet plans!'))
        self.stdout.write(self.style.SUCCESS('Workout Plans:'))
        self.stdout.write('  - Beginner Full Body Program')
        self.stdout.write('  - Intermediate Push/Pull/Legs Split')
        self.stdout.write('  - Advanced Athletic Performance Program')
        self.stdout.write(self.style.SUCCESS('Diet Plans:'))
        self.stdout.write('  - Muscle Building Plan (3000 cal)')
        self.stdout.write('  - Fat Loss Plan (1800 cal)')
        self.stdout.write('  - Balanced Maintenance Plan (2400 cal)')
        self.stdout.write('  - Vegetarian Muscle Building Plan (2800 cal)')
