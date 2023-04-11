import sqlite3 
import pandas as pd

def main():
    try:
        df = pd.read_csv("final_cars_datasets.csv").head(10)
        for index, row in df.iterrows():
            print(row["price"], row["mark"])
    except Exception as e:
        print("Erorr occured: ", e)

    finally:
       print("DOne")
if __name__ == "__main__":
    main()