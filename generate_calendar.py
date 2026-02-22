import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import re

# ---- KONFIGURACJA ----
TEAMS = ["FaZe", "GamerLegion", "Ninjas in Pyjamas"]
CALENDAR_FILE = "matches.ics"
TIMEZONE = pytz.timezone("Europe/Warsaw")
REMINDER_MINUTES = 30

# ---- POBIERANIE STRONY ----
url = "https://www.hltv.org/matches"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# ---- ZBIERANIE TEKSTU Z HTML ----
text = soup.get_text(separator="\n")

lines = text.split("\n")

events = []

today = datetime.now(TIMEZONE)

for line in lines:
    # linie wyglądają np. "13:00 bo1 GamerLegion Phantom"
    m = re.match(r"(\d{1,2}:\d{2}) .+? (.+?) (.+)$", line.strip())
    if m:
        time_str = m.group(1)                # np. "13:00"
        team1 = m.group(2).strip()
        team2 = m.group(3).strip()

        if team1 in TEAMS or team2 in TEAMS:
            # budujemy datę meczu
            dt = datetime(today.year, today.month, today.day,
                          int(time_str.split(":")[0]),
                          int(time_str.split(":")[1]))
            dt = TIMEZONE.localize(dt)

            if dt < today:
                continue  # pomijamy mecze które już były

            end = dt + timedelta(hours=3)

            event = f"""BEGIN:VEVENT
SUMMARY:{team1} vs {team2}
DTSTART:{dt.strftime('%Y%m%dT%H%M%S')}
DTEND:{end.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:{url}
BEGIN:VALARM
TRIGGER:-PT{REMINDER_MINUTES}M
ACTION:DISPLAY
DESCRIPTION:Przypomnienie
END:VALARM
END:VEVENT
"""
            events.append(event)

calendar_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HLTV Calendar//EN
{''.join(events)}
END:VCALENDAR
"""

with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
    f.write(calendar_content)

print(f"Zapisano {len(events)} mecz(y) do {CALENDAR_FILE}")
