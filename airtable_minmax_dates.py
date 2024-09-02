import os
from pyairtable import Table
from datetime import datetime

# Airtable configuration
TOKEN = os.environ["AIRTABLE_TOKEN"]
BASE_ID = "appeKpwmbTIiH15Vw"
TABLE_NAME = "Inventory List"


def find_min_max_dates():
    # Connect to Airtable
    table = Table(TOKEN, BASE_ID, TABLE_NAME)

    # Fetch all records
    all_records = table.all()

    # Date field you want to evaluate (adjust according to your table)
    date_field = "Next Delivery"  # Change to the name of your date field
    item_field = "Items"  # Field containing the name of the item

    # Initialize variables to store the min and max dates
    min_date = None
    max_date = None
    min_record = None
    max_record = None

    for record in all_records:
        date_str = record["fields"].get(date_field)
        if date_str:
            # Convert the string date to a datetime object
            date = datetime.fromisoformat(date_str)
            if min_date is None or date < min_date:
                min_date = date
                min_record = record
            if max_date is None or date > max_date:
                max_date = date
                max_record = record

    # Output the results
    if min_date and max_date:
        min_item_name = min_record["fields"].get(item_field, "Unknown")
        max_item_name = max_record["fields"].get(item_field, "Unknown")
        print(f"Minimum Date: {min_date}, Item Name: {min_item_name}")
        print(f"Maximum Date: {max_date}, Item Name: {max_item_name}")

        # Optionally, do something with these records, like returning them
        return min_record, max_record
    else:
        print("No valid date records found.")


def main():
    min_record, max_record = find_min_max_dates()
    # Further processing can be done here if needed


if __name__ == "__main__":
    main()
