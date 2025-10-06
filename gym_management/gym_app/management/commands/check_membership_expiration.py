from django.core.management.base import BaseCommand
from gym_management.gym_app.models import Gym_user
from gym_management.gym_app.utils import send_email
from datetime import datetime, timedelta
from django.utils import timezone

def check_and_notify_expiring_memberships():
    today = timezone.now().date()
    
    approved_users = Gym_user.objects.filter(is_approved=True, membership_end_date__isnull=False)
    
    for user in approved_users:
        if user.membership_end_date < today:
            if not user.is_blocked:
                user.is_blocked = True
                user.save()
                print(f"Blocked user: {user.username} (expired on {user.membership_end_date})")
        
        elif user.membership_end_date <= today + timedelta(days=7):
            if not user.reminder_sent and user.email:
                days_left = (user.membership_end_date - today).days
                
                subject = "Membership Expiring Soon - Renew Now"
                message = f"""Dear {user.first_name},

Your gym membership is expiring soon!

Membership expires in: {days_left} days
Expiry date: {user.membership_end_date.strftime('%B %d, %Y')}

Please renew your membership to continue enjoying our facilities.

If your membership expires, your profile will be blocked and you will need to register again with a new payment.

Thank you,
Gym Management Team"""
                
                result = send_email(user.email, subject, message)
                if result:
                    user.reminder_sent = True
                    user.save()
                    print(f"Sent reminder to: {user.email}")

class Command(BaseCommand):
    help = 'Check membership expiration and send reminders'

    def handle(self, *args, **options):
        self.stdout.write('Checking membership expiration...')
        check_and_notify_expiring_memberships()
        self.stdout.write(self.style.SUCCESS('Membership check completed!'))
