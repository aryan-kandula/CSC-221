# Country Statistics Lookup Program
# Date: 09/07/2025
# CSC221 M1Pro – Review
# Aryan Kandula
#
# Pseudocode:
# Display a welcome message
# Ask the user for a country code
# Repeat until the user enters "stop"
#     If the country code is valid (US, CA, MX):
#         Ask for a statistic (pop, gdp, ccy, fx)
#         If the statistic is valid:
#             Look up and display the value
#         Else:
#             Show an invalid statistic message
#     Else if the country code is not stop:
#         Show an invalid country code message
# End the program when the user enters "stop"

import Country_Functions_AryanKandula

def main():
    """
    Main program that asks user for a country code and statistic,
    and looks up the value from the dictionary.
    Program continues until user enters STOP.
    """

    print("Welcome to the Country Statistics Lookup Program")
    print("Type 'stop' anytime as country code to quit.\n")

    # start with empty so loop runs
    country = ""

    # sentinel loop
    while country != "STOP":
        country = input("Please enter a country code (US, CA, MX): ")
        country = country.upper()

        if country == "STOP":
            print("Program ended. Thank you!")
        elif country == "US" or country == "CA" or country == "MX":
            measure = input("Please enter a statistic (pop, gdp, ccy, fx): ")
            measure = measure.lower()

            if measure == "pop" or measure == "gdp" or measure == "ccy" or measure == "fx":
                value = Country_Functions_AryanKandula.lookup_value(country, measure)
                print(country, measure, "=", value, "\n")
            else:
                print("Invalid statistic. Try again.\n")
        else:
            print("Invalid country code. Try again.\n")

# Run program
main()
