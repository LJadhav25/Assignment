from flask import Flask, render_template, request
import csv
import json
import os

app = Flask(__name__)


@app.route('/home')
def home_page():
    return render_template('home.html')


file_directory = 'files'


def write_csv(data):
    csv_file_path = os.path.join(file_directory, 'form_data.csv')
    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Gender', 'Blood Group']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


def write_json(data):
    json_file_path = os.path.join(file_directory, 'form_data.json')
    with open(json_file_path, 'a') as jsonfile:
        json.dump(data, jsonfile, indent=4)
        jsonfile.write('\n')


def get_medical_condition(gender, blood_group):
    medical_conditions = {
        ('Female', 'A+'): 'Arthritis',
        ('Female', 'A-'): 'Arthritis',
        ('Female', 'AB+'): 'Arthritis',
        ('Female', 'AB-'): 'Hypertension',
        ('Female', 'B+'): 'Diabetes',
        ('Female', 'B-'): 'Diabetes',
        ('Female', 'O+'): 'Arthritis',
        ('Female', 'O-'): 'Arthritis',
        ('Male', 'A+'): 'Asthma',
        ('Male', 'A-'): 'Diabetes',
        ('Male', 'AB+'): 'Cancer',
        ('Male', 'AB-'): 'Cancer',
        ('Male', 'B+'): 'Diabetes',
        ('Male', 'B-'): 'Diabetes',
        ('Male', 'O+'): 'Diabetes',
        ('Male', 'O-'): 'Arthritis'
    }
    key = (gender, blood_group)
    highest_risk_condition = medical_conditions.get(key, 'Unknown')
    return highest_risk_condition


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        blood_group = request.form['blood_group']

        form_data = {
            'Name': name,
            'Gender': gender,
            'Blood Group': blood_group
        }
        
        write_csv(form_data)

        write_json(form_data)

        medical_condition = get_medical_condition(gender, blood_group)

        return render_template('contact.html', name=name, gender=gender, blood_group=blood_group, medical_condition=medical_condition)


app.run(port=5001)
