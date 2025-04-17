# ----------------------
# Import Required Modules
# ----------------------
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime
import plotly.express as px

from database import get_data_from_db
from data_processing import (
    process_data,
    calculate_phase_durations_and_counts,
    calculate_average_duration,
)
from graphs import (
    create_avg_duration_bar,
    create_phase_count_bar,
    create_gantt_chart,
)

TAB_COUNT = 2  # Number of tabs (views)
INTERVAL_DURATION = 15 * 1000  # Interval duration in milliseconds (15 seconds)

# ----------------------
# Initialize Dash App
# ----------------------
app = dash.Dash(__name__)
app.title = "Phase Dashboard"

# ----------------------
# App Layout
# ----------------------
app.layout = html.Div(
    [
        # Store to keep track of which tab (view) is currently active
        dcc.Store(id="current-tab-index", data=0),
        # Dropdown for selecting date ranges (populated dynamically)
        dcc.Dropdown(
            id="date-selector",
            options=[{"label": "All Data", "value": "all"}],  # Default option
            value="all",
            clearable=False,
            style={
                "width": "50%",
                "margin": "0 auto",
                "color": "black",
                "backgroundColor": "black",
                "cursor": "auto",
            },
        ),
        # Button to manually switch between views (tabs)
        html.Button(
            "Next Graph",
            id="switch-tab-button",
            style={
                "backgroundColor": "black",
                "color": "white",
                "border": "1px solid white",
                "padding": "5px 10px",
                "cursor": "pointer",
                "display": "block",
                "margin": "10px auto",
            },
        ),
        # Div container for all tab content (both views are here, only one is shown at a time)
        html.Div(
            id="tabs-content",
            children=[
                # ------------------ Tab 0: Bar Graphs ------------------
                html.Div(
                    id="tab-0",
                    children=[
                        html.Div(
                            id="bar-graphs-container",
                            children=[
                                dcc.Graph(id="avg-duration-bar"),  # Avg phase durations
                                dcc.Graph(id="count-phase-bar"),  # Count per phase
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "width": "100%",
                                "gap": "10px",
                            },
                        ),
                    ],
                    style={"display": "flex", "flexWrap": "wrap"},  # Initially shown
                ),
                # ------------------ Tab 1: Gantt Chart ------------------
                html.Div(
                    id="tab-1",
                    children=[
                        dcc.Graph(id="gantt-chart"),  # Gantt chart showing timeline
                    ],
                    style={"display": "none"},  # Initially hidden
                ),
            ],
        ),
        # Automatic update interval (used for refreshing graphs or auto-switching views)
        dcc.Interval(
            id="interval-component", interval=INTERVAL_DURATION, n_intervals=0
        ),
    ]
)

# ----------------------
# Callback: Handle Tab Switching (Manual or Timed)
# ----------------------
@app.callback(
    Output("current-tab-index", "data"),
    [
        Input("interval-component", "n_intervals"),
        Input("switch-tab-button", "n_clicks"),
    ],
    [State("current-tab-index", "data")],
)
def cycle_tabs(n, n_clicks, current_tab_index):
    # If button has not been clicked, do nothing
    if n_clicks is None:
        return current_tab_index
    # Otherwise, toggle between tabs 0 and 1
    return (current_tab_index + 1) % TAB_COUNT


# ----------------------
# Callback: Update Tab Visibility
# ----------------------
@app.callback(
    [
        Output("tab-0", "style"),
        Output("tab-1", "style"),
    ],
    Input("current-tab-index", "data"),
)
def display_tab_content(tab_index):
    # Show tab 0 content if index is 0, otherwise hide it
    tab_0_style = (
        {"display": "flex", "flexWrap": "wrap"}
        if tab_index == 0
        else {"display": "none"}
    )
    # Show tab 1 content if index is 1, otherwise hide it
    tab_1_style = {"display": "block"} if tab_index == 1 else {"display": "none"}
    return tab_0_style, tab_1_style


# ----------------------
# Callback: Update All Graphs and Dropdown Options
# ----------------------
@app.callback(
    [
        Output("date-selector", "options"),
        Output("avg-duration-bar", "figure"),
        Output("count-phase-bar", "figure"),
        Output("gantt-chart", "figure"),
    ],
    [Input("interval-component", "n_intervals"), Input("date-selector", "value")],
)
def update_graphs(n_intervals, selected_date):
    # Fetch data and available dates from database
    data, available_dates = get_data_from_db()

    # Create dropdown options based on available dates
    dropdown_options = [{"label": date, "value": date} for date in available_dates]
    dropdown_options.insert(
        0, {"label": "All Data", "value": "all"}
    )  # Add default option

    # If no data is available, return empty graphs
    if not data:
        return dropdown_options, {}, {}, {}

    # Filter and process the raw data based on selected date
    filtered_data = process_data(data, selected_date)

    # Calculate phase durations and how many times each phase appears
    phase_durations, phase_counts = calculate_phase_durations_and_counts(filtered_data)

    # Compute average duration per phase
    avg_durations = calculate_average_duration(phase_durations, phase_counts)

    # Assign a unique color to each phase using Plotly's qualitative color set
    phase_colors = {
        phase: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
        for i, phase in enumerate(phase_durations)
    }

    # Format data into Gantt chart-friendly structure
    gantt_data = []
    for target_id, date_entries in filtered_data.items():
        for date, phases in date_entries.items():
            for i, (phase, start_time) in enumerate(phases):
                # Use next phase's start as this phase's end time, or duplicate start if last
                end_time = phases[i + 1][1] if i + 1 < len(phases) else start_time
                gantt_data.append(
                    {
                        "Task": phase,
                        "Start": start_time,
                        "Finish": end_time,
                        "Target ID": target_id,
                    }
                )

    # Create Plotly graph objects
    avg_duration_bar = create_avg_duration_bar(avg_durations, phase_colors)
    phase_count_bar = create_phase_count_bar(phase_counts, phase_colors)
    gantt_chart = create_gantt_chart(gantt_data, phase_colors)

    # Return updated graphs and dropdown options
    return dropdown_options, avg_duration_bar, phase_count_bar, gantt_chart


# ----------------------
# Run the App
# ----------------------
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
