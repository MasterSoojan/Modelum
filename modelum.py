from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from PIL import Image, ImageDraw
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Ensure the static directory exists where images will be saved
if not os.path.exists("static"):
    os.makedirs("static")

def generate_house_blueprint(floors, rooms, sqft):
    """Generates a house blueprint image based on user input."""
    width, height = 600, 500
    img = Image.new("RGB", (width, height), "blue")
    draw = ImageDraw.Draw(img)

    margin = 40
    # Use max(val, 1) to prevent division by zero if inputs are 0
    room_width = (width - 2 * margin) // max(rooms, 1)
    room_height = (height - 2 * margin) // max(floors, 1)

    # Draw the rooms for each floor
    for floor in range(floors):
        for room in range(rooms):
            x1 = margin + room * room_width
            y1 = margin + floor * room_height
            x2 = x1 + room_width - 5
            y2 = y1 + room_height - 5
            draw.rectangle([x1, y1, x2, y2], outline="white", width=2)
            draw.text((x1 + 5, y1 + 5), f"R{room+1}F{floor+1}", fill="white")

    # Add a label with the details
    label = f"Floors: {floors}, Rooms/Floor: {rooms}, Size: {sqft} sqft"
    draw.text((20, height - 30), label, fill="white")

    # Save the generated image to the 'static' folder
    img.save("static/house_blueprint.png")

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/generate_house', methods=['POST'])
def generate_house():
    """API endpoint to generate and return the house blueprint."""
    try:
        data = request.json
        floors = int(data.get('floors', 1))
        rooms = int(data.get('rooms', 1))
        sqft = int(data.get('sqft', 100))
        
        generate_house_blueprint(floors, rooms, sqft)
        
        # Return the path to the newly created image
        return jsonify({"image": "/static/house_blueprint.png"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
