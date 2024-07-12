#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Description: Discord Bot with Google Calendar Integration

This project is a Discord bot designed to interact with Google Calendar, allowing users to fetch and create calendar events directly from a Discord server. The bot leverages Discord's slash commands for ease of use and integrates seamlessly with the Google Calendar API for robust event management. 

Key Features:
1. **Google Calendar Authentication**: Securely authenticate with Google Calendar using OAuth 2.0. Credentials are stored and refreshed as needed.
2. **Event Retrieval**: Fetch and display upcoming events from the primary Google Calendar in a well-formatted table.
3. **Event Creation**: Authorized users can create new calendar events by specifying the event summary, description, start time, and end time.
4. **Role-Based Access Control**: Ensure only users with specific roles can create events, maintaining control and security within the server.
5. **Pacific Time Zone Handling**: Events are handled in the 'America/Los_Angeles' time zone for accurate scheduling.

This bot facilitates efficient event management for communities using Discord, bridging the gap between real-time communication and calendar scheduling.

Created on Thu Jul 11 2024

@author: cod3iaks
"""
import discord
from discord.ext import commands
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tabulate import tabulate
import datetime
import os.path
import pytz

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Right click on a role to copy id and paste it here,
# could also be user id
ALLOWED_ROLE_ID = ALLOWED_ROLE_ID
# Enter the bot token ID
TOKEN = ''

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

# Authenticate Google Calendar
def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

# Fetch upcoming events from Google Calendar
def fetch_google_calendar_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=25, singleEvents=True, 
                                          orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    if not events:
        return 'No upcoming events found.'
    else:
        event_list = []
        for event in evetns:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = datetime.datetime.fromisocalendar(start.replace('Z', '+00:00'))
            event_list.append([start.strftime('%Y-%m-%d %H:%M:%S'), event['summary']])
        
        return tabulate(event_list, headers=["Start", "Event"], tablefmt="pretty")
    
# Create an event in Google Calendar
def create_google_calendar_event(service, summary, description, start_time, end_time):
    start_dt = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    end_dt = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

    western = pytz.timezone('America/Los_Angeles')
    start_dt = western.localize(start_dt)
    end_dt = western.localize(end_dt)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'datetime': start_dt.isoformat(),
            'timezone': 'America/Los_Angeles',
        },
        'end': {
            'datetime': end_dt.isoformat(),
            'timezone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

@bot.event
async def on_ready():
    print("Bot is up and running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="mcevent")
async def mcevent(interaction: discord.Interaction):
    service = authenticate_google_calendar()
    events_table = fetch_google_calendar_events(service)
    await interaction.channel.send(f'```{events_table}```')

@bot.tree.command(name="createmcevent")
async def createmcevent(interaction: discord.Interaction, summary: str, description: str, start_time: str, end_time: str):
    if ALLOWED_ROLE_ID in [role.id for role in interaction.user.roles]:
        service = authenticate_google_calendar()
        event = create_google_calendar_event(service, summary, description, start_time, end_time)
        await interaction.response.send_message(f'Event created: {event.get("htmlLink")}')
    else:
        await interaction.response.send_message('You do not have permission to use this command.', ephemeral=True)
    
bot.run(TOKEN)