from datetime import datetime, timedelta


def get_time_from_string(time_string):
    """
        sends a string, and returns a date in datetime format
        :param time_string: string
    """
    # Parse the time string
    format_str = "%Y-%m-%dT%H:%M:%S%z"
    datetime_object = datetime.strptime(time_string, format_str)

    # Get the time from the obtained datetime object
    time = datetime_object.time()

    return time


def process_date(input_date_str: str):  # Format YYYY-MM-DD

    """
        Check that the date entered is greater than the current date,

        Check that the date entered is NOT 5 months older than the current one

        returns a string with adding 60 days to the entered date
        Example: current_date="2024-01-01" input= "2024-05-19" , output= "2024-06-18"

        :param input_date_str: string
    """
    try:
        # Convert the string to a datetime object
        current_date = datetime.now()
        input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

        # Check if the input date is equal to or later than the current date
        if input_date + timedelta(days=1) < current_date:
            raise DateProcessingError("The input date is earlier than the current date.")  # Exception

        # Check if the input date is not more than 5 months ahead of the current date
        five_months_later = current_date + timedelta(days=30 * 5)
        if input_date > five_months_later:
            raise DateProcessingError("The input date is more than 5 months ahead of the current date.")  # Exception

        # Add 60 days to the input date
        new_date = input_date + timedelta(days=60)

        # Return a string with the new date in the same format
        new_date_str = new_date.strftime('%Y-%m-%d')
        return new_date_str

    except ValueError:
        raise DateProcessingError("Invalid date format. Please use 'YYYY-MM-DD'.")  # Exception


class DateProcessingError(Exception):
    pass
