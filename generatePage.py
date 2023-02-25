
import requests

sessions = requests.get("https://events.ethdenver.com/__event/aaff48cd-46ca-46ba-bdb1-0a5aa5eb00e3/api/sessions.json?meta=true&attendee_member_token=f47c95ca-c959-4649-aa45-5ef0747f84e4&ignore_session_restrictions=false&include_media_options=true").json()
venues = requests.get("https://events.ethdenver.com/__event/aaff48cd-46ca-46ba-bdb1-0a5aa5eb00e3/api/rooms.json?meta=true").json()
rooms = {}

events = []

for venue in venues: 
  rooms[venue["id"]] = venue["name"]

fout = open("ethdenver2023schedule.md", "w");
fout.write("""
# Eth Denver 2023 Schedule
| Event Name | Description | Venue | Time | Date | Add to Calendar |
| ---------- | ----------- | ------ | ----| ----- | ---------------|
""")

for session in sessions:
  if len(session["instances"]) == 0:
    continue
  instance = session["instances"][0]
  event = {"name":session["name"], "description":session["description"], "room":rooms[instance["room_id"]], "start_time": instance["time"], "end_time": instance["end_time"], "tz": instance["time_zone_offset"], "date": instance["date"]}
  google_url = "https://www.google.com/calendar/render?action=TEMPLATE&text="+event["name"]+"&dates="+event["date"].replace("-","")+"T"+event["start_time"].replace(":","")+"00Z"+event["tz"]+"/"+event["date"].replace("-","")+"T"+event["end_time"].replace(":","")+"00Z"+event["tz"]
  fout.write("|"+event["name"]+"|"+event["description"]+"|"+event["room"]+"|"+event["start_time"]+"|"+event["date"]+"|[Add to Cal]("+google_url+")|\n")

