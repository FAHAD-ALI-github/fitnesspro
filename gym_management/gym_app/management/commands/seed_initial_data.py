from django.core.management.base import BaseCommand
from gym_management.gym_app.models import Gender, MembershipPlan, Address, Gym_split, Muscle_strength

class Command(BaseCommand):
    help = 'Seed initial data for gym management system'

    def handle(self, *args, **kwargs):
        if not Gender.objects.exists():
            Gender.objects.create(gender='Male')
            Gender.objects.create(gender='Female')
            self.stdout.write(self.style.SUCCESS('Created genders'))
        
        if not MembershipPlan.objects.exists():
            MembershipPlan.objects.create(name='1 Month Plan', duration_months=1, price=2000)
            MembershipPlan.objects.create(name='3 Month Plan', duration_months=3, price=5500)
            MembershipPlan.objects.create(name='6 Month Plan', duration_months=6, price=10000)
            MembershipPlan.objects.create(name='12 Month Plan', duration_months=12, price=18000)
            self.stdout.write(self.style.SUCCESS('Created membership plans'))
        
        if not Address.objects.exists():
            addresses = ['Township', 'Johar Town', 'Model Town', 'Faisal Town', 'Green Town', 'Iqbal Town', 'Garden Town']
            for area in addresses:
                Address.objects.create(area=area)
            self.stdout.write(self.style.SUCCESS('Created addresses'))
        
        if not Gym_split.objects.exists():
            Gym_split.objects.create(split_name='5 Day Split')
            Gym_split.objects.create(split_name='3 Day Split')
            self.stdout.write(self.style.SUCCESS('Created gym splits'))
        
        if not Muscle_strength.objects.exists():
            Muscle_strength.objects.create(type='Beginner')
            Muscle_strength.objects.create(type='Intermediate')
            Muscle_strength.objects.create(type='Advanced')
            self.stdout.write(self.style.SUCCESS('Created muscle strength levels'))
        
        self.stdout.write(self.style.SUCCESS('Initial data seeded successfully!'))
