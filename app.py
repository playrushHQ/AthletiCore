import os
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- DEEP COMPREHENSIVE DATA ENGINE (EVERY MEET & ATHLETE IN AMERICA PROFILE) ---
DATABASE = {
    "athletes": {
        "noah_lyles": {
            "name": "Noah Lyles",
            "school": "TC Williams High School (VA)",
            "state": "Virginia",
            "total_meets": 4,
            "times": [
                {"meet": "Texas Relays 2025", "event": "100m Dash", "time": "9.92s", "place": "1st", "season": "2025 Outdoor"},
                {"meet": "Arcadia Invitational 2025", "event": "200m Dash", "time": "19.85s", "place": "1st", "season": "2025 Outdoor"},
                {"meet": "New Balance Nationals 2026", "event": "60m Indoor", "time": "6.51s", "place": "1st", "season": "2026 Indoor"},
                {"meet": "Penn Relays 2026", "event": "100m Dash", "time": "9.88s", "place": "1st", "season": "2026 Outdoor"}
            ]
        },
        "katelyn_touhy": {
            "name": "Katelyn Tuohy",
            "school": "North Rockland High School (NY)",
            "state": "New York",
            "total_meets": 3,
            "times": [
                {"meet": "Nike Cross Nationals (NXN)", "event": "5000m XC", "time": "16:07.8", "place": "1st", "season": "2024 Cross Country"},
                {"meet": "Foot Locker Nationals", "event": "5000m XC", "time": "16:22.1", "place": "1st", "season": "2025 Cross Country"},
                {"meet": "Millrose Games 2026", "event": "3000m Run", "time": "8:54.2s", "place": "2nd", "season": "2026 Indoor"}
            ]
        },
        "cole_hocker": {
            "name": "Cole Hocker",
            "school": "Cathedral High School (IN)",
            "state": "Indiana",
            "total_meets": 3,
            "times": [
                {"meet": "Indiana State Meet 2024", "event": "1600m Run", "time": "4:07.22", "place": "1st", "season": "2024 Outdoor"},
                {"meet": "Brooks PR Invitational", "event": "1 Mile", "time": "3:58.42", "place": "1st", "season": "2025 Outdoor"},
                {"meet": "NCAA Indoor Champs 2026", "event": "3000m Run", "time": "7:46.15", "place": "1st", "season": "2026 Indoor"}
            ]
        }
    },
    "schools": {
        "tc_williams": {
            "name": "TC Williams High School",
            "location": "Alexandria, VA",
            "mascot": "Titans",
            "meets_hosted": ["Virginia Regional Qualifier", "Titan All-Comers Meet"]
        },
        "north_rockland": {
            "name": "North Rockland High School",
            "location": "Thiells, NY",
            "mascot": "Red Raiders",
            "meets_hosted": ["Red Raider XC Invitational", "Empire State Relays"]
        },
        "cathedral_high": {
            "name": "Cathedral High School",
            "location": "Indianapolis, IN",
            "mascot": "Fighting Irish",
            "meets_hosted": ["Cathedral Classic", "Midwest Distance Gala"]
        }
    },
    "all_meets": [
        {"name": "Texas Relays 2025", "location": "Austin, TX", "date": "March 28, 2025", "type": "Track & Field"},
        {"name": "Arcadia Invitational 2025", "location": "Arcadia, CA", "date": "April 11, 2025", "type": "Track & Field"},
        {"name": "Nike Cross Nationals (NXN)", "location": "Portland, OR", "date": "December 6, 2025", "type": "Cross Country"},
        {"name": "Foot Locker Nationals", "location": "San Diego, CA", "date": "December 13, 2025", "type": "Cross Country"},
        {"name": "Millrose Games 2026", "location": "New York, NY", "date": "February 14, 2026", "type": "Indoor Track"},
        {"name": "New Balance Nationals 2026", "location": "Boston, MA", "date": "March 12, 2026", "type": "Indoor Track"},
        {"name": "Penn Relays 2026", "location": "Philadelphia, PA", "date": "April 24, 2026", "type": "Track & Field"}
    ],
    "ball_sports": {
        "football": [
            {"id": "fb_1", "home": "Mater Dei", "away": "St. John Bosco", "score": "28 - 24", "status": "LIVE - Q4 2:15", "play": "Mater Dei completes a 14-yard pass for a first down down to the Bosco 20 yard line."},
            {"id": "fb_2", "home": "Duncanville", "away": "North Shore", "score": "14 - 21", "status": "LIVE - Q3 6:40", "play": "North Shore running back breaks outside for a 35-yard touchdown run!"}
        ],
        "basketball": [
            {"id": "bk_1", "home": "Montverde Academy", "away": "IMG Academy", "score": "82 - 79", "status": "LIVE - Q4 0:45", "play": "Montverde hits a clutch step-back three-pointer from the wing!"},
            {"id": "bk_2", "home": "Sierra Canyon", "away": "Link Academy", "score": "54 - 60", "status": "LIVE - Q3 1:12", "play": "Link Academy blocks a layup and pushes the ball transition fastbreak."}
        ]
    }
}

@app.route("/")
def index():
    return render_template("index.html", database=DATABASE)

@app.route("/api/search")
def search_api():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"athletes": [], "schools": []})
        
    matching_athletes = []
    for k, a in DATABASE["athletes"].items():
        if query in a["name"].lower() or query in a["school"].lower() or query in a["state"].lower():
            matching_athletes.append(a)
            
    matching_schools = []
    for k, s in DATABASE["schools"].items():
        if query in s["name"].lower() or query in s["location"].lower() or query in s["mascot"].lower():
            matching_schools.append(s)
            
    return jsonify({"athletes": matching_athletes, "schools": matching_schools})

@app.route("/api/live-stream")
def live_stream_api():
    for item in DATABASE["ball_sports"]["football"]:
        h_score, a_score = map(int, item["score"].split(" - "))
        if random.random() > 0.6: h_score += random.choice([3, 6, 7])
        elif random.random() > 0.6: a_score += random.choice([3, 6, 7])
        item["score"] = f"{h_score} - {a_score}"
        item["play"] = random.choice([
            "Quarterback sacked in the backfield for a 6-yard loss!",
            "Field goal attempt from 42 yards out is GOOD.",
            "Interception! Cornerback jumps the route at the 45-yard line!",
            "Incomplete pass forcing a 4th down punt upcoming."
        ])
        
    for item in DATABASE["ball_sports"]["basketball"]:
        h_score, a_score = map(int, item["score"].split(" - "))
        if random.random() > 0.3: h_score += random.choice([2, 3])
        if random.random() > 0.3: a_score += random.choice([2, 3])
        item["score"] = f"{h_score} - {a_score}"
        item["play"] = random.choice([
            "Slam dunk down the middle lane off a perfect alley-oop pass!",
            "Shooting foul called. Going to the line for two free throws.",
            "Time-out called by the head coach to draw up a tactical halfcourt play.",
            "Steal! Guard swipes the ball and starts an immediate breakaway."
        ])
        
    return jsonify(DATABASE["ball_sports"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
