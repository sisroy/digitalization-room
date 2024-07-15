import csv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from collections import defaultdict

app = Flask(__name__)

# Function to parse CSV file and return data as list of dictionaries
def parse_csv(file):
    reader = csv.DictReader(file)
    data = []
    for row in reader:
        data.append(row)
    return data

# Load hostel rooms from CSV file
hostel_rooms = defaultdict(list)
with open('hostel_rooms.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        hostel_name = row['Hostel Name']
        room_number = int(row['Room Number'])
        capacity = int(row['Capacity'])
        gender = row['Gender'].strip()  # strip to remove any leading/trailing whitespace
        hostel_rooms[hostel_name].append({'room_number': room_number, 'capacity': capacity, 'gender': gender})

# Function to allocate rooms to groups
def allocate_rooms(groups, hostel_rooms):
    allocation = []
    for group_id, group_data in groups.items():
        group_id = int(group_id)
        member_count = int(group_data['Members'])
        gender = group_data['Gender'].strip()  # strip to remove any leading/trailing whitespace
        allocated = False

        # Find matching rooms in respective hostel
        if gender in ['Boys', 'Girls']:
            for room in hostel_rooms[f'{gender} Hostel']:
                if room['gender'] == gender and room['capacity'] >= member_count:
                    allocation.append({
                        'Group ID': group_id,
                        'Hostel Name': f'{gender} Hostel',
                        'Room Number': room['room_number'],
                        'Members Allocated': member_count
                    })
                    room['capacity'] -= member_count
                    allocated = True
                    break
        
        if not allocated:
            allocation.append({
                'Group ID': group_id,
                'Hostel Name': 'Unallocated',  # If no suitable room found
                'Room Number': '-',
                'Members Allocated': member_count
            })

    return allocation

@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle file upload and room allocation
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'group_csv' not in request.files or 'hostel_csv' not in request.files:
        return 'Files not found', 400
    
    group_csv = request.files['group_csv']
    hostel_csv = request.files['hostel_csv']

    if group_csv.filename == '' or hostel_csv.filename == '':
        return 'No selected files', 400
    
    groups_data = parse_csv(group_csv)
    hostel_data = parse_csv(hostel_csv)

    # Convert groups_data to a dictionary with Group ID as key
    groups = {group['Group ID']: group for group in groups_data}

    # Allocate rooms
    allocation = allocate_rooms(groups, hostel_rooms)

    # Prepare HTML output
    return render_template('allocation.html', allocation=allocation)

if __name__ == '__main__':
    app.run(debug=True)
