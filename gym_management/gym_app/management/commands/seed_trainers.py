from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gym_management.gym_app.models import Trainer, WorkoutPlan, DietPlan, WorkoutDay, DietDay

class Command(BaseCommand):
    help = "Seeds the database with 3 experienced Pakistani trainers and comprehensive fitness plans."

    def handle(self, *args, **options):
        trainers_data = [
            {
                "first_name": "Muhammad",
                "last_name": "Asad",
                "email": "masad@elitepakfitness.com",
                "phone_number": "03001234567",
                "username": "masad_elite",
                "password": "trainer123",
                "specialization": "Strength & Conditioning",
                "experience_years": 8,
                "bio": "Certified strength coach with 8 years of experience training athletes and fitness enthusiasts across Pakistan."
            },
            {
                "first_name": "Abdullah",
                "last_name": "Khan",
                "email": "akhan@elitepakfitness.com",
                "phone_number": "03121234567",
                "username": "akhan_transform",
                "password": "trainer123",
                "specialization": "Weight Loss & Body Transformation",
                "experience_years": 6,
                "bio": "Nutrition specialist and personal trainer focused on sustainable weight management and lifestyle changes."
            },
            {
                "first_name": "Usman",
                "last_name": "Ahmed",
                "email": "uahmed@elitepakfitness.com",
                "phone_number": "03331234567",
                "username": "uahmed_muscle",
                "password": "trainer123",
                "specialization": "Bodybuilding & Muscle Hypertrophy",
                "experience_years": 7,
                "bio": "Professional bodybuilder and certified trainer specializing in muscle growth and competition preparation."
            }
        ]

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Workout plan templates by category
        workout_templates = {
            "beginner": {
                "Monday": "Chest & Triceps\n• Push-ups – 3x12\n• Dumbbell Chest Press – 3x10\n• Tricep Dips – 3x8\n• Overhead Dumbbell Extension – 3x12\n• Cardio – 15 min walk",
                "Tuesday": "Back & Biceps\n• Lat Pulldowns – 3x12\n• Dumbbell Rows – 3x10\n• Bicep Curls – 3x12\n• Hammer Curls – 3x10\n• Plank – 3x30s",
                "Wednesday": "Rest or Light Cardio\n• Walking – 20-30 minutes\n• Stretching – 10 minutes",
                "Thursday": "Legs & Core\n• Bodyweight Squats – 3x15\n• Lunges – 3x10 each leg\n• Leg Press – 3x12\n• Crunches – 3x15\n• Bicycle Crunches – 3x20",
                "Friday": "Shoulders & Arms\n• Dumbbell Shoulder Press – 3x10\n• Lateral Raises – 3x12\n• Front Raises – 3x12\n• Arm Circles – 2x20\n• Cardio – 15 min",
                "Saturday": "Full Body Circuit\n• Jumping Jacks – 3x20\n• Bodyweight Squats – 3x15\n• Push-ups – 3x10\n• Mountain Climbers – 3x15\n• Cool down stretching",
                "Sunday": "Rest Day\n• Complete rest or light stretching\n• Focus on recovery and hydration"
            },
            "intermediate": {
                "Monday": "Chest & Triceps\n• Barbell Bench Press – 4x10\n• Incline Dumbbell Press – 4x10\n• Cable Flyes – 3x12\n• Close-Grip Bench Press – 4x10\n• Tricep Pushdowns – 3x12\n• Overhead Tricep Extension – 3x12",
                "Tuesday": "Back & Biceps\n• Deadlifts – 4x8\n• Pull-ups – 4x8\n• Barbell Rows – 4x10\n• Cable Rows – 3x12\n• Barbell Curls – 4x10\n• Hammer Curls – 3x12",
                "Wednesday": "Rest or Active Recovery\n• Light cardio 20-30 min\n• Stretching and mobility work\n• Foam rolling",
                "Thursday": "Legs & Glutes\n• Barbell Squats – 4x10\n• Romanian Deadlifts – 4x10\n• Leg Press – 4x12\n• Leg Curls – 3x12\n• Calf Raises – 4x15\n• Walking Lunges – 3x12 each",
                "Friday": "Shoulders & Core\n• Military Press – 4x10\n• Lateral Raises – 4x12\n• Rear Delt Flyes – 3x12\n• Face Pulls – 3x15\n• Planks – 3x60s\n• Russian Twists – 3x20",
                "Saturday": "Arms & Conditioning\n• Barbell Curls – 4x10\n• Skull Crushers – 4x10\n• Concentration Curls – 3x12\n• Rope Pushdowns – 3x15\n• HIIT Cardio – 20 min",
                "Sunday": "Rest Day\n• Complete rest\n• Meal prep for the week\n• Recovery and sleep"
            },
            "advanced": {
                "Monday": "Chest & Triceps (Heavy)\n• Barbell Bench Press – 5x5 (heavy)\n• Incline Barbell Press – 4x8\n• Weighted Dips – 4x8\n• Cable Crossovers – 4x12\n• Close-Grip Bench – 4x8\n• Tricep Rope Pushdowns – 4x12\n• Overhead Extensions – 3x12",
                "Tuesday": "Back & Biceps (Volume)\n• Deadlifts – 5x5 (heavy)\n• Weighted Pull-ups – 4x8\n• Barbell Rows – 4x8\n• T-Bar Rows – 4x10\n• Cable Rows – 3x12\n• Barbell Curls – 4x10\n• Preacher Curls – 3x12\n• Hammer Curls – 3x12",
                "Wednesday": "Legs (Heavy)\n• Barbell Squats – 5x5 (heavy)\n• Front Squats – 4x8\n• Romanian Deadlifts – 4x8\n• Leg Press – 4x12\n• Leg Extensions – 3x15\n• Leg Curls – 3x15\n• Calf Raises – 5x15",
                "Thursday": "Shoulders & Traps\n• Standing Military Press – 5x5\n• Dumbbell Shoulder Press – 4x10\n• Lateral Raises – 4x12\n• Rear Delt Flyes – 4x12\n• Upright Rows – 3x12\n• Barbell Shrugs – 4x12\n• Face Pulls – 3x15",
                "Friday": "Arms & Core\n• Barbell Curls – 4x10\n• Skull Crushers – 4x10\n• Incline Curls – 4x12\n• Overhead Tricep Extension – 4x12\n• Cable Curls – 3x15\n• Tricep Kickbacks – 3x15\n• Weighted Planks – 4x60s\n• Hanging Leg Raises – 4x15",
                "Saturday": "Full Body Power\n• Power Cleans – 4x6\n• Front Squats – 4x8\n• Weighted Pull-ups – 4x6\n• Push Press – 4x8\n• Farmers Walk – 4x40m\n• Battle Ropes – 4x30s",
                "Sunday": "Active Recovery\n• Light cardio 30 min\n• Yoga or stretching 20 min\n• Foam rolling\n• Sauna/steam (optional)"
            },
            "weight_loss": {
                "Monday": "Upper Body + Cardio\n• Push-ups – 4x15\n• Dumbbell Rows – 4x12\n• Shoulder Press – 3x12\n• Bicep Curls – 3x15\n• Tricep Dips – 3x12\n• HIIT Cardio – 20 min\n• Cool down – 5 min",
                "Tuesday": "Lower Body + Core\n• Squats – 4x15\n• Lunges – 4x12 each\n• Step-ups – 3x15 each\n• Leg Curls – 3x15\n• Planks – 3x45s\n• Mountain Climbers – 3x20\n• Steady Cardio – 30 min",
                "Wednesday": "Cardio & Core Focus\n• Treadmill Intervals – 30 min\n• Bicycle Crunches – 4x20\n• Russian Twists – 3x20\n• Leg Raises – 3x15\n• Plank to Push-up – 3x10\n• Jump Rope – 10 min",
                "Thursday": "Full Body Circuit\n• Burpees – 4x10\n• Kettlebell Swings – 4x15\n• Box Jumps – 3x12\n• Battle Ropes – 3x30s\n• Medicine Ball Slams – 3x15\n• Rowing Machine – 15 min",
                "Friday": "Upper Body + HIIT\n• Bench Press – 4x12\n• Lat Pulldowns – 4x12\n• Dumbbell Flyes – 3x12\n• Cable Rows – 3x12\n• Face Pulls – 3x15\n• HIIT Sprints – 20 min",
                "Saturday": "Active Recovery + Long Cardio\n• Brisk Walking – 45 min\n• Swimming (optional) – 20 min\n• Stretching – 15 min\n• Light yoga",
                "Sunday": "Rest Day\n• Complete rest\n• Meal prep\n• Focus on hydration"
            }
        }

        # Diet plan templates by category
        diet_templates = {
            "beginner": {
                "calories": 2000,
                "breakfast": "3 egg omelette with vegetables, 2 whole wheat parathas, green tea",
                "lunch": "Grilled chicken breast (150g), brown rice (1 cup), mixed vegetables, cucumber raita",
                "dinner": "Baked fish or chicken (120g), sweet potato, green salad with olive oil",
                "snacks": "Apple with peanut butter, handful of almonds, protein shake (if needed)"
            },
            "intermediate": {
                "calories": 2400,
                "breakfast": "4 egg whites + 2 whole eggs, oatmeal with banana and honey, black coffee",
                "lunch": "Grilled chicken (180g), quinoa or brown rice (1.5 cups), vegetables, lentil soup",
                "dinner": "Lean beef or fish (150g), roasted vegetables, mixed green salad, 1 chapati",
                "snacks": "Greek yogurt with berries, protein shake, almonds and walnuts (30g)"
            },
            "advanced": {
                "calories": 2800,
                "breakfast": "6 egg whites + 2 whole eggs, oatmeal (1 cup) with berries and nuts, protein shake",
                "lunch": "Grilled chicken breast (200g), brown rice (2 cups), vegetables, chickpea salad",
                "dinner": "Lean beef or salmon (180g), sweet potato (medium), broccoli, spinach salad",
                "snacks": "Protein shake (2 scoops), Greek yogurt with granola, mixed nuts (40g), banana with peanut butter"
            },
            "weight_loss": {
                "calories": 1800,
                "breakfast": "3 egg white omelette with spinach and tomatoes, 1 whole wheat toast, green tea",
                "lunch": "Grilled chicken (120g), small portion brown rice (0.5 cup), large mixed salad, lemon water",
                "dinner": "Grilled fish (130g), steamed vegetables, small sweet potato, green salad",
                "snacks": "Apple, carrot sticks with hummus, green tea, handful of almonds (15g)"
            },
            "muscle_gain": {
                "calories": 3000,
                "breakfast": "6 whole eggs scrambled, oatmeal (1.5 cups) with banana and honey, protein shake, orange juice",
                "lunch": "Grilled chicken or beef (250g), brown rice (2 cups), vegetables, lentils, whole wheat naan",
                "dinner": "Salmon or lean beef (200g), quinoa (1.5 cups), roasted vegetables, avocado salad",
                "snacks": "Protein shake (2 scoops), Greek yogurt with granola and berries, mixed nuts (50g), peanut butter sandwich, dates"
            }
        }

        for data in trainers_data:
            trainer, created = Trainer.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "phone_number": data["phone_number"],
                    "password": make_password(data["password"]),
                    "specialization": data["specialization"]
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created trainer: {trainer.first_name} {trainer.last_name} ({data['experience_years']} years exp)"))

                # Create multiple workout plans for different categories
                categories = ["beginner", "intermediate", "advanced", "weight_loss"]
                
                for category in categories:
                    workout_plan = WorkoutPlan.objects.create(
                        trainer=trainer,
                        name=f"{category.title()} - {trainer.first_name}'s {trainer.specialization} Program",
                        description=f"A comprehensive {category} level program designed by {trainer.first_name} with {data['experience_years']} years of experience. Suitable for {category} athletes and fitness enthusiasts.",
                        difficulty_level=category if category in ["beginner", "intermediate", "advanced"] else "intermediate",
                        is_default=(category == "intermediate")
                    )

                    # Add workout days for this category
                    for day in days_of_week:
                        WorkoutDay.objects.create(
                            workout_plan=workout_plan,
                            day_name=day,
                            exercises=workout_templates[category][day],
                            notes=f"Focus on proper form. Rest 60-90 seconds between sets. Stay hydrated."
                        )

                    self.stdout.write(self.style.SUCCESS(f"  📋 Created {category} workout plan for {trainer.first_name}"))

                # Create multiple diet plans for different categories
                diet_categories = ["beginner", "intermediate", "advanced", "weight_loss", "muscle_gain"]
                
                for category in diet_categories:
                    diet_plan = DietPlan.objects.create(
                        trainer=trainer,
                        name=f"{category.title().replace('_', ' ')} - {trainer.first_name}'s Nutrition Plan",
                        description=f"A balanced {category.replace('_', ' ')} nutrition plan by {trainer.first_name}. {diet_templates[category]['calories']} calories daily.",
                        total_calories=diet_templates[category]["calories"],
                        is_default=(category == "intermediate")
                    )

                    # Add diet days
                    for day in days_of_week:
                        DietDay.objects.create(
                            diet_plan=diet_plan,
                            day_name=day,
                            breakfast=diet_templates[category]["breakfast"],
                            lunch=diet_templates[category]["lunch"],
                            dinner=diet_templates[category]["dinner"],
                            snacks=diet_templates[category]["snacks"]
                        )

                    self.stdout.write(self.style.SUCCESS(f"  🍽️  Created {category} diet plan for {trainer.first_name}"))

            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Trainer '{trainer.username}' already exists — skipped."))

        self.stdout.write(self.style.SUCCESS("\n🎯 Trainer seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS(f"📊 Created {len(trainers_data)} trainers with multiple workout and diet plans each."))