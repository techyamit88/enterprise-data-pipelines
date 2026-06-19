import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b" # Or whatever text model you have pulled in Ollama

# 1. Raw incoming text data from the delivery logs
raw_data = [
    {"text": "Drop the food packet on the front porch next to the red Honda Civic. Watch out for the stray cat near the stairs."},
    {"text": "Deliver to building B back door entrance. Do not enter through the front gate, the security guard says it is locked."}
]

def query_ollama_for_ner(text):
    prompt = f"""
    Analyze this text and extract entities. You must look for locations, vehicles, and obstacles/dangers.
    
    Text: "{text}"
    
    Return a valid JSON object matching this exact structure:
    {{
      "urgency": "High Alert / Dangerous" or "Routine Delivery",
      "entities": [
        {{"text": "exact substring matched", "label": "LOCATION" or "VEHICLE" or "OBSTACLE_DANGER"}}
      ]
    }}
    Return raw JSON only. Do not wrap in markdown or backticks.
    """
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"Ollama parsing failed: {e}")
        return None

def build_label_studio_task(text, ai_prediction):
    # This maps the text character locations exactly how Label Studio demands it for NER
    predictions = []
    
    # Add the classification choice
    predictions.append({
        "from_name": "urgency",
        "to_name": "text",
        "type": "choices",
        "value": {"choices": [ai_prediction["urgency"]]}
    })
    
    # Add the text span locations
    for ent in ai_prediction.get("entities", []):
        start_idx = text.find(ent["text"])
        if start_idx != -1:
            end_idx = start_idx + len(ent["text"])
            predictions.append({
                "from_name": "label",
                "to_name": "text",
                "type": "labels",
                "value": {
                    "start": start_idx,
                    "end": end_idx,
                    "text": ent["text"],
                    "labels": [ent["label"]]
                }
            })
            
    return {
        "data": {"text": text},
        "predictions": [{
            "model_version": "ollama-" + MODEL_NAME,
            "result": predictions
        }]
    }

# Execute Pipeline
import_dataset = []
for item in raw_data:
    print(f"-> Extracting spans for text: '{item['text'][:30]}...'")
    ai_output = query_ollama_for_ner(item["text"])
    
    if ai_output:
        task_json = build_label_studio_task(item["text"], ai_output)
        import_dataset.append(task_json)

# Save to file
with open("label_studio_import.json", "w") as f:
    json.dump(import_dataset, f, indent=2)
print("\n✅ Label Studio pre-label import file created successfully as 'label_studio_import.json'!")