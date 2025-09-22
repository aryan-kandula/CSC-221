import pandas as pd

# State to Code map
STATE_CODES = {
    "Georgia": "GA",
    "Maryland": "MD",
    "North Carolina": "NC",
    "South Carolina": "SC",
    "Virginia": "VA"
}

# State to Region map
REGION_MAP = {
    "Virginia": "Mid-Atlantic",
    "Maryland": "Mid-Atlantic",
    "North Carolina": "Southeast",
    "South Carolina": "Southeast",
    "Georgia": "Southeast"
}

# 1
def show_first_15(df):
    print("\n--- First 15 Records ---")
    print(df.head(15).to_string(index=False))

# 2
def count_records(df):
    print("\n--- Total Number of Records ---")
    print("Number of parks listed:", len(df))

# 3
def count_parks_per_state(df):
    print("\n--- Number of Parks per State ---")
    result = df.groupby("STATE").size()
    print(result)

# 4
def count_parks_by_region(df):
    print("\n--- Number of Parks per Region ---")
    df["REGION"] = df["STATE"].map(REGION_MAP)
    result = df.groupby("REGION").size()
    print(result)

# 5
def top2_by_region(df):
    print("\n--- Top 2 Parks by Acreage per Region ---")
    df["REGION"] = df["STATE"].map(REGION_MAP)
    result = df.sort_values(["REGION", "ACREAGE"], ascending=[True, False])
    result = result.groupby("REGION").head(2)
    print(result[["REGION", "STATE", "PARK NAME", "ACREAGE"]].to_string(index=False))

# 6
def waterfalls_by_state(df):
    print("\n--- Parks with Waterfalls by State ---")
    result = df[df["FEATURE"].str.contains("Waterfall", case=False, na=False)]
    if result.empty:
        print("No parks with waterfalls found.")
    else:
        print(result[["STATE", "COUNTY", "PARK NAME", "FEATURE"]].to_string(index=False))

# 7
def search_by_feature(df):
    feature = input("Enter feature to search for: ").strip().capitalize()
    result = df[df["FEATURE"].str.contains(feature, case=False, na=False)]
    if result.empty:
        print(f"No parks found with feature: {feature}")
    else:
        print(result[["STATE", "COUNTY", "PARK NAME", "FEATURE"]].to_string(index=False))

# 8
def search_by_state_code(df):
    code = input("Enter state code: ").strip().upper()
    if code not in STATE_CODES.values():
        print("❌ Invalid state code. Dataset only includes GA, MD, NC, SC, VA.")
        return
    state_name = [k for k, v in STATE_CODES.items() if v == code][0]
    df["STATE CODE"] = df["STATE"].map(STATE_CODES)
    result = df[df["STATE CODE"] == code]
    if result.empty:
        print(f"No parks found for {state_name}.")
    else:
        print(result[["PARK NAME", "REGION", "ACREAGE", "FEATURE", "STATE CODE"]].to_string(index=False))
