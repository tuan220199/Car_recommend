import sqlite3

def main():
    try:
        # Set up the database with sqlite 3
        categories = {
            "gm": "https://gmauthority.com/blog/wp-content/uploads/2021/01/General-Motors-GM-Logo-Brandmark-Gradient-2021-lead-720x340.jpg",
            "kubota": "https://logos-world.net/wp-content/uploads/2020/12/Kubota-Logo-2010-present-700x394.png"
        }
        db = sqlite3.connect("pet/db.sqlite3")
        for cate in categories:
            db.execute("UPDATE car_category SET image_url_brand=? WHERE groups=? ", (categories[cate],cate))
        db.commit()
        print("Done")
        '''
        url27="https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/LandRover.svg/1200px-LandRover.svg.png"
        url28="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Kia-logo.png/1200px-Kia-logo.png"
        db = sqlite3.connect("pet/db.sqlite3")
        db.execute("UPDATE car_category SET image_url_brand=? WHERE id=? ", (url27,27))
        db.execute("UPDATE car_category SET image_url_brand=? WHERE id=? ", (url28,28))
        db.commit()
        '''
    except Exception as e:
        print("Error occurred: ", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()