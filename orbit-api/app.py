from flask import Flask, request, jsonify

app = Flask(__name__)

orbits = [
    {
    "id": 1,
    "text": "Good workout today",
    "mood": "happy",
    "created_at": "2026-03-10",
    "photo_url": None,
    },
    {
    "id": 2,
    "text": "Bad study time today",
    "mood": "sad",
    "created_at": "2026-03-10",
    "photo_url": None,
    },
    {
    "id": 4,
    "text": "Productive study time",
    "mood": "productive",
    "created_at": "2026-03-10",
    "photo_url": None,
    },
]


@app.route("/entries")
def entries():
    results = orbits 
    mood = request.args.get("mood")
    if mood: 
        results = [o for o in results if o["mood"] == mood]
    
    return jsonify(results)

@app.route("/entries/<int:entry_id>")
def get_entry(entry_id):
    entry = next((o for o in orbits if o["id"] == entry_id), None)

    if entry is None:
        return jsonify({"error": "Entry not found"}), 404
    
    return jsonify(entry)

@app.route("/entries", methods = ["POST"])
def create_entry():
    data = request.get_json()

    new_entry = {
        "id": max(o["id"] for o in orbits) + 1 if orbits else 1,
        "text": data.get("text"),
        "mood": data.get("mood"),
        "created_at": data.get("created_at"),
        "photo_url": data.get("photo_url"),
    }

    orbits.append(new_entry)

    return jsonify(new_entry), 201

@app.route("/entry/<int:entry_id>", methods = ["PATCH"])
def update_entry(entry_id):
    entry = next((o for o in orbits if o["id"] == entry_id), None)

    if entry is None:
        return jsonify({"error": "Entry not found"}), 404
    
    data = request.get_json()

    if not data: 
        return jsonify({"error": "No data provided"}), 400
    
    allowed_moods = {"happy", "sad", "productive", "calm", "stressed"}

    if "mood" in data:
        if data ["mood"] not in allowed_moods: 
            return jsonify({"error": "Invalid mood"}), 400
        entry["mood"] = data["mood"]

    if "text" in data:
        entry["text"] = data["text"]

    if "photo_url" in data:
        entry["photo_url"] = data["photo_url"]

    return jsonify(entry), 200

@app.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    global orbits

    entry = next((o for o in orbits if o["id"] == entry_id), None)

    if entry is None:
        return jsonify({"error": "Entry not found"}), 404

    orbits = [o for o in orbits if o["id"] != entry_id]

    return jsonify({"message": "Entry deleted"}), 200


if __name__ == '__main__':
    app.run(debug = True)