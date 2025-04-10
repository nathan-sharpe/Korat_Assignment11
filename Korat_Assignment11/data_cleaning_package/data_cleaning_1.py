# File Name : data_cleaning_1.py
# Student Name: Nathan Sharpe
# email: sharpenn@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:  4/17/25
# Course #/Section: IS 4010-001
# Semester/Year: Spring 2025
# Brief Description of the assignment: Clean up data from a CSV file and call and API to provide missing information.

# Brief Description of what this module does: Provides information on how to call APIs and work with the data returned
# Citations: https://app.zipcodebase.com/
# gemini.google.com

# Anything else that's relevant: Gemini was used to create the class

import pandas as pd
import requests
import json
import re

class AddressCleaner:
    def __init__(self, input_csv_file, output_csv_file, api_key):
        """
        Initializes the AddressCleaner with input and output file names and the API key.
        """
        self.input_file = input_csv_file
        self.output_file = output_csv_file
        self.api_key = api_key
        self.base_url = "https://app.zipcodebase.com/api/v1/radius"
        self.cleaned_count = 0

    def _get_zipcodes_near_blue_jay_ohio(self):
        """
        Calls the zipcodebase API to get zip codes within a 100-mile radius of Blue Jay, Ohio (assuming zip code 45247).

        Returns:
            list or None: A list of zip codes within the radius, or None if an error occurs.
        """
        params = {
            "apikey": self.api_key,
            "code": "45247",  # Assuming a central zip code for Blue Jay, OH
            "radius": "100",
            "country": "us"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data and 'results' in data:
                return [item['postal_code'] for item in data['results']]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error during API call for zip codes near Blue Jay: {e}")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON response for zip codes near Blue Jay.")
            return None

    def clean_addresses(self):
        """
        Reads the input CSV, identifies rows with potentially missing zip codes in "Full Address"
        for addresses likely in or near Blue Jay, Ohio, and populates them with a valid
        zip code from the surrounding area.
        Saves the cleaned data to a new CSV. Only the first 5 missing zip codes are populated.
        """
        try:
            df = pd.read_csv(self.input_file)
        except FileNotFoundError:
            print(f"Error: Input file '{self.input_file}' not found.")
            return

        if "Full Address" not in df.columns:
            print("Error: 'Full Address' column not found in the CSV file.")
            return

        nearby_zip_codes = self._get_zipcodes_near_blue_jay_ohio()
        if not nearby_zip_codes:
            print("Could not retrieve zip codes near Blue Jay, Ohio. Cleaning process aborted.")
            return

        for index, row in df.iterrows():
            if self.cleaned_count < 5:
                full_address = row["Full Address"]

                # Heuristic to identify addresses likely in or near Blue Jay, Ohio
                is_likely_nearby = False
                if isinstance(full_address, str):
                    if re.search(r',\s*OH\b', full_address, re.IGNORECASE):
                        is_likely_nearby = True
                    elif "Ohio" in full_address:
                        is_likely_nearby = True
                    elif "Blue Jay" in full_address:
                        is_likely_nearby = True
                    elif re.search(r'\b452\d{2}\b', full_address): # Check for Cincinnati area zip codes
                        is_likely_nearby = True

                    has_likely_zip = False
                    if re.search(r',\s*\d{5}(-\d{4})?\b', full_address):
                        has_likely_zip = True
                    elif re.fullmatch(r'\d{5}(-\d{4})?', full_address.strip()):
                        has_likely_zip = True

                    if is_likely_nearby and not has_likely_zip:
                        print(f"Processing potential nearby address (index {index}): {full_address}")
                        if nearby_zip_codes:
                            df.loc[index, "Full Address"] = f"{full_address.strip()}, {nearby_zip_codes[0]}"
                            self.cleaned_count += 1
                            print(f"  Populated with zip code: {nearby_zip_codes[0]}")
            else:
                break

        df.to_csv(self.output_file, index=False)
        print(f"\nCleaned data saved to '{self.output_file}'. Populated {self.cleaned_count} missing zip codes for likely nearby addresses (up to the first 5).")