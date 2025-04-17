import plotly.graph_objects as go
import plotly.express as px

# ----------------------
# Function: Create Average Duration Bar
# ----------------------
def create_avg_duration_bar(avg_duration, phase_colors):
    """
    Creates a horizontal bar chart showing the average duration (in minutes) for each phase.

    Args:
        avg_duration (dict): Average duration per phase {phase: avg_minutes}.
        phase_colors (dict): Mapping of phase names to specific colors {phase: color}.

    Returns:
        dict: A Plotly bar chart figure in dictionary format.
    """
    return {
        "data": [
            go.Bar(
                x=list(
                    avg_duration.values()
                ),  # The X-axis will show the duration values
                y=list(avg_duration.keys()),  # The Y-axis will show the phase names
                orientation="h",  # Specify a horizontal bar chart
                marker=dict(
                    color=[
                        phase_colors.get(
                            phase, "blue"
                        )  # Assign color for each phase or default to blue
                        for phase in avg_duration.keys()
                    ]
                ),
                text=list(
                    avg_duration.values()
                ),  # Add labels inside the bars to display duration
                textposition="inside",  # Position the text inside the bar
                insidetextfont=dict(
                    color="white", size=14
                ),  # Style the text with white color and a font size of 14
            )
        ],
        "layout": go.Layout(
            xaxis=dict(
                title="Average Duration (minutes)",  # Label for the X-axis
                color="white",  # Color of axis labels and ticks
                showgrid=True,  # Display gridlines on the X-axis
                tickformat=".0f",  # Remove decimal places from the tick marks
            ),
            yaxis=dict(title="Phase", color="white"),  # Label for the Y-axis
            paper_bgcolor="black",  # Set the background color of the entire figure
            plot_bgcolor="black",  # Set the background color of the plot area
            font=dict(color="white"),  # Set the font color to white for visibility
            autosize=True,  # Automatically adjust the layout size based on content
            margin=dict(l=50, r=50, t=50, b=50),  # Set margins around the plot
        ),
    }


# ----------------------
# Function: Create Phase Count Bar
# ----------------------
def create_phase_count_bar(phase_counts, phase_colors):
    """
    Creates a horizontal bar chart showing how many times each phase occurred.

    Args:
        phase_counts (dict): Count of how often each phase occurred {phase: count}.
        phase_colors (dict): Mapping of phase names to colors {phase: color}.

    Returns:
        dict: A Plotly bar chart figure in dictionary format.
    """
    return {
        "data": [
            go.Bar(
                x=list(phase_counts.values()),  # The X-axis will show the count values
                y=list(phase_counts.keys()),  # The Y-axis will show the phase names
                orientation="h",  # Horizontal bar chart
                marker=dict(
                    color=[
                        phase_colors.get(
                            phase, "blue"
                        )  # Use color mapping or default to blue
                        for phase in phase_counts.keys()
                    ]
                ),
                text=list(phase_counts.values()),  # Display the counts inside the bars
                textposition="inside",  # Place the text inside the bars
                insidetextfont=dict(
                    color="white", size=14
                ),  # Style the text inside the bars
            )
        ],
        "layout": go.Layout(
            xaxis=dict(
                title="Total", color="white", showgrid=True
            ),  # Label for the X-axis
            yaxis=dict(title="Phase", color="white"),  # Label for the Y-axis
            paper_bgcolor="black",  # Set the figure background to black
            plot_bgcolor="black",  # Set the plot background to black
            font=dict(color="white"),  # Set font color to white
            autosize=True,  # Auto-resize layout
            margin=dict(l=50, r=50, t=50, b=50),  # Set margins around the plot
        ),
    }


# ----------------------
# Function: Create Gantt Chart
# ----------------------
def create_gantt_chart(gantt_data, phase_colors):
    """
    Creates a Gantt chart to visualize phase durations over time for each target.

    Args:
        gantt_data (DataFrame): DataFrame containing columns: 'Target ID', 'Task', 'Start', 'Finish'.
        phase_colors (dict): Mapping of phases to colors for the timeline bars.

    Returns:
        plotly.graph_objects.Figure: A Gantt chart figure object.
    """
    # Create a timeline chart (Gantt chart) using Plotly Express
    fig = px.timeline(
        gantt_data,  # DataFrame that contains the Gantt chart data
        x_start="Start",  # Column in DataFrame indicating the start time of the phase
        x_end="Finish",  # Column in DataFrame indicating the finish time of the phase
        y="Target ID",  # Each row represents a target, placed on the Y-axis
        color="Task",  # The color of each bar is determined by the phase (Task)
        color_discrete_map=phase_colors,  # Map phase names to specific colors
        labels={"Target ID": "Target ID", "Task": "Phase"},  # Custom labels for axes
        title="Phase Duration Gantt Chart",  # Title of the chart
    )

    # Update layout settings for better appearance in dark mode
    fig.update_layout(
        yaxis_title="Target ID",  # Label for the Y-axis (Target ID)
        paper_bgcolor="black",  # Set the figure background color to black
        plot_bgcolor="black",  # Set the plot background color to black
        font=dict(color="white"),  # Set the font color to white for visibility
        showlegend=True,  # Show the legend for color mapping
        xaxis=dict(
            tickformat="%H:%M:%S", showgrid=True
        ),  # Time format on X-axis with gridlines
        yaxis=dict(showgrid=True),  # Display gridlines on the Y-axis
        autosize=True,  # Automatically adjust the layout size based on content
        margin=dict(l=50, r=50, t=50, b=50),  # Set margins around the plot area
    )

    # Return the Gantt chart figure
    return fig
