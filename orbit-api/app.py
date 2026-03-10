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
        results = [o for o in results]
    
    return jsonify(results)

@app.route("/entries/<int:entry_id>")
def get_entry(entry_id):
    entry = next((o for o in orbits if o["id"] == entry_id), None)

    if entry is None:
        return jsonify({"error": "Entry not found"}), 404
    
    return jsonify(entry)

if __name__ == '__main__':
    app.run(debug = True)