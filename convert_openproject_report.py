#!/usr/bin/env python3
"""
Convert OpenProject XLS cost reports to Google Sheets format.

Input: OpenProject XLS export with columns:
  - Date (Spent)
  - User
  - Activity
  - Logged for (Task description)
  - Comment
  - Project
  - Units (hours)
  - Cost type
  - Costs

Output: CSV with columns:
  A: Projekt
  B: Datum
  C: Stunden (Summe)
  D: Task-IDs
  E: Manuelle Korrektur (original hours, editable)
"""

import pandas as pd
import re
from datetime import datetime
from collections import defaultdict
import sys

def extract_task_ids(task_description):
    """
    Extract task IDs from task description.
    
    Examples:
      "Task #6748: [VP5-2745] Analyse..." -> "VP5-2745"
      "Task #6907: VP5-2762 [YAML]..." -> "VP5-2762"
    """
    if pd.isna(task_description) or task_description == '-':
        return ''
    
    # Pattern to match VP5-XXXX format
    matches = re.findall(r'VP5-\d+', str(task_description))
    
    if matches:
        # Remove duplicates and join
        return ', '.join(sorted(set(matches)))
    
    return ''

def convert_report(input_file, output_file='converted_report.csv'):
    """Convert OpenProject XLS to target format."""
    
    print(f"📖 Lese Datei: {input_file}")
    
    # Read XLS file
    df = pd.read_excel(input_file, engine='xlrd')
    
    # Skip header row (first row contains column names)
    df = df[1:]  # Skip the header row
    
    # Rename columns for easier access
    df.columns = [
        'Date',
        'User',
        'Activity',
        'Logged_for',
        'Comment',
        'Project',
        'Units',
        'Cost_type',
        'Costs'
    ]
    
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convert Units to float
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
    
    # Extract task IDs
    df['Task_IDs'] = df['Logged_for'].apply(extract_task_ids)
    
    print(f"✅ {len(df)} Einträge geladen")
    
    # Group by Project and Date
    grouped = df.groupby(['Project', 'Date']).agg({
        'Units': 'sum',
        'Task_IDs': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))) if any(x) else ''
    }).reset_index()
    
    # Clean up task IDs (remove empty strings)
    grouped['Task_IDs'] = grouped['Task_IDs'].apply(
        lambda x: ', '.join([t.strip() for t in x.split(',') if t.strip()])
    )
    
    # Format date as YYYY-MM-DD
    grouped['Date'] = grouped['Date'].dt.strftime('%Y-%m-%d')
    
    # Add manual correction column with original hours
    grouped['Manuelle_Korrektur'] = grouped['Units']
    
    # Rename columns to match target format
    result = grouped.rename(columns={
        'Project': 'Projekt',
        'Date': 'Datum',
        'Units': 'Stunden (Summe)',
        'Task_IDs': 'Task-IDs',
        'Manuelle_Korrektur': 'Manuelle Korrektur'
    })
    
    # Reorder columns
    result = result[['Projekt', 'Datum', 'Stunden (Summe)', 'Task-IDs', 'Manuelle Korrektur']]
    
    # Sort by date
    result = result.sort_values('Datum')
    
    print(f"📊 {len(result)} Tage gruppiert")
    print(f"\nVorschau:")
    print(result.head(10).to_string(index=False))
    
    # Save to CSV
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Konvertierung abgeschlossen!")
    print(f"📁 Ausgabe: {output_file}")
    print(f"\n💡 Nächste Schritte:")
    print(f"   1. Öffne {output_file}")
    print(f"   2. Importiere in Google Sheets")
    print(f"   3. Bearbeite Spalte E (Manuelle Korrektur)")
    
    return result

if __name__ == "__main__":
    # Check if input file is provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Use default file in current directory
        input_file = "cost-report-2026-02-02-T-11-34-4120260202-7-p8jkg3.xls"
    
    # Check if output file is provided
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "converted_report.csv"
    
    try:
        convert_report(input_file, output_file)
    except FileNotFoundError:
        print(f"❌ Fehler: Datei '{input_file}' nicht gefunden!")
        print(f"\nVerwendung: python3 {sys.argv[0]} <input.xls> [output.csv]")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
