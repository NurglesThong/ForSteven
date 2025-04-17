import psycopg2

# ----------------------
# Function: Get Data from Database
# ----------------------
def get_data_from_db():
    """
    Connects to a PostgreSQL database, fetches all phase data, and retrieves available unique dates.

    Returns:
        tuple:
            - data (list of tuples): All records in the form (target_id, phase_timestamp, phase),
              ordered by timestamp.
            - available_dates (list of str): List of unique dates (YYYY-MM-DD) as strings, used for filtering.
    """
    try:
        print("Attempting to connect to the database...")

        # Establish a connection to the PostgreSQL database
        # The connection string includes:
        #   - host: Address of the database server (could be 'localhost' or container name if using Docker)
        #   - port: Default port for PostgreSQL (5432)
        #   - dbname: Name of the database you're connecting to
        #   - user: Username to authenticate with
        #   - password: Password for the user
        conn = psycopg2.connect(
            host="postgres",  # Database host (usually a container name or localhost)
            port="5432",  # Default PostgreSQL port
            dbname="data",  # Database name
            user="admin",  # Username for authentication
            password="admin",  # Password for authentication
        )

        # Print a success message when the connection is established
        print("Connection successful!")

        # Create a cursor object which will be used to execute SQL queries
        cur = conn.cursor()

        # Query to retrieve all phase data ordered by timestamp
        # This will fetch the target_id, timestamp, and phase columns from the 'data' table
        fetch_all_data_query = """
            SELECT target_id, phase_timestamp, phase
            FROM data
            ORDER BY phase_timestamp
        """
        # Execute the query to fetch all data
        cur.execute(fetch_all_data_query)

        # Fetch all rows from the executed query and store them in the variable 'data'
        # Each row will be a tuple (target_id, phase_timestamp, phase)
        data = cur.fetchall()
        print(f"Fetched {len(data)} rows from the database.")

        # Query to retrieve unique dates from the phase_timestamp column
        # This query will give us a list of distinct dates that appear in the database
        unique_dates_query = """
            SELECT DISTINCT DATE(phase_timestamp)
            FROM data
            ORDER BY DATE(phase_timestamp)
        """
        # Execute the query to fetch unique dates
        cur.execute(unique_dates_query)

        # Fetch all the unique dates, which will be returned as a list of tuples (date,)
        raw_dates = cur.fetchall()

        # Convert the tuples (e.g., (2024-04-01,)) into a simple string "2024-04-01"
        available_dates = [str(date_tuple[0]) for date_tuple in raw_dates]

        # Close the cursor and connection to the database to free up resources
        cur.close()
        conn.close()

        # Return the fetched data (list of tuples) and the list of available dates
        return data, available_dates

    except Exception as e:
        # If an exception occurs during the process, catch it and print a user-friendly error message
        print(f"Error connecting to the database: {e}")
        # Return empty lists in case of an error to ensure the function doesn't break other code
        return [], []
