# Salom-Poq Telegram Bot

This repository contains a Telegram bot that:
- Provides weather and prayer times for Uzbek cities (OpenWeather + Aladhan APIs).
- Automatically replies on the owner's behalf when the owner is offline (away mode).
- Forwards incoming messages to the owner while in away mode.

Quick start
1. Create a virtual environment and install dependencies:

   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Set environment variables (create a .env or export variables):

   BOT_TOKEN=your_bot_token_here

   Optionally set WEATHER_API_KEY if you prefer not to keep it in code.

3. Run the bot:

   python main.py

Notes
- Owner commands (only owner can use):
  - /away — enable away mode (bot replies on your behalf)
  - /back — disable away mode
  - /setphone <phone> — set phone number shown in away reply
  - /status — show current away status and phone

- Bot stores its state in bot_state.json in the working directory.
- For group auto-reply, make sure the bot has permission to read messages (disable privacy mode in BotFather or make the bot admin in groups).
