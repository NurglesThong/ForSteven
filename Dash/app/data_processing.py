from datetime import datetime

# ----------------------
# Function: Process Data
# ----------------------
def process_data(data, selected_date):
    """
    Organizes raw phase data by target ID and date.

    Args:
        data (list of tuples): Each tuple contains (target_id, phase_timestamp, phase).
        selected_date (str): A specific date in "YYYY-MM-DD" format or "all" to include all dates.

    Returns:
        dict: Nested dictionary in the form {target_id: {date: [(phase, timestamp), ...]}}.
    """
    # Dictionary to store the processed data (organized by target ID and date)
    organized_data = {}

    # Iterate through each entry in the raw data
    for target_id, timestamp_str, phase in data:
        # Convert timestamp string to a Python datetime object for easy manipulation
        phase_timestamp = datetime.strptime(str(timestamp_str), "%Y-%m-%d %H:%M:%S")

        # Extract just the date part (YYYY-MM-DD) to use for filtering later
        date_only = phase_timestamp.date()

        # If a specific date is selected and it doesn't match the current one, skip this entry
        if selected_date != "all" and str(date_only) != selected_date:
            continue

        # Organize data using a nested dictionary:
        # Outer key: target_id
        # Inner key: date
        # Value: a list of tuples (phase, timestamp)
        organized_data.setdefault(target_id, {}).setdefault(date_only, []).append(
            (phase, phase_timestamp)
        )

    return organized_data


# ----------------------
# Function: Calculate Phase Durations and Counts
# ----------------------
def calculate_phase_durations_and_counts(organized_data):
    """
    Calculates total duration and count of occurrences for each phase.

    Args:
        organized_data (dict): The output from `process_data`, containing organized phase data.

    Returns:
        tuple: Two dictionaries:
            - phase_durations: Total time spent in each phase (in seconds).
            - phase_counts: How many times each phase occurred.
    """
    # Initialize dictionaries to hold phase durations and counts
    phase_durations = {}
    phase_counts = {}

    # Loop through each target's data
    for target_id, date_entries in organized_data.items():
        # Loop through each date for the target
        for date, phases in date_entries.items():
            # Loop through the phase sequence and calculate the duration between consecutive phases
            for i in range(len(phases) - 1):
                current_phase, start_time = phases[i]
                _, end_time = phases[i + 1]

                # Calculate the duration between the current phase and the next one (in seconds)
                duration = (end_time - start_time).total_seconds()

                # Ensure the phase keys are initialized in the dictionaries
                phase_durations.setdefault(current_phase, 0)
                phase_counts.setdefault(current_phase, 0)

                # Add the duration to the total duration for this phase
                phase_durations[current_phase] += duration
                # Increment the count of how many times this phase occurred
                phase_counts[current_phase] += 1

    # Return both dictionaries: total durations and counts per phase
    return phase_durations, phase_counts


# ----------------------
# Function: Calculate Average Duration
# ----------------------
def calculate_average_duration(phase_durations, phase_counts):
    """
    Calculates the average duration (in minutes) for each phase.

    Args:
        phase_durations (dict): A dictionary containing total duration (in seconds) for each phase.
        phase_counts (dict): A dictionary containing the number of occurrences for each phase.

    Returns:
        dict: A dictionary with the average duration for each phase in minutes, rounded to 2 decimals.
    """
    # Initialize dictionary to hold the average duration for each phase
    average_durations = {}

    # Loop through each phase and calculate the average duration
    for phase in phase_durations:
        # Average = total duration / count of occurrences, converted to minutes
        avg_minutes = (
            phase_durations[phase] / phase_counts[phase] / 60
        )  # Convert seconds to minutes
        # Store the result, rounded to 2 decimal places
        average_durations[phase] = round(avg_minutes, 2)

    # Return the dictionary of average durations
    return average_durations
