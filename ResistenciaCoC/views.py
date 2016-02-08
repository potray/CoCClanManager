import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import time

from ResistenciaCoC.forms import RegistrationForm, LoginForm, CreateClanForm
from ResistenciaCoC.models import War, Attack, Castle, Clan, Member_request

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
            # The creator is also a manager.
            new_clan.managers.add(request.user)
            new_clan.save()
            return index_logged_in(request)
    else:
        form = CreateClanForm()

    return render(request, 'create_clan.html', {'form': form})


@login_required
def join_clan(request):
    args = {}
    error = 'none'
    if request.method == 'GET':
        # Check if a clan was searched.
        if 'search_clan' in request.GET:
            searched_clan = request.GET['search_clan']
            # Check if the clan tag is valid.
            if len(searched_clan) > 0:
                if len(searched_clan) != 8:
                    error = 'Invalid clan tag'
                else:
                    clan = Clan.objects.filter(tag=searched_clan)
                    if not clan:
                        error = 'There isn\'t any clan with this tag'
                    else:
                        args['clan'] = clan[0]
    args['error'] = error
    return render(request, 'join_clan.html', args)


@login_required
def clan(request):
    error = 'None'
    args = {}
    clan = Clan.objects.get(tag=request.GET['tag'])
    args['clan'] = clan

    if request.method == 'POST':
        form_type = request.POST['form_type']

        # Start the war.
        if form_type == 'start_war':
            clan.is_at_war = True
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI3ZTIzZjhhLWE1NzItNGJiYS05MmExLTVjMmMxNTQ3YWQxOSIsImlhdCI6MTQ1NDk2NjE4MCwic3ViIjoiZGV2ZWxvcGVyL2FjZjM1YTNkLWQyY2MtNmYzOC1jOTNmLTlmNmIzZWMyMWQ2YiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjU0LjIyOC4yMDguMTgyIiwiMTI3LjAuMC4xIl0sInR5cGUiOiJjbGllbnQifV19.z4KKAYUQ_VLHEOCF-fkta5cCzJlIxi_SS1sblPdvxogf8Efx697XbxEVI08yMcrdyLjKQtSgny_kdPso8RZiLQ"
            token2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZiMmE5OTNiLTRiNzgtNDhmZS1hZWJlLTAwZjVlNGJiOGZhMCIsImlhdCI6MTQ1NDk2Nzg3NSwic3ViIjoiZGV2ZWxvcGVyL2FjZjM1YTNkLWQyY2MtNmYzOC1jOTNmLTlmNmIzZWMyMWQ2YiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjIxNy4yMTYuODQuMjQ2Il0sInR5cGUiOiJjbGllbnQifV19.GjxKGPa75kBy4rNpjF_jaH-_CJ5PDM70xwDDJuXPvo20eX4-dJGcpOqOvcyvJAL0w4EJPxXkZ6IpOO3kLQQOCQ"
            quota_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjE1NzdkNzg2LTgzNGUtNGMxMC1hYzE4LTUyYmUwZWQwYjYzNyIsImlhdCI6MTQ1NDk2OTYzNCwic3ViIjoiZGV2ZWxvcGVyL2FjZjM1YTNkLWQyY2MtNmYzOC1jOTNmLTlmNmIzZWMyMWQ2YiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjU0LjE1NC4yMTguNjYiLCI1Mi4xNi4xMjEuMTMiXSwidHlwZSI6ImNsaWVudCJ9XX0.vr0uO4VHj7ryokQnO1WSpU41kyHF5IpBy5DllMOCmiRrUtyTQhNz_YP-X-lSrrCqvEWqQxeVlR-9rliDlkHFag"
            url = "https://api.clashofclans.com/v1/clans/%2390JL9JCQ?Authorization=Bearer%20"+quota_key
            r = requests.get(url)
            json = r.json()
            print json['name']
            args['clan_name'] = json['name']
            clan.save()

        # End the war.
        elif form_type == 'end_war':
            clan.is_at_war = False
            clan.save()

        # Join request.
        elif form_type == 'join_clan':
            # Check if there is a current member request
            if Member_request.objects.filter(clan=clan, user=request.user):
                error = 'You already sent a member request to this clan.'
            else:
                new_request = Member_request(clan=clan, user=request.user)
                new_request.save()

        # Manage member request
        elif form_type == 'member_request':
            request_id = request.POST['id']
            print request_id
            member_request = Member_request.objects.get(id=request_id)
            accepted = request.POST['accepted']
            if accepted == 'true':
                # Add member to the clan.
                clan.members.add(member_request.user)
                clan.save()
            # Delete the request
            member_request.delete()

    # Set the arguments depending on the privileges of the user.
    privileges = 'None'
    # Check if the user is a member of the clan.
    if request.user in clan.members.all():
        privileges = 'Member'
        # Check for manager and admin.
        if request.user in clan.managers.all():
            privileges = 'Manager'
            # Managers and admins have access to member requests.
            member_requests = Member_request.objects.filter(clan=clan)
            args['member_requests'] = member_requests
            if request.user == clan.admin:
                privileges = 'Administrator'

    # Set the final arguments.
    args['clan_members'] = clan.members.all().order_by('first_name')
    args['privileges'] = privileges
    args['error'] = error

    return render(request, 'clan.html', args)
