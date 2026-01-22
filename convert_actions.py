import json
import re
import csv

# Read CSV data from file
csv_data = []
with open(r"c:\Users\ahmad\Desktop\Hiwonewco\Hiwonder Actions\actions_data.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    for row in reader:
        # Convert all values to integers: [Index, Time, ID1-ID16]
        csv_data.append([int(val) for val in row])

def convert_to_4096(value): 
    """Convert from 0-1000 range to 0-4096 range"""
    return round(value * 4.096)

def generate_action_id():
    """Generate a random 4-character hex ID"""
    import random
    return ''.join(random.choices('0123456789abcdef', k=4))

def create_action(index, time_ms, servo_values):
    """Create an action object"""
    data = {}
    
    # Add servo values (ID 1-16)
    for i, value in enumerate(servo_values, 1):
        converted_value = convert_to_4096(value)
        data[str(i)] = {
            "isEnabled": True,
            "value": converted_value
        }
    
    # Add Time
    data["T"] = {
        "isEnabled": True,
        "value": time_ms
    }
    
    # Add Head
    data["H"] = {
        "isEnabled": True,
        "value": 90,
        "speed": 10
    }
    
    return {
        "id": generate_action_id(),
        "data": data,
        "markerPositionTime": "",  # Will be calculated
        "actionName": f"Action {index}"
    }

# Generate all actions
all_actions = []
cumulative_time = 0

for row in csv_data:
    index = row[0]
    time_ms = row[1]
    servo_values = row[2:18]  # 16 servo values
    
    cumulative_time += time_ms
    
    action = create_action(index, time_ms, servo_values)
    action["markerPositionTime"] = f"{cumulative_time / 1000:.3f}"
    
    all_actions.append(action)

# Read the original file
with open(r"c:\Users\ahmad\Desktop\Hiwonewco\Hiwonder Actions\nameofact.txt", 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the JSON
data = json.loads(content)

# Update createActionState
create_action_state = json.loads(data["createActionState"])
create_action_state["allActions"] = all_actions

# Update the data
data["createActionState"] = json.dumps(create_action_state)

# Write to .pld file
with open(r"c:\Users\ahmad\Desktop\Hiwonewco\Hiwonder Actions\nameofact.pld", 'w', encoding='utf-8') as f:
    json.dump(data, f)

print("Conversion complete!")
print(f"Total actions: {len(all_actions)}")
print("\nConverted servo values for Action 1:")
for i in range(1, 17):
    original = csv_data[0][i+1]
    converted = convert_to_4096(original)
    print(f"  S{i}: {original} -> {converted}")
