from datetime import datetime, timedelta

def process_date(input_date_str):
    # Convert the string to a datetime object
    current_date = datetime.now()
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

    # Check if the input date is equal to or later than the current date
    if input_date + timedelta(days=1) < current_date:
        return "The input date is earlier than the current date."

    # Check if the input date is not more than 5 months ahead of the current date
    five_months_later = current_date + timedelta(days=30 * 5)
    if input_date > five_months_later:
        return "The input date is more than 5 months ahead of the current date."

    # Add 30 days to the input date
    new_date = input_date + timedelta(days=30)

    # Return a string with the new date in the same format
    new_date_str = new_date.strftime('%Y-%m-%d')
    return new_date_str

# Example usage
input_date_str = "2024-05-19"
result = process_date(input_date_str)
print(result)
