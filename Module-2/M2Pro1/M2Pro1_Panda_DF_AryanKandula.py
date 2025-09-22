"""
East Coast State Parks Helper Program
09/21/2025
CSC221 M2Pro1 Panda DF
Aryan Kandula

Pseudocode (Algorithm):
1. Import pandas and park_functions module.
2. Define main() function.
    a. Try to load the Excel file once at the start.
    b. If file not found or dependency missing, show error and exit.
    c. Display menu in a loop until user enters 9.
    d. Call the correct function from park_functions_AryanKandula based on choice.
    e. Handle invalid inputs with exception handling.
3. Call main() when program starts.
"""

import pandas as pd
import park_functions_AryanKandula  # custom functions

def main():
    try:
        # Load dataset once
        df = pd.read_excel("east_coast_major_state_parks-1.xlsx")
        print("\n✅ Dataset loaded successfully!\n")

    except FileNotFoundError:
        print("❌ Error: Dataset file not found. Please check filename and path.")
        return
    except ImportError:
        print("❌ Error: Missing openpyxl. Please install it using 'pip install openpyxl'.")
        return
    except Exception as e:
        print("❌ Error loading dataset:", e)
        return

    choice = 0
    while choice != 9:
        print("\n--- Menu ---")
        print("1. Display First 15 records in dataset")
        print("2. Get Number of record(parks) listed in dataset")
        print("3. Get Number of State Parks by State")
        print("4. Get Number of State Parks per Region")
        print("5. Get Top 2, by acreage, per Region")
        print("6. Get State Parks with Waterfalls by State")
        print("7. Search Parks by Feature")
        print("8. Allow to Search DataFrame by State Code")
        print("9. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number from the menu.")
            choice = 0
            continue

        if choice == 1:
            park_functions_AryanKandula.show_first_15(df)
        elif choice == 2:
            park_functions_AryanKandula.count_records(df)
        elif choice == 3:
            park_functions_AryanKandula.count_parks_per_state(df)
        elif choice == 4:
            park_functions_AryanKandula.count_parks_by_region(df)
        elif choice == 5:
            park_functions_AryanKandula.top2_by_region(df)
        elif choice == 6:
            park_functions_AryanKandula.waterfalls_by_state(df)
        elif choice == 7:
            park_functions_AryanKandula.search_by_feature(df)
        elif choice == 8:
            park_functions_AryanKandula.search_by_state_code(df)
        elif choice == 9:
            print("👋 Thank you for using the program. Goodbye!")
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()