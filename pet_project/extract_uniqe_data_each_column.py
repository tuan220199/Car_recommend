import pandas as pd

def main():
    try:
        df = pd.read_csv("final_cars_datasets.csv")
        transmission = set(df["transmission"])
        drive = set(df["drive"])
        hand_drive = set(df["hand_drive"])
        fuel = set(df["fuel"])

        print(len(transmission),transmission)
        print(len(drive),drive)
        print(len(hand_drive),hand_drive)
        print(len(fuel),fuel)
    except Exception as e:
        print("Error occurred: ", e)
    
    finally:
        print("Done")

if __name__ == "__main__":
    main()