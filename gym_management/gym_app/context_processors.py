from .models import Gym_user, Trainer

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
