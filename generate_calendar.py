import requests
from datetime import datetime, timedelta
import pytz

# --- KONFIGURACJA ---
TEAMS = ["FaZe", "GamerLegion", "Ninjas in Pyjamas"]
CALENDAR_FILE = "matches.ics"
TIMEZONE = pytz.timezone("Europe/Warsaw")
REMINDER_MINUTES = 30

# --- POBIERANIE JSON Z HLTV API ---
url = "https://hltv-api.vercel.app/matches"
resp = requests.get(url)
data = resp.json()

events = []

now = datetime.now(TIMEZONE)

for match in data:
    t1 = match.get("team1")
    t2 = match.get("team2")
    time_str = match.get("date")

    # jeśli brak danych → pomiń
    if not (t1 and t2 and time_str):
        continue

    # filtrowanie pod drużyny
    if t1 not in TEAMS and t2 not in TEAMS:
        continue

    # parsowanie daty meczu
    match_time = datetime.fromisoformat(time_str).astimezone(TIMEZONE)

    # przeskocz jeśli mecz już był
    if match_time < now:
        continue

    end_time = match_time + timedelta(hours=3)

    event = f"""BEGIN:VEVENT
SUMMARY:{t1} vs {t2}
DTSTART:{match_time.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_time.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:https://hltv.org/matches
BEGIN:VALARM
TRIGGER:-PT{REMINDER_MINUTES}M
ACTION:DISPLAY
DESCRIPTION:Przypomnienie o meczu
END:VALARM
END:VEVENT
"""
    events.append(event)

calendar_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HLTV Calendar API//EN
{''.join(events)}
END:VCALENDAR
"""

with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
    f.write(calendar_content)

print(f"Zapisano {len(events)} mecz(y) do {CALENDAR_FILE}")
