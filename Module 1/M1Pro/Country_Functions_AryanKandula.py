# Country Functions Module
# CSC221 M1Pro – Review
# Aryan Kandula

# Dictionary with country data and its statistics
allData = {
    'US': {'pop': 325.7, 'gdp': 19.39, 'ccy': 'USD', 'fx': 1.0},
    'CA': {'pop': 36.5, 'gdp': 1.65, 'ccy': 'CAD', 'fx': 1.35},
    'MX': {'pop': 129.2, 'gdp': 1.15, 'ccy': 'MXN', 'fx': 19.68}
}

def lookup_value(code, measure):
    """
    Looks up and returns the value for a given country code and measure.
    :param code: string (country code, e.g., 'US')
    :param measure: string (measure name, e.g., 'pop')
    :return: the value from the dictionary
    """
    return allData[code][measure]
