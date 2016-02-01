from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from ResistenciaCoC.forms import RegistrationForm, LoginForm, CreateClanForm
from ResistenciaCoC.models import War, Attack, Castle

# Troop names
troop_names = ['barbarian', 'archer', 'giant', 'goblin', 'wall_breaker', 'balloon', 'wizard', 'healer', 'dragon',
               'pekka', 'minion', 'hog_rider', 'valkyrie', 'golem', 'witch', 'lava_hound']


def todo(request):
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
                quantity = request.POST.get(troop_name + '_quantity')
                print quantity
                if not quantity:
                    quantity = 0
                else:
                    quantity = int(quantity)
                # troop_max_needed = request.POST.get(troop_name + '_max_needed', False)
                setattr(castle, troop_name + '_max_needed', request.POST.get(troop_name + '_max_needed', False))
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

        elif request.POST['form-type'] == 'donor':
            print 'donor!'
            # Get the attack
            attack = Attack.objects.get(id=request.POST['attack-id'])
            attack.donor = request.POST['donor']
            attack.save()
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
        else:
            args['war'] = False

    return render(request, 'index.html', args)


@login_required
def index_logged_in(request):
    # Get user clan info
    user = request.user
    clan_member = user.clan_member.all()
    if clan_member.count() == 0:
        clan_membership = 'no_clan'
    else:
        clan_membership = clan_member
    return render(request, 'index_logged_in.html', {'clan_membership': clan_membership,
                                                    'user': user,})


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return index_logged_in(request)
            else:
                print"no"
    else:
        # Check if there is a logged in user
        if request.user.username != '':
            return index_logged_in(request)
        form = LoginForm()
    return render(request, 'index.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password.
            print form.cleaned_data
            new_user = form.instance
            new_user.password = make_password(new_user.password)
            new_user.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def create_clan(request):
    if request.method == 'POST':
        form = CreateClanForm(request.POST)
        if form.is_valid():
            # Save the clan
            new_clan = form.instance
            # The creator is the admin.
            new_clan.admin = request.user
            new_clan.save()
            # The creator is also a member! We need to do this after saving because many to many relationships.
            new_clan.members.add(request.user)
            new_clan.save()
            return index_logged_in(request)
    else:
        form = CreateClanForm()

    return render(request, 'create_clan.html', {'form': form})

def join_clan(request):
    return None