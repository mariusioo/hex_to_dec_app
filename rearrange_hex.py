import pandas as pd

# Read the cleaned hex values from the Excel file
df = pd.read_excel("cleaned_hex.xlsx")

# Get the column name (it's the first column)
column_name = df.columns[0]

# Convert the hex values to a list of strings
hex_strings = df[column_name].astype(str).tolist()

# Create lists to store original and rearranged hex values
original_hex = []
rearranged_hex = []

# Process each hex string
for hex_str in hex_strings:
    # Split the string into pairs of characters using a for loop
    pairs = []
    for i in range(0, len(hex_str), 2):
        pair = hex_str[i:i+2]
        pairs.append(pair)
    
    # Reverse the pairs
    reversed_pairs = pairs[::-1]
    
    # Join the pairs back together
    rearranged_hex_str = ''.join(reversed_pairs)
    
    # Store both original and rearranged values
    original_hex.append(hex_str)
    rearranged_hex.append(rearranged_hex_str)
    
    print("Original hex:", hex_str)
    print("Rearranged hex:", rearranged_hex_str)
    print("-" * 50)  # Add a separator line between each hex value

# Create a new DataFrame with both original and rearranged hex values
result_df = pd.DataFrame({
    'Original Hex': original_hex,
    'Rearranged Hex': rearranged_hex
})

# Save to a new Excel file
result_df.to_excel("rearranged_hex.xlsx", index=False)
print("\nResults have been saved to 'rearranged_hex.xlsx'")