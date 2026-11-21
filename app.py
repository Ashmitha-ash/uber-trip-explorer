import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load and Clean Dataset ---
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "Uber file.csv")

if not os.path.exists(csv_path):
    # Fallback to local working directory
    csv_path = "Uber file.csv"

df = pd.read_csv(csv_path)

# Normalize column names
df.columns = df.columns.str.strip()

# Clean duplicate header rows if present
if "dispatching_base_number" in df.columns:
    df = df[df["dispatching_base_number"] != "dispatching_base_number"].copy()

# Parse numeric columns
df["active_vehicles"] = pd.to_numeric(df["active_vehicles"], errors="coerce").fillna(0).astype(int)
df["trips"] = pd.to_numeric(df["trips"], errors="coerce").fillna(0).astype(int)

# Standardize date and time
if "Date/Time" in df.columns:
    df["datetime"] = pd.to_datetime(df["Date/Time"], dayfirst=True, errors="coerce")
else:
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")

df = df.dropna(subset=["datetime"]).copy()
df["date"] = df["datetime"].dt.date
df["hour"] = df["datetime"].dt.hour
df["base"] = df["dispatching_base_number"]

# Unique bases and dates for dropdown choices
unique_bases = ["All"] + sorted(df["base"].dropna().unique().tolist())
unique_dates = sorted(df["date"].dropna().unique().tolist())
unique_dates_str = [str(d) for d in unique_dates]

# Set visual styling
sns.set_theme(style="whitegrid")

# --- Analysis & Visualization Function ---
def explore(base_choice, start_date_str, end_date_str, chart_type):
    try:
        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()
    except Exception:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "Invalid date selection.", ha="center", va="center", fontsize=14)
        return "0", "0", "N/A", "N/A", fig, pd.DataFrame({"Error": ["Invalid date format."]})

    # Filter by Date
    filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Filter by Base
    if base_choice != "All":
        filtered = filtered[filtered["base"] == base_choice]

    # Handle empty dataset
    if filtered.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No records found for the selected filter.", ha="center", va="center", fontsize=14)
        return "0", "0", "N/A", "N/A", fig, pd.DataFrame({"Message": ["No data matching criteria"]})

    # KPI Calculations
    t_trips = filtered["trips"].sum()
    t_veh = filtered["active_vehicles"].sum()
    total_trips = f"{t_trips:,}"
    total_vehicles = f"{t_veh:,}"

    # Peak hour & Top Base
    hourly_sum = filtered.groupby("hour")["trips"].sum()
    peak_hour = f"{hourly_sum.idxmax()}:00 ({hourly_sum.max():,} trips)"
    top_base = filtered.groupby("base")["trips"].sum().idxmax()

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 5))

    if chart_type == "Base Distribution (Pie Chart)":
        base_trips = filtered.groupby("base")["trips"].sum()
        colors = sns.color_palette("pastel")[0:len(base_trips)]
        ax.pie(
            base_trips,
            labels=base_trips.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        ax.set_title("Trip Share by Dispatching Base", fontsize=14, fontweight="bold", pad=15)

    elif chart_type == "Daily Trip Trend (Line Chart)":
        daily_trips = filtered.groupby("date")["trips"].sum().reset_index()
        sns.lineplot(data=daily_trips, x="date", y="trips", marker="o", ax=ax, color="#1f77b4", linewidth=2.5)
        ax.set_title("Daily Completed Trips Trend", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Total Completed Trips", fontsize=12)
        plt.xticks(rotation=30)

    else:  # Hourly Peak Trips (Bar Chart)
        hourly_trips = filtered.groupby("hour")["trips"].sum().reset_index()
        sns.barplot(
            data=hourly_trips,
            x="hour",
            y="trips",
            ax=ax,
            palette="Blues_d",
            hue="hour",
            legend=False
        )
        ax.set_title("Hourly Trip Distribution (Rush Hour Analysis)", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Hour of Day (0 - 23)", fontsize=12)
        ax.set_ylabel("Total Completed Trips", fontsize=12)

    plt.tight_layout()

    # Data preview table
    preview_cols = ["Date/Time", "dispatching_base_number", "active_vehicles", "trips"]
    preview_df = filtered[preview_cols].rename(columns={
        "Date/Time": "Date & Time",
        "dispatching_base_number": "Base Code",
        "active_vehicles": "Active Vehicles",
        "trips": "Trips Completed"
    }).head(100)

    return total_trips, total_vehicles, top_base, peak_hour, fig, preview_df


# --- Build Gradio Interface ---
with gr.Blocks(title="Uber Trip Explorer") as demo:
    gr.Markdown("# 🚖 Uber Trip Explorer & Analytics Dashboard")
    gr.Markdown(
        "Interactive dashboard to explore Uber trip demand, vehicle activity, and dispatching base operations. "
        "Filter by **Base** and **Date Range** to visualize key trends."
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Filter Controls")
            base_choice = gr.Dropdown(
                choices=unique_bases,
                value=unique_bases[0],
                label="📍 Select Dispatching Base"
            )
            start_date = gr.Dropdown(
                choices=unique_dates_str,
                value=unique_dates_str[0],
                label="📅 Start Date"
            )
            end_date = gr.Dropdown(
                choices=unique_dates_str,
                value=unique_dates_str[-1],
                label="📅 End Date"
            )
            chart_type = gr.Radio(
                choices=[
                    "Hourly Peak Trips (Bar Chart)",
                    "Base Distribution (Pie Chart)",
                    "Daily Trip Trend (Line Chart)"
                ],
                value="Hourly Peak Trips (Bar Chart)",
                label="📊 Select Chart Type"
            )
            explore_btn = gr.Button("🔍 Run Analysis", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("### 📈 Key Performance Indicators (KPIs)")
            with gr.Row():
                kpi_trips = gr.Textbox(label="Total Trips", interactive=False)
                kpi_vehicles = gr.Textbox(label="Active Vehicles", interactive=False)
                kpi_top_base = gr.Textbox(label="Top Base", interactive=False)
                kpi_peak_hour = gr.Textbox(label="Peak Rush Hour", interactive=False)

            plot_output = gr.Plot(label="Analytics Visualization")

    gr.Markdown("### 📋 Filtered Records Preview")
    table_output = gr.Dataframe(interactive=False)

    # Wire up button event
    explore_btn.click(
        fn=explore,
        inputs=[base_choice, start_date, end_date, chart_type],
        outputs=[kpi_trips, kpi_vehicles, kpi_top_base, kpi_peak_hour, plot_output, table_output]
    )

if __name__ == "__main__":
    demo.launch()
