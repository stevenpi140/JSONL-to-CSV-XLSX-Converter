from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.jsonl'):
        try:
            # Create a temporary file to save the uploaded JSONL
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl') as temp_jsonl:
                file.save(temp_jsonl.name)
                temp_jsonl_path = temp_jsonl.name

            # Get output format
            output_format = request.form.get('format', 'csv')
            
            if output_format == 'xlsx':
                # Create a temporary file for the XLSX output
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xlsx:
                    temp_xlsx_path = temp_xlsx.name
                
                # Perform conversion
                df = pd.read_json(temp_jsonl_path, lines=True)
                df.to_excel(temp_xlsx_path, index=False)
                
                output_path = temp_xlsx_path
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                download_name = f"{os.path.splitext(file.filename)[0]}.xlsx"
            else:
                # Create a temporary file for the CSV output
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv:
                    temp_csv_path = temp_csv.name

                # Perform conversion
                df = pd.read_json(temp_jsonl_path, lines=True)
                df.to_csv(temp_csv_path, index=False, encoding='utf-16')
                
                output_path = temp_csv_path
                mimetype = 'text/csv'
                download_name = f"{os.path.splitext(file.filename)[0]}.csv"

            # Clean up JSONL file
            os.remove(temp_jsonl_path)

            # Send the file
            return send_file(
                output_path,
                as_attachment=True,
                download_name=download_name,
                mimetype=mimetype
            )

        except ValueError as e:
            flash(f'Error: Invalid JSONL format. {e}')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An unexpected error occurred: {e}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a .jsonl file.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
