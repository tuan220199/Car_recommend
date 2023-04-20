import sqlite3

def main():
    try:
        # Set up the database with sqlite 3
        db = sqlite3.connect("pet/db.sqlite3")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM car_category")
        categories = cursor.fetchall()

        for cate in categories:
            url = f"https://www.carlogos.org/car-logos/{cate[1]}-logo.png"
            db.execute("UPDATE car_category SET image_url_brand=? WHERE groups=? ", (url,cate[1]))
            db.commit()
        print("Done")

    except Exception as e:
        print("Error occurred: ", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()