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
    def __init__(self, file_path='fuelPurchaseData.csv'):
        self.file_path = file_path
        self.data = []

    def load_csv(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.data = list(reader)

    def round_column_c(self):
        for i, row in enumerate(self.data):
            if i == 0:
                continue  # Skip header
            try:
                value = float(row[2])
                # Force 2 decimal places always, even for whole numbers
                row[2] = f"{value:.2f}"
            except (ValueError, IndexError):
                continue  # Skip if data isn't valid

    def save_csv(self, output_path='fuelPurchaseData.csv'):
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
