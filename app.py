# Ensure pandas is installed in your virtual environment: pip install pandas
from flask import Flask, render_template, request, send_file, url_for, session
import pandas as pd
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls', 'csv', 'txt'}

def rearrange_hex(hex_str, method):
    hex_str = str(hex_str)
    if method == 'reverse_all':
        # Simply reverse all bytes
        pairs = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
        return ''.join(pairs[::-1])
    elif method == 'no_invert':
        return hex_str
    return hex_str

def hex_to_dec(hex_str):
    try:
        return int(hex_str, 16)
    except Exception:
        return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        method = request.form.get('method')
        output_cols = request.form.getlist('output_cols')
        output_format = request.form.get('output_format')
        if not file or not allowed_file(file.filename):
            return 'Invalid file type', 400
        # Read file into DataFrame
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        elif ext == 'csv':
            df = pd.read_csv(file)
        elif ext == 'txt':
            df = pd.read_csv(file, delimiter=None, engine='python', header=None)
        else:
            return 'Unsupported file type', 400
        # Assume first column is hex
        col = df.columns[0]
        df['Rearranged Hex'] = df[col].astype(str).apply(lambda x: rearrange_hex(x, method))
        df['Decimal'] = df['Rearranged Hex'].apply(hex_to_dec)
        # Prepare output
        output_df = pd.DataFrame()
        if 'original' in output_cols:
            output_df['Original Hex'] = df[col]
        if 'rearranged' in output_cols:
            output_df['Rearranged Hex'] = df['Rearranged Hex']
        if 'decimal' in output_cols:
            output_df['Decimal'] = df['Decimal']
        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.'+output_format)
        if output_format == 'csv':
            output_df.to_csv(tmp.name, index=False)
        else:
            output_df.to_csv(tmp.name, index=False, sep='\t')
        tmp.close()
        return send_file(tmp.name, as_attachment=True, download_name=f'converted.{output_format}')
    return render_template('index.html')

@app.route('/scan_duplicates', methods=['GET', 'POST'])
def scan_duplicates():
    if request.method == 'POST':
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        if not file1 or not file2 or not allowed_file(file1.filename) or not allowed_file(file2.filename):
            return 'Invalid file type', 400
        # Read files into DataFrames
        ext1 = file1.filename.rsplit('.', 1)[1].lower()
        ext2 = file2.filename.rsplit('.', 1)[1].lower()
        if ext1 in ['xlsx', 'xls']:
            df1 = pd.read_excel(file1)
        elif ext1 == 'csv':
            df1 = pd.read_csv(file1)
        elif ext1 == 'txt':
            df1 = pd.read_csv(file1, delimiter=None, engine='python', header=None)
        else:
            return 'Unsupported file type for file 1', 400
        if ext2 in ['xlsx', 'xls']:
            df2 = pd.read_excel(file2)
        elif ext2 == 'csv':
            df2 = pd.read_csv(file2)
        elif ext2 == 'txt':
            df2 = pd.read_csv(file2, delimiter=None, engine='python', header=None)
        else:
            return 'Unsupported file type for file 2', 400
        # Assume first column is hex/decimal
        col1 = df1.columns[0]
        col2 = df2.columns[0]
        # Find duplicates
        duplicates = df1[col1].isin(df2[col2]).tolist()
        # Create a DataFrame for the comparison
        comparison_df = pd.DataFrame({
            'Value': df1[col1],
            'Is Duplicate': duplicates
        })
        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        comparison_df.to_csv(tmp.name, index=False)
        tmp.close()
        session['comparison_file'] = tmp.name
        return render_template('duplicates.html', duplicates=duplicates, download_url=url_for('download_comparison'))
    return render_template('scan_duplicates.html')

@app.route('/download_comparison')
def download_comparison():
    if 'comparison_file' not in session:
        return 'No comparison file available', 404
    return send_file(session['comparison_file'], as_attachment=True, download_name='comparison.csv')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        file = request.files.get('file')
        method = request.form.get('method')
        output_cols = request.form.getlist('output_cols')
        output_format = request.form.get('output_format')
        if not file or not allowed_file(file.filename):
            return 'Invalid file type', 400
        # Read file into DataFrame
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        elif ext == 'csv':
            df = pd.read_csv(file)
        elif ext == 'txt':
            df = pd.read_csv(file, delimiter=None, engine='python', header=None)
        else:
            return 'Unsupported file type', 400
        # Assume first column is hex
        col = df.columns[0]
        df['Rearranged Hex'] = df[col].astype(str).apply(lambda x: rearrange_hex(x, method))
        df['Decimal'] = df['Rearranged Hex'].apply(hex_to_dec)
        # Prepare output
        output_df = pd.DataFrame()
        if 'original' in output_cols:
            output_df['Original Hex'] = df[col]
        if 'rearranged' in output_cols:
            output_df['Rearranged Hex'] = df['Rearranged Hex']
        if 'decimal' in output_cols:
            output_df['Decimal'] = df['Decimal']
        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.'+output_format)
        if output_format == 'csv':
            output_df.to_csv(tmp.name, index=False)
        else:
            output_df.to_csv(tmp.name, index=False, sep='\t')
        tmp.close()
        return send_file(tmp.name, as_attachment=True, download_name=f'converted.{output_format}')
    return render_template('convert.html')

if __name__ == '__main__':
    app.run(debug=True) 