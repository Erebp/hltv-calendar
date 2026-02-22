import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

# --- KONFIGURACJA ---
TEAMS = ["FaZe", "G2", "NAVI"]  # <- tutaj wpisz swoje drużyny
CALENDAR_FILE = "matches.ics"
TIMEZONE = pytz.timezone("Europe/Warsaw")
REMINDER_MINUTES = 30  # przypomnienie przed meczem

# --- POBIERANIE STRONY HLTV ---
url = "https://www.hltv.org/matches"
headers = {
    "User-Agent": "Mozilla/5.0"
}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# --- TWORZENIE LISTY WYDARZEŃ ---
events = []

matches = soup.select(".upcomingMatch")  # selektor dla nadchodzących meczów
for match in matches:
    team_names = match.select(".matchTeamName")
    if len(team_names) < 2:
        continue

    t1, t2 = team_names[0].text.strip(), team_names[1].text.strip()
    if not any(team in TEAMS for team in [t1, t2]):
        continue  # pomiń jeśli żadna drużyna nie jest w TEAMS

    timestamp = match.get("data-zulu")
    if not timestamp:
        continue
    start_utc = datetime.fromtimestamp(int(timestamp), pytz.utc)
    start_local = start_utc.astimezone(TIMEZONE)
    if start_local < datetime.now(TIMEZONE):
        continue  # pomiń mecze w przeszłości
    end_local = start_local + timedelta(hours=3)

    event = f"""BEGIN:VEVENT
SUMMARY:{t1} vs {t2}
DTSTART:{start_local.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_local.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:https://www.hltv.org/matches
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
PRODID:-//HLTV Calendar//EN
{''.join(events)}
END:VCALENDAR
"""

with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
    f.write(calendar_content)

print(f"Zapisano {len(events)} mecz(y) do {CALENDAR_FILE}")
