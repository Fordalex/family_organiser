from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from message.functions.functions import get_searched_users
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event, EventInvite
from .functions.functions import *

import datetime
import os
from os import path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
if path.exists('env.py'):
    import env
import json
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow

@login_required
def menu(request):
    """
    View all the users events, created or invited.
    """
    # Get all events the users has been invited to.
    all_events = Event.objects.all()
    events = []
    for event in all_events:
        if request.user in event.participants.all():
            events.append(event)

    events = add_count_down_to_events(events)

    context = {
        'events': events,
    }

    return render(request, 'event/menu.html', context)

@login_required
def create_event(request):
    """
    Create a new event and invite friends to the created event.
    """
    # Create the event.
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            event_form = form.save(commit=False)
            event_form.event_creator = request.user
            event_form.save()
            event_form.participants.add(request.user)

            return redirect('invite', event_form.pk, 0)

    context = {
        'create_event_form': EventForm,
    }

    return render(request, 'event/create_event.html', context)


@login_required
def invite(request, event_pk, user_pk):
    """
    Invite friends to an event passed into the view.
    """
    # Find the friends searched by the user.
    if request.method == 'GET':
        searched_users = get_searched_users(request)
    else:
        searched_users = []

    event = get_object_or_404(Event, pk=event_pk)
    invited_users = EventInvite.objects.filter(event=event)

    # Send invite to user.
    if request.method == 'POST':
        EventInvite.create_invitation(get_object_or_404(User, pk=user_pk), event)

    context = {
        'event': event,
        'searched_users': searched_users,
        'invited_users': invited_users,
    }

    return render(request, 'event/invite.html', context)


@login_required
def event(request, pk):
    """
    View the selected event and create messages on the page for only attendees to see.
    """

    event = Event.objects.get(pk=pk)
    event = add_count_down_to_events([event])

    context = {
        'event': event[0],
    }

    return render(request, 'event/event.html', context)


@login_required
def remove_event(request, pk):
    """
    Remove an event from the database.
    """

    event = get_object_or_404(Event, pk=pk)
    event.delete()

    return redirect('menu')

@login_required
def view_invite(request, pk):
    """
    View the invite page where the user can accept or decline the request.
    """

    context = {
        'event': get_object_or_404(Event, pk=pk)
    }

    return render(request, 'event/view_invite.html', context)

@login_required
def edit_invite(request, pk, operation):
    """
    Accepting or declining the event invitation.
    """

    if operation == 'accept':
        Event.participant_accepted(pk, request.user)
        return redirect('event', pk)

    if operation == 'decline':
        return redirect('profile')


# All the views to add the event to the google calendar api.

def authorise(request, event):
    """
    Authorise the appilcate with Oauth
    """
    print(event)

    event = json.loads(event)

    request.session['event'] = event

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    config = json.loads(os.environ['CRED'])

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
    config, SCOPES)

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://127.0.0.1:8001/event/oauth_2_call_back/'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    request.session['state'] = state

    return redirect(authorization_url)


def oauth_2_call_back(request):

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.session['state']

    config = json.loads(os.environ['CRED'])

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
    config, SCOPES, state=state)

    flow.redirect_uri = 'http://127.0.0.1:8001/event/oauth_2_call_back/'

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.get_full_path()

    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials


    service = build('calendar', 'v3', credentials=credentials)

    event_date = request.session['event']['date']
    event_start_time = request.session['event']['start_time']
    event_end_time = request.session['event']['end_time']

    # Call the Calendar API
    event = {
        'summary': request.session['event']['title'],
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': request.session['event']['description'],
        'start': {
            'dateTime': '{}T00:00:00-{}'.format(event_date, event_start_time),
            'timeZone': "Europe/London",
        },
        'end': {
            'dateTime': '{}T00:00:00-{}'.format(event_date, event_end_time),
            'timeZone': "Europe/London",
        },
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }

    event = service.events().insert(calendarId='primary', body=event).execute()
    # The url the the event on google calendar

    calendar_link = event.get('htmlLink') 
    

    return redirect('calendar_confirmed')


def calendar_confirmed(request):


    return render(request, 'event/calendar_confirmed.html')