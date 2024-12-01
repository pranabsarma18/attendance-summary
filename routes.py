from flask import Blueprint, render_template, request, send_file
from utils import process_attendance
import pandas as pd
from io import BytesIO

main = Blueprint('main', __name__)

@main.route('/')
def upload_page():
    return render_template('upload.html')

@main.route('/process', methods=['POST'])
def process_file():
    file = request.files.get('file')
    if file:
        # Get user-provided holiday data
        total_holidays = int(request.form.get('total_holidays', 0))  # Other holidays
        total_saturdays = int(request.form.get('total_saturdays', 0))  # 2nd & 4th Saturdays

        # Process the uploaded file
        summary_df = process_attendance(file, total_holidays, total_saturdays)

        # Save the summary as an Excel file for download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            summary_df.to_excel(writer, index=False, sheet_name='Summary')
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="Attendance_Summary.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        return "No file uploaded. Please go back and upload a file."

