from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from ResistenciaCoC.models import War, Attack, Castle


# Troop names
troop_names = ['barbarian', 'archer', 'giant', 'goblin', 'wallbreaker', 'balloon', 'wizard', 'healer', 'dragon', 'pekka', 'minion', 'hog_rider', 'valkyrie', 'golem', 'witch', 'lava_hound']


def index(request):
    # Get current date and time.
    weekday = time.strftime('%A')
    hour = time.strftime('%H')

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

    else:
        # Just get the current war if there is any.
        current_war = War.objects.filter(ended=False)
        if current_war:
            current_war = current_war[0]

    # Check if some data was sent
    if request.method == 'POST':
        if request.POST['form-type'] == 'attacker':
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

        elif request.POST['form-type'] == 'castle':
            # Get the data
            attacker = request.POST['attacker']

            # Create the castle
            castle = Castle()

            for troop_name in troop_names:
                quantity = request.POST[troop_name + '_quantity']
                if not quantity:
                    quantity = 0
                else:
                    quantity = int(request.POST[troop_name + '_quantity'])

                setattr(castle, troop_name + '_level', int(request.POST[troop_name + '_level']))
                setattr(castle, troop_name + '_quantity', quantity)

            castle.save()

            # Check if there is a castle created by this attacker and override it.
            previous_attack = Attack.objects.filter(war=current_war, attacker=attacker)
            if previous_attack:
                if previous_attack[0].castle:
                    previous_attack[0].castle.delete()
                previous_attack[0].castle = castle
                previous_attack[0].save()
            else:
                # Create a new empty attack with this castle
                new_attack = Attack()
                new_attack.attacker = attacker
                new_attack.castle = castle
                new_attack.war = current_war
                new_attack.save()

    # Get template arguments
    args = {}
    if current_war:
        if not current_war.ended:
            # Get all the attacks in this war
            attacks = Attack.objects.filter(war=current_war)
            args['war'] = current_war
            args['weekday'] = current_war.date.strftime('%A')
            if attacks:
                args['attacks'] = attacks
            # args['troop_names'] = troop_names
        else:
            args['war'] = False

    return render(request, 'index.html', args)
