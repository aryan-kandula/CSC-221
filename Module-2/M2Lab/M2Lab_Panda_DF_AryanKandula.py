# S&P 500 Price Data Analysis using Pandas
# Date: 09/14/2025
# CSC221 M2Lab – Panda DF
# Aryan Kandula

import pandas as pd

def load_csv_file(filename):
    """
    Load a CSV file into a Pandas DataFrame with error handling.
    """
    try:
        df = pd.read_csv(filename)
        print(f"✅ Successfully loaded {filename}\n")
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file {filename} was not found.\n")
    except pd.errors.EmptyDataError:
        print(f"❌ Error: The file {filename} is empty.\n")
    except Exception as e:
        print(f"❌ Unexpected error while loading {filename}: {e}\n")
    return None

def main():
    # Step A: Load Data
    print("=== Step A: Load Data ===")
    constituents = load_csv_file("SP500_Constituents.csv")
    prices = load_csv_file("SP500_Adjusted_Prices.csv")

    if constituents is None or prices is None:
        print("Program terminated due to file loading error.")
        return

    print("Constituents DataFrame (first 5 rows):")
    print(constituents.head(), "\n")
    print("Prices DataFrame (first 5 rows):")
    print(prices.head(), "\n")

    # Step B: Rotate Data
    print("=== Step B: Rotate Data ===")
    try:
        rotated = prices.pivot(index="Symbol", columns="Date", values="Adjusted_price")
        print("Rotated Price DataFrame (first 5 rows):")
        print(rotated.head(), "\n")
    except Exception as e:
        print(f"❌ Error while rotating data: {e}")
        return

    # Step C: Join Data
    print("=== Step C: Join Data ===")
    try:
        merged = constituents.join(rotated, on="Symbol")
        print("Joined DataFrame (first 5 rows):")
        print(merged.head(), "\n")
    except Exception as e:
        print(f"❌ Error while joining data: {e}")
        return

    # Step D: Augment Data
    print("=== Step D: Augment Data ===")
    try:
        last_two = rotated.columns[-2:]
        merged["PriceDiff"] = merged[last_two[-1]] - merged[last_two[0]]
        print("DataFrame with PriceDiff column (first 5 rows):")
        print(merged[["Symbol", last_two[-1], last_two[0], "PriceDiff"]].head(), "\n")
    except Exception as e:
        print(f"❌ Error while augmenting data: {e}")
        return

    # Step E: Missing Values
    print("=== Step E: Missing Values ===")
    try:
        missing = merged[merged.isnull().any(axis=1)]
        if missing.empty:
            print("No stocks are missing price data.\n")
        else:
            print("Stocks with missing price data:")
            print(missing[["Symbol", "Security"]], "\n")
    except Exception as e:
        print(f"❌ Error while checking missing values: {e}")
        return

# Run main program
if __name__ == "__main__":
    main()
