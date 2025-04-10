# Zach class

# File Name : data_cleaning_2.py
# Student Name: Zach Bell
# email:  bellzj@mail.uc.edu
# Assignment Number: Assignment 11  {required}
# Due Date:  4/17/25 {required}
# Course #/Section: IS4010-001  {required}
# Semester/Year: Spring 2025  {required}
# Brief Description of the assignment:  Cleaining up the data in the csv file. {required}

# Brief Description of what this module does. Builds on pulling data from API and integrating into a project.
# Citations: chatgpt

# Anything else that's relevant:

import csv

class GrossPriceEditor:
    """
    A class to process and clean a CSV file containing fuel purchase data.
    Includes methods to round values, remove duplicates, and filter out specific rows.
    """

    def __init__(self, file_path='fuelPurchaseData.csv'):
        """
        Constructor to initialize the CSV editor.

        @param file_path: Path to the input CSV file. Defaults to 'fuelPurchaseData.csv'.
        """
        self.file_path = file_path
        self.data = []

    def load_csv(self):
        """
        Loads the contents of the CSV file into memory.
        """
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.data = list(reader)

    def round_column_c(self):
        """
        Rounds the values in column C (index 2) to exactly 2 decimal places.
        Skips the header and handles invalid or missing values.
        """

        for i, row in enumerate(self.data):
            if i == 0:
                continue  # Skip header
            try:
                value = float(row[2])
                # Force 2 decimal places always, even for whole numbers
                row[2] = f"{value:.2f}"
            except (ValueError, IndexError):
                continue  # Skip if data isn't valid

    def remove_duplicates(self):
        """
        Removes duplicate rows from the data.
        Only the first occurrence of each unique row is kept.
        """
        seen = set()
        new_data = []
        for row in self.data:
            row_tuple = tuple(row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                new_data.append(row)
        self.data = new_data
    
    def remove_pepsi_rows(self):
        """
        Removes rows where column F (index 5) contains the word 'Pepsi' (case-insensitive).
        Header row is always preserved.
        """
        header = self.data[0]
        filtered_data = [header]
        for row in self.data[1:]:
            try:
                if row[5].strip().lower() != "pepsi":
                    filtered_data.append(row)
            except IndexError:
                # If column F is missing, keep the row
                filtered_data.append(row)
        self.data = filtered_data

    def save_csv(self, output_path='fuelPurchaseData.csv'):
        """
        Saves the processed data to a new CSV file.

        @param output_path: Destination file path to save the CSV. Defaults to the original filename.
        """
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
