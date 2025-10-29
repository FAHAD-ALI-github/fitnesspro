from .models import Gym_user, Trainer, GymInfo
import os


def logged_in_user(request):
    user = None
    trainer = None

    if request.session.get('user_id'):
        try:
            user = Gym_user.objects.get(id=request.session['user_id'])
        except Gym_user.DoesNotExist:
            user = None
    elif request.session.get('trainer_id'):
        try:
            trainer = Trainer.objects.get(id=request.session['trainer_id'])
        except Trainer.DoesNotExist:
            trainer = None

    return {'logged_in_user': user, 'logged_in_trainer': trainer}


# Context processor to provide gym information globally

def gym_info_context(request):
    """
    Context processor to make gym_info available to all templates
    """
    gym_info = GymInfo.objects.first()
    return {
        'gym_info': gym_info
    }



def formspree_id(request):
    return {"FORMSPREE_ID": os.getenv("FORMSPREE_ID")}
