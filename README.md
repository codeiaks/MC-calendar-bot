# MC-calendar-bot

# Discord Bot with Google Calendar Integration

This project is a Discord bot designed to interact with Google Calendar, allowing users to fetch and create calendar events directly from a Discord server. The bot leverages Discord's slash commands for ease of use and integrates seamlessly with the Google Calendar API for robust event management.

## Key Features

1. **Google Calendar Authentication**: Securely authenticate with Google Calendar using OAuth 2.0. Credentials are stored and refreshed as needed.
2. **Event Retrieval**: Fetch and display upcoming events from the primary Google Calendar in a well-formatted table.
3. **Event Creation**: Authorized users can create new calendar events by specifying the event summary, description, start time, and end time.
4. **Role-Based Access Control**: Ensure only users with specific roles can create events, maintaining control and security within the server.
5. **Pacific Time Zone Handling**: Events are handled in the 'America/Los_Angeles' time zone for accurate scheduling.

This bot facilitates efficient event management for communities using Discord, bridging the gap between real-time communication and calendar scheduling.

## Prerequisites

- Python 3.7 or higher
- Discord.py library
- Google API Python Client
- Tabulate library
- OAuth2Client library

## Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/codeiaks/MC-calendar-bot.git
   cd MC-calendar-bot
   ```

2. **Install dependencies**:

   Create and activate a virtual environment (optional):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

   Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. **Create and configure your Google API credentials**:

   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the `credentials.json` file and place it in the root directory of your project

4. **Obtain Discord bot token**:

   - Create a new Discord bot and obtain the token. Follow the instructions on the [Discord Developer Portal](https://discord.com/developers/docs/intro).
   - Replace `TOKEN` with your bot token
   - Replace `ALLOWED_ROLE_ID` with the role ID that is allowed to create events

## Usage

1. **Run the bot**:

   ```sh
   python mc-calendar-bot.py
   ```

2. **Authenticate Google Calendar**:

   The first time you run the bot, you will need to authenticate with Google Calendar. Follow the instructions in the console to complete the authentication process. The credentials will be saved in `token.json`.

3. **Commands**:

   - **/mcevent**: Fetch and display upcoming events from the primary Google Calendar.
   - **/createmcevent [summary] [description] [start_time] [end_time]**: Create a new event in the Google Calendar (requires the user to have the specified role).

## Example

1. Fetch upcoming events:

   ```sh
   /mcevent
   ```

2. Create a new event (if you have the required role):

   ```sh
   /createmcevent "Meeting" "Discuss project updates" "2024-07-15T10:00" "2024-07-15T11:00"
   ```

## Contributing

- Feel free to contribute to this project! Fork the repository and submit a pull request with your changes.
