import json

# Simulated numerical sensor logs from the drone's flight processor
# Format: [Timestamp, LiDAR_Distance_Meters, IMU_Acceleration_G]
raw_telemetry_streams = [
    # Stream 1: Simulated collision event
    [
        {"Time": "12:00:01", "LiDAR_Dist": "4.2m", "IMU_Acc": "1.01g"},
        {"Time": "12:00:02", "LiDAR_Dist": "2.1m", "IMU_Acc": "1.05g"},
        {"Time": "12:00:03", "LiDAR_Dist": "0.1m", "IMU_Acc": "4.89g"}, # <-- Massive G-force spike!
        {"Time": "12:00:04", "LiDAR_Dist": "0.0m", "IMU_Acc": "0.98g"}
    ],
    # Stream 2: Simulated sensor hardware failure
    [
        {"Time": "14:22:55", "LiDAR_Dist": "8.5m", "IMU_Acc": "1.00g"},
        {"Time": "14:22:56", "LiDAR_Dist": "0.0m", "IMU_Acc": "1.02g"}, # <-- Sudden total signal drop!
        {"Time": "14:22:57", "LiDAR_Dist": "8.6m", "IMU_Acc": "0.99g"}
    ]
]

def analyze_sensor_anomalies(log_rows):
    """Programmatic rules engine analyzing data frames for anomalies."""
    has_high_g = False
    has_sensor_drop = False
    
    for row in log_rows:
        acc_val = float(row["IMU_Acc"].replace("g", ""))
        dist_val = float(row["LiDAR_Dist"].replace("m", ""))
        
        if acc_val > 3.0:
            has_high_g = True
        if dist_val == 0.0:
            has_sensor_drop = True
            
    if has_high_g:
        return "CRITICAL: IMU Shock/Collision"
    elif has_sensor_drop:
        return "CRITICAL: LiDAR Blindness Drop"
    else:
        return "Normal Metrics"

# Build Unified Label Studio Tasks
import_dataset = []

for index, stream in enumerate(raw_telemetry_streams):
    # Determine the classification programmatically
    detected_anomaly = analyze_sensor_anomalies(stream)
    
    task = {
        "data": {
            # Convert the list of dictionaries into standard tabular format for the UI
            "log_data": stream
        },
        "predictions": [{
            "model_version": "telemetry-anomaly-v1",
            "result": [{
                "from_name": "status",
                "to_name": "telemetry",
                "type": "choices",
                "value": {
                    "choices": [detected_anomaly]
                }
            }]
        }]
    }
    import_dataset.append(task)

# Write to disk
output_file = "label_studio_sensor_import.json"
with open(output_file, "w") as f:
    json.dump(import_dataset, f, indent=4)

print(f"✅ Programmatic Telemetry Import file generated: '{output_file}'")