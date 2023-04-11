import sqlite3 
import pandas as pd 

def main():
    db= sqlite3.connect("pet/db.sqlite3")
    df = pd.read_csv("final_cars_datasets.csv")
        
    num = 1
    for index, row in df.iterrows():
        mark = row["mark"]

        # Define the owner by id related to user table
        owner = 1 
        if num%4 == 0:
            owner = 4
        elif num%4 == 1:
            owner = 1
        elif num%4 == 2:
            owner = 2
        else:
            owner = 3    
            
        # Extract data from the databse: table car_category
        cursor = db.cursor()
        cursor.execute("SELECT * FROM car_category")
        categories = cursor.fetchall()

            
        mark_category = 1
        for category in categories:
            if (category[1] == mark):
                mark_category = category[0]

        db.execute("INSERT INTO car_car (price, year, mileage, engine_capacity, model, transmission, drive, hand_drive, fuel, image_url, mark_category_id, owner_id) values (?,?,?,?,?,?,?,?,?,?,?,?)", (row["price"], row["year"], row["mileage"], row["engine_capacity"], row["model"], row["transmission"], row["drive"], row["hand_drive"], row["fuel"], row["image_url"], mark_category, owner))
        db.commit()
            
        num+=1    
    
    db.close()

if __name__ == "__main__":
    main()