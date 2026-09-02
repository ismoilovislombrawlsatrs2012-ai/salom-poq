# Deployment instructions

This document explains how to run the Salom-Poq bot using Docker (recommended) or systemd.

Using Docker (recommended)

1. Copy environment variables to a local .env file or export them in your shell:

   BOT_TOKEN=your_bot_token
   OWNER_ID=your_numeric_telegram_id
   WEATHER_API_KEY=your_openweather_key

2. Build and start with docker-compose:

   docker compose up -d --build

3. Check logs:

   docker compose logs -f

4. To stop:

   docker compose down

Using systemd (bare-metal install)

1. Place your code at /home/YOUR_USER/salom-poq (or another path). Update the systemd unit file at systemd/salom-poq.service replacing YOUR_USER and paths.

2. Copy the unit file to /etc/systemd/system/:

   sudo cp systemd/salom-poq.service /etc/systemd/system/salom-poq.service

3. Reload systemd and enable the service:

   sudo systemctl daemon-reload
   sudo systemctl enable --now salom-poq.service

4. Check status and logs:

   sudo systemctl status salom-poq.service
   sudo journalctl -u salom-poq.service -f

Notes and security
- Do not store BOT_TOKEN in a public repo. Use environment variables or a secrets manager.
- If using Docker on a server, make sure the firewall allows outbound HTTPS (APIs) and that the server's time is correct (for API timestamps).
- The bot stores runtime state in bot_state.json; ensure the container or host has write access to the working directory.
