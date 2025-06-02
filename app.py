# Ensure pandas is installed in your virtual environment: pip install pandas
from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import tempfile

app = Flask(__name__)

# Allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls', 'csv', 'txt'}

def rearrange_hex(hex_str, method):
    hex_str = str(hex_str)
    if method == 'reverse_bytes':
        # Split into pairs, reverse, join
        pairs = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
        return ''.join(pairs[::-1])
    elif method == 'last2_to_front':
        if len(hex_str) < 2:
            return hex_str
        return hex_str[-2:] + hex_str[:-2]
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

if __name__ == '__main__':
    app.run(debug=True) 