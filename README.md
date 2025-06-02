# Hex to Decimal Converter

A web application that converts hexadecimal numbers to decimal, with options for hex rearrangement and duplicate scanning.

## Features

- Convert hex numbers to decimal
- Rearrange hex numbers in pairs of two
- Support for multiple file formats (xlsx, xls, csv, txt)
- Scan for duplicates between two files
- Download results in CSV or TXT format

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

### Converting Hex to Decimal

1. Click "Convert Hex to Decimal"
2. Upload your file (supported formats: xlsx, xls, csv, txt)
3. Choose a hex rearrangement method:
   - Reverse all bytes (pairs of two)
   - No Inversion
4. Select output columns (Original Hex, Rearranged Hex, Decimal)
5. Choose output format (CSV or TXT)
6. Click "Convert & Download"

### Scanning for Duplicates

1. Click "Scan for Duplicates"
2. Upload two files to compare
3. View the results showing which values are duplicates
4. Download the comparison file if needed

## File Format Requirements

- Input files should have hex/decimal values in the first column
- Supported file formats: xlsx, xls, csv, txt
- For CSV files, values should be comma-separated
- For TXT files, values should be tab-separated 