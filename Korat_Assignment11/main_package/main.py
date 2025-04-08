# documentation

from data_cleaning_package.data_cleaning_2 import *

if __name__ == "__main__":
    priceConverter = GrossPriceEditor()
    priceConverter.load_csv()
    priceConverter.round_column_c()
    priceConverter.remove_duplicates()
    priceConverter.remove_pepsi_rows()
    priceConverter.save_csv("Data/dataAnomalies.csv")