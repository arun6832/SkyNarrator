from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

# Initialize Flask app
app = Flask(__name__)

# Function to generate the advisory summary based on input data
def generate_advisory(input_data):
    advisory = []
    for day, data in input_data.items():
        # Based on data, generate the advisory for irrigation, crop management, etc.
        advisory.append(f"On {day}, with {data['Rainfall']} rainfall, the irrigation is recommended.")
        advisory.append(f"Wind speed of {data['Wind Speed']} could impact crops, so take necessary precautions.")
        advisory.append(f"The temperature of {data['Temperature']} and humidity of {data['Humidity']} suggest checking for crop diseases.")
        advisory.append(f"Relative humidity between {data['Relative Humidity Min']} and {data['Relative Humidity Max']} indicates moderate conditions for growth.")
        advisory.append("")  # Add a line break between days

    return "\n".join(advisory)

# Function to generate the PDF
def generate_pdf(input_data, advisory):
    # Create a PDF file
    file_name = "weather_advisory_report.pdf"
    pdf_path = os.path.join('static', file_name)
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

    # Prepare data for the table
    weather_data = []
    header = ["Day", "Rainfall", "Wind Speed", "Temperature", "Humidity", "Relative Humidity Max", "Relative Humidity Min"]
    weather_data.append(header)

    # Loop through the input data to add each day's weather data to the table
    for day, weather in input_data.items():
        row = [
            day,
            weather["Rainfall"],
            weather["Wind Speed"],
            weather["Temperature"],
            weather["Humidity"],
            weather["Relative Humidity Max"],
            weather["Relative Humidity Min"]
        ]
        weather_data.append(row)

    # Create a Table for weather data
    table = Table(weather_data)

    # Style the table (color, borders, etc.)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SIZE', (0, 0), (-1, 0), 10),
        ('SIZE', (0, 1), (-1, -1), 8),
    ]))

    # Create a paragraph for the advisory summary
    styles = getSampleStyleSheet()
    advisory_paragraph = Paragraph(advisory, styles['Normal'])

    # Build the PDF content
    elements = [table, advisory_paragraph]

    # Build and save the PDF
    pdf.build(elements)
    return pdf_path

# Define route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define route to handle dynamic input population and advisory generation
@app.route('/generate_input', methods=['POST'])
def generate_input():
    # This is where you would run the backend model and generate data
    generated_input = {
        "Day 1": {
            "Rainfall": "10 mm",
            "Wind Speed": "15 km/h",
            "Temperature": "25°C",
            "Humidity": "80%",
            "Relative Humidity Max": "90%",
            "Relative Humidity Min": "70%"
        },
        "Day 2": {
            "Rainfall": "5 mm",
            "Wind Speed": "10 km/h",
            "Temperature": "28°C",
            "Humidity": "75%",
            "Relative Humidity Max": "85%",
            "Relative Humidity Min": "65%"
        },
        "Day 3": {
            "Rainfall": "0 mm",
            "Wind Speed": "8 km/h",
            "Temperature": "30°C",
            "Humidity": "70%",
            "Relative Humidity Max": "80%",
            "Relative Humidity Min": "60%"
        },
        "Day 4": {
            "Rainfall": "20 mm",
            "Wind Speed": "20 km/h",
            "Temperature": "22°C",
            "Humidity": "85%",
            "Relative Humidity Max": "95%",
            "Relative Humidity Min": "75%"
        },
        "Day 5": {
            "Rainfall": "15 mm",
            "Wind Speed": "12 km/h",
            "Temperature": "24°C",
            "Humidity": "78%",
            "Relative Humidity Max": "88%",
            "Relative Humidity Min": "68%"
        }
    }
    # Returning the generated data as JSON to populate the form
    return jsonify(generated_input)

# Define route to handle PDF generation
@app.route('/generate_pdf', methods=['POST'])
def generate():
    if request.method == 'POST':
        # Get user input from the form
        input_data = request.form['input_data']
        input_dict = eval(input_data)  # Convert string to dictionary for easy manipulation

        # Generate the advisory summary
        advisory = generate_advisory(input_dict)

        # Generate the PDF
        pdf_path = generate_pdf(input_dict, advisory)

        # Send the generated PDF for download
        return send_file(pdf_path, as_attachment=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
