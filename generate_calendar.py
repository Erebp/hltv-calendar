import feedparser
from datetime import datetime, timedelta
import pytz

TEAMS = ["FaZe", "GamerLegion", "Ninjas in Pyjamas"]

feed = feedparser.parse("https://www.hltv.org/rss/matches")

events = []

for entry in feed.entries:
    for team in TEAMS:
        if team.lower() in entry.title.lower():

            match_time = datetime(*entry.published_parsed[:6])
            match_time = pytz.utc.localize(match_time)

            end_time = match_time + timedelta(hours=3)

            event = f"""BEGIN:VEVENT
SUMMARY:{entry.title}
DTSTART:{match_time.strftime('%Y%m%dT%H%M%SZ')}
DTEND:{end_time.strftime('%Y%m%dT%H%M%SZ')}
DESCRIPTION:{entry.link}
END:VEVENT
"""
            events.append(event)

calendar_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HLTV Calendar//EN
{''.join(events)}
END:VCALENDAR
"""

with open("matches.ics", "w", encoding="utf-8") as f:
    f.write(calendar_content)
