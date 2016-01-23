from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from ResistenciaCoC.models import War, Attack


def index(request):
    # Get current date and time.
    weekday = time.strftime('%A')
    hour = time.strftime('%H')

    print (weekday)
    print (hour)

    current_war = None

    # If it's Friday at 22:00+, Saturday, Monday at 23:00+ or Tuesday, create a new war if there isn't any created.
    if weekday == 'Friday' and (hour == '22' or hour == '23') \
            or weekday == 'Saturday' \
            or weekday == 'Monday' and (hour == '23') \
            or weekday == 'Tuesday':

        print('Start war time!')
        # Check if there is a current war
        current_war = War.objects.filter(ended=False)
        if not current_war:
            # print('No war, a new one needs to be created!!')
            new_war = War()
            new_war.save()
            current_war = new_war
        else:
            # current_war is currently a queryset, so we take the first element.
            current_war = current_war[0]

    # If it's Sunday at 22:00+, Monday at 23:00-, Wednesday at 21:00+ o Thursday, end current war.
    elif weekday == 'Sunday' and (hour == '22' or hour == '23') \
            or weekday == 'Monday' and int(hour) < 23 \
            or weekday == 'Wednesday' and int(hour) >= 21 \
            or weekday == 'Thursday':

        print('End war time!')
        current_war = War.objects.filter(ended=False)
        if current_war:
            # current_war is currently a queryset, so we take the first element.
            current_war[0].ended = True
            current_war[0].save()

    # Check if some data was sent
    if request.method == 'POST':
        # Get the data
        attacker = request.POST['attacker']
        army = request.POST['army']

        # Create a new attack
        new_attack = Attack(attacker=attacker, army=army, war=current_war)

        # Check if there is an attack created by this attacker and override it.
        previous_attack = Attack.objects.filter(war=current_war, attacker=attacker)
        if previous_attack:
            previous_attack[0].army = army
            previous_attack[0].save()
        else:
            new_attack.save()

    # Get all the attacks in this war
    attacks = Attack.objects.filter(war=current_war)

    return render(request, 'index.html', {'war': current_war,
                                          'weekday': current_war.date.strftime('%A'),
                                          'attacks': attacks})
