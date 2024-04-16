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


def get_medical_condition(blood_group):

    medical_conditions = {
        'A+': 'Blood Group Type A+ individuals may have a higher risk of developing Arthritis, Asthma, Cancer, and Hypertension.',
        'A-': 'Blood Group Type A- individuals may be at increased risk of Cancer and Diabetes.',
        'B+': 'Blood Group Type B+ individuals might have an increased risk of Diabetes and Hypertension.',
        'B-': 'Blood Group Type B- individuals may have a higher risk of Diabetes, Hypertension, and Obesity.',
        'AB+': 'Blood Group Type AB+ individuals might have a higher risk of Arthritis, Diabetes, and Obesity.',
        'AB-': 'Blood Group Type AB- individuals may be at higher risk for Diabetes, Hypertension, and Obesity.',
        'O+': 'Blood Group Type O+ individuals may be at increased risk for Arthritis, Asthma, and Cancer.',
        'O-': 'Blood Group Type O- individuals might have a higher risk of Arthritis and Obesity.'
    }
    return medical_conditions.get(blood_group, 'Unknown')


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

        medical_condition = get_medical_condition(blood_group)

        return render_template('contact.html', name=name, gender=gender, blood_group=blood_group, medical_condition=medical_condition)


app.run(port=5001)
