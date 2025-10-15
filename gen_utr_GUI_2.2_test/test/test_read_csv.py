import unittest
import os
import json
import tempfile
from io import StringIO
from read_csv_and_create_json import read_csv_and_create_json
import csv

class TestReadCSVAndCreateJSON(unittest.TestCase):
    def setUp(self):
        # Mock CSV content with the expected column names
        self.mock_csv_data = """gene_symbol,transcript_id,disease_name
        VWF,NM_000552,von Willebrands sjukdom
        F8,NM_000132,Hemofili A
        SERPINC1,NM_000488,Antitrombinbrist
        """
        
        # Expected JSON output
        self.expected_json = {
            "VWF": {"Transcript": "NM_000552", "Disease": "von Willebrands sjukdom"},
            "F8": {"Transcript": "NM_000132", "Disease": "Hemofili A"},
            "SERPINC1": {"Transcript": "NM_000488", "Disease": "Antitrombinbrist"}
        }

    def test_read_csv_and_create_json(self):
        # Create a temporary file to act as the CSV file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_csv:
            temp_csv.write(self.mock_csv_data)
            temp_csv.seek(0)  # Go back to the beginning of the file

            # Print the header to check
            reader = csv.DictReader(temp_csv)
            headers = reader.fieldnames
            print(f"CSV Headers: {headers}")  # Print the headers for debugging

            # Create a temporary file to act as the JSON file
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_json:
                temp_json_path = temp_json.name
                
                # Call the function to read CSV and create JSON
                read_csv_and_create_json(temp_csv.name, temp_json.name)
                
                # Read the JSON file content
                with open(temp_json.name, 'r') as json_file:
                    output_data = json.load(json_file)
                
                # Compare the output to the expected JSON
                self.assertEqual(output_data, self.expected_json)

        # Clean up the temporary files
        os.remove(temp_csv.name)
        os.remove(temp_json_path)

if __name__ == '__main__':
    unittest.main()
