# File Name : main.py
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

from data_cleaning_package.data_cleaning_2 import *
from data_cleaning_package.data_cleaning_1 import *

if __name__ == "__main__":
    # Instantiate an object of the GrossPriceEditor class
    priceConverter = GrossPriceEditor()

    # Load the CSV file fuelPurchaseData
    priceConverter.load_csv()
    
    # Force the price to be 2 decimal places
    priceConverter.round_column_c()
    
    # Remove duplicate rows
    priceConverter.remove_duplicates()
    
    # Remove rows of pepsi purchases
    priceConverter.remove_pepsi_rows()
    
    # Save the results to a new CSV file called dataAnomalies
    priceConverter.save_csv("Data/dataAnomalies.csv")

    # Parameters for the address cleaning method
    api_key = "ea061a30-1649-11f0-8845-33c76b16c565"
    input_file = "Data/dataAnomalies.csv"
    output_file = "Data/cleanedData.csv"

    # Instantiate an object of the AddressCleaner class
    cleaner = AddressCleaner(input_file, output_file, api_key)
    # Run the clean addresses method on the cleaner object
    cleaner.clean_addresses()