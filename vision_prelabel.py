import json
import base64
import os
from PIL import Image

def encode_image_to_base64(image_path):
    """Converts a local image into a base64 data string for native Label Studio parsing."""
    try:
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        # Format explicitly as a data URI string
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def calculate_ls_percentages(pixel_box, img_width, img_height):
    """
    Translates standard CV pixel coordinates [xmin, ymin, xmax, ymax]
    into Label Studio's strict 0-100 percentage system [x, y, width, height].
    """
    xmin, ymin, xmax, ymax = pixel_box
    
    # Calculate box width and height in pixels
    box_w = xmax - xmin
    box_h = ymax - ymin
    
    # Convert to 0-100 percentage relative scale
    ls_x = (xmin / img_width) * 100
    ls_y = (ymin / img_height) * 100
    ls_w = (box_w / img_width) * 100
    ls_h = (box_h / img_height) * 100
    
    return ls_x, ls_y, ls_w, ls_h

# Initialize Configuration
IMAGE_FILE = "test_drone_frame.jpg"

if not os.path.exists(IMAGE_FILE):
    print(f"❌ Error: Please place an image named '{IMAGE_FILE}' in this folder first!")
    exit()

# Open image to extract actual width and height dimensions
with Image.open(IMAGE_FILE) as img:
    width, height = img.size

print(f"-> Ingesting frame dimensions: {width}x{height}px")

# Mocking a detection output payload from an object detection model
# Let's assume the model found a Vehicle and a Pedestrian at these exact pixel boundaries:
mock_ai_detections = [
    {
        "class": "Vehicle",
        "box": [100, 200, 450, 500]  # [xmin, ymin, xmax, ymax]
    },
    {
        "class": "Pedestrian",
        "box": [500, 150, 620, 480]
    }
]

# Convert image to inline text resource
base64_image_data = encode_image_to_base64(IMAGE_FILE)

# Build the structural Label Studio Result schema
results_array = []
for index, det in enumerate(mock_ai_detections):
    # Perform spatial transformation calculations
    x, y, w, h = calculate_ls_percentages(det["box"], width, height)
    
    results_array.append({
        "id": f"pred_{index}",
        "from_name": "label",
        "to_name": "image",
        "type": "rectanglelabels",
        "original_width": width,
        "original_height": height,
        "image_rotation": 0,
        "value": {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "rotation": 0,
            "rectanglelabels": [det["class"]]
        }
    })

# Format the final unified task document
ls_task = [{
    "data": {
        "image": base64_image_data
    },
    "predictions": [{
        "model_version": "drone-vision-v1",
        "result": results_array
    }]
}]

# Save the dataset to disk
output_filename = "label_studio_vision_import.json"
with open(output_filename, "w") as f:
    json.dump(ls_task, f, indent=4)

print(f"\n✅ Programmatic Vision Task generated successfully: '{output_filename}'")