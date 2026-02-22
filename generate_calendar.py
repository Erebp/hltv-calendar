from datetime import datetime, timedelta
import pytz

CALENDAR_FILE = "matches.ics"
TIMEZONE = pytz.timezone("Europe/Warsaw")
REMINDER_MINUTES = 30

# --- PRZYKŁADOWE MECZE ---
matches = [
    {"team1": "FaZe", "team2": "GamerLegion", "hour": 18, "minute": 0},
    {"team1": "GamerLegion", "team2": "Ninjas in Pyjamas", "hour": 20, "minute": 30},
    {"team1": "FaZe", "team2": "Ninjas in Pyjamas", "hour": 22, "minute": 0},
]

events = []
today = datetime.now(TIMEZONE)

for m in matches:
    start = TIMEZONE.localize(datetime(today.year, today.month, today.day, m["hour"], m["minute"]))
    end = start + timedelta(hours=3)
    event = f"""BEGIN:VEVENT
SUMMARY:{m['team1']} vs {m['team2']}
DTSTART:{start.strftime('%Y%m%dT%H%M%S')}
DTEND:{end.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:Przykładowy mecz
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
PRODID:-//HLTV Calendar Static//EN
{''.join(events)}
END:VCALENDAR
"""

with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
    f.write(calendar_content)

print(f"Zapisano {len(events)} mecz(y) do {CALENDAR_FILE}")
