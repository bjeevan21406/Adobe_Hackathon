# In main.py
import os
import json
from utils.extractor_1a import extract_structure

def main():
    """
    Main function to process all PDFs in the input directory
    and save the output in the output directory.
    """
    input_dir = '/app/input'
    output_dir = '/app/output'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processing {pdf_path}...")

            try:
                # Extract the structured outline
                result_data = extract_structure(pdf_path)

                # Define output path
                output_filename = os.path.splitext(filename)[0] + '.json'
                output_path = os.path.join(output_dir, output_filename)

                # Write the JSON output
                with open(output_path, 'w') as f:
                    json.dump(result_data, f, indent=4)
                
                print(f"Successfully created {output_path}")

            except Exception as e:
                print(f"Failed to process {pdf_path}: {e}")

if _name_ == "_main_":
    main()