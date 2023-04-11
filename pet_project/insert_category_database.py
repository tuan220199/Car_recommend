import sqlite3
import pandas as pd

def main():
    try:
        # Set up the database with sqlite 3
        db = sqlite3.connect("pet/db.sqlite3")

        df = pd.read_csv("final_cars_datasets.csv")
        category = set(df["mark"])
        category = list(category)
        num = 1

        for cate in category:
            db.execute("INSERT INTO car_category (id,groups) values (?,?)", (num,cate))
            db.commit()
            num+=1
            print(cate)

        print("Done")

    except Exception as e:
        print("Error occurred: ", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()
