import pandas as pd
import sys
import os

def convert_jsonl_to_csv(input_file, output_file):
    """
    Converts a JSONL file to a CSV file using pandas.
    """
    try:
        print(f"Reading {input_file}...")
        # Read JSONL file
        df = pd.read_json(input_file, lines=True)
        
        print(f"Converting to CSV...")
        # Save to CSV
        df.to_csv(output_file, index=False, encoding='utf-16')
        
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    except ValueError as e:
        print(f"Error: Invalid JSONL format in '{input_file}'. {e}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python converter.py <input_jsonl_file> <output_csv_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    convert_jsonl_to_csv(input_path, output_path)
