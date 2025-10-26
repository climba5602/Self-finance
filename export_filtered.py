import pandas as pd

# Load the Excel file
excel_path = '5_-List-of-RCHEs-Providing-Non-subsidised-Places-for-the-Elderly_Q-30_6_2025.xlsx'
sheet_names = pd.ExcelFile(excel_path).sheet_names

combined_data = []

for sheet in sheet_names:
    df = pd.read_excel(excel_path, sheet_name=sheet, header=2)
    df = df.iloc[1:].dropna(how='all')  # Skip first row, drop empty rows

    # Rename columns for easier access
    columns_map = {
        df.columns[0]: 'S/N',
        df.columns[1]: 'District',
        df.columns[2]: 'Agency',
        df.columns[3]: 'Name',
        df.columns[4]: 'Address',
        df.columns[5]: 'Tel',
        df.columns[6]: 'Fax',
        df.columns[7]: 'Hostel',
        df.columns[8]: 'Home_for_Aged',
        df.columns[9]: 'Care_and_Attention',
        df.columns[10]: 'Nursing_Home',
        df.columns[11]: 'Total',
        df.columns[12]: 'Sex',
        df.columns[13]: 'Religion'
    }
    df = df.rename(columns=columns_map)

    combined_data.append(df)

# Combine all sheets
all_data = pd.concat(combined_data, ignore_index=True)

# Clean District and convert number columns
all_data['District'] = all_data['District'].str.strip()
all_data['Care_and_Attention'] = pd.to_numeric(all_data['Care_and_Attention'], errors='coerce').fillna(0)
all_data['Nursing_Home'] = pd.to_numeric(all_data['Nursing_Home'], errors='coerce').fillna(0)

# Filter to include only Care-and-Attention or Nursing Home places
filtered_df = all_data[(all_data['Care_and_Attention'] > 0) | (all_data['Nursing_Home'] > 0)]

# Export to CSV
filtered_df.to_csv('elderly_homes_combined_filtered.csv', index=False, encoding='utf-8-sig')

print("Exported filtered data to 'elderly_homes_combined_filtered.csv'")
