import pandas as pd

def process_attendance(file, total_holidays, total_saturdays):
    # Load Excel and skip metadata rows
    data = pd.read_excel(file, skiprows=7)

    # Set the first valid row as header
    data.columns = data.iloc[0]
    data = data[1:]

    # Remove columns with all NaN and rows with any NaN
    data.dropna(axis=1, how='all', inplace=True)
    data.dropna(axis=0, how='any', inplace=True)

    # Rename "Emp Name" column for clarity
    data.rename(columns={"Emp Name": "Name"}, inplace=True)

    # Reset index
    data.reset_index(drop=True, inplace=True)

    # Calculate attendance summary
    summary = []
    for _, row in data.iterrows():
        name = row["Name"]
        
        # Total Present: Count of 'P' or 'MIS' (Present or Marked Present)
        total_present = sum(row[1:].isin(['P', 'MIS']))

        # Total Absent: Count of 'A' (Absent)
        total_absent = sum(row[1:] == 'A')

        # Calculate Total Official Holidays: Sundays (WO-I) and 2nd/4th Saturdays
        total_official_holidays = sum(row[1:] == 'WO-I') + total_saturdays
        
        # Adjust Total Absent (excluding holidays)
        adjusted_absent = total_absent - total_saturdays

        # Net Final Absent: Total Absent - Total Other Holidays
        net_final_absent = adjusted_absent - total_holidays

        # Add summary row
        summary.append({
            "Name": name,
            "Total Present": total_present,
            "Total Absent (Excluding Other Holidays)": adjusted_absent,
            "Total Other Holidays": total_holidays,
            "Net Final Absent": net_final_absent
        })

    # Convert summary to DataFrame
    summary_df = pd.DataFrame(summary)
    return summary_df
