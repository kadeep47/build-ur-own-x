# analyze_and_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def analyze_from_csv(filepath="learning_progress.csv"):
    """
    1. Read the CSV with columns:
       Topic, Weightage (%), Planned Start, Planned End,
       Actual Start, Actual End, Level
    2. Compute each topic's Actual Days and Productivity (%/day).
    3. Build a date range from the earliest Planned Start → latest Planned End.
    4. For each day in that range, calculate:
         - expected cumulative %  (linear interpolation across planned durations)
         - actual cumulative %    (linear interpolation across actual durations)
    5. Plot two overlaid line charts:
         • Expected Cumulative % (blue)
         • Actual   Cumulative % (red)
       and save as "expected_vs_actual_progress.png".
    6. Build a Gantt‐style chart: one horizontal bar for each topic’s Planned dates
       (light gray), and one overlaid bar for each topic’s Actual dates (dark gray).
       Save as "gantt_timeline.png".
    """

    # ----- 1) Load CSV -----
    df = pd.read_csv(filepath)

    # Convert all relevant columns to datetime
    for col in ["Planned Start", "Planned End", "Actual Start", "Actual End"]:
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")

    # Ensure Weightage is a float
    df["Weightage (%)"] = df["Weightage (%)"].astype(float)

    # ----- 2) Compute "Actual Days" and "Productivity (%/day)" -----
    df["Actual Days"] = (df["Actual End"] - df["Actual Start"]).dt.days + 1
    df["Productivity (%/day)"] = df["Weightage (%)"] / df["Actual Days"]

    # ----- 3) Build a full date range for plotting cumulative progress -----
    overall_start = df["Planned Start"].min()
    overall_end   = df["Planned End"].max()
    full_dates = pd.date_range(start=overall_start, end=overall_end)

    expected_cum = []
    actual_cum   = []

    # ----- 4) For each date, sum up "expected" and "actual" contributions -----
    for single_date in full_dates:
        exp_sum = 0.0
        act_sum = 0.0

        # Loop through each topic
        for _, row in df.iterrows():
            p_start, p_end    = row["Planned Start"], row["Planned End"]
            a_start, a_end    = row["Actual Start"], row["Actual End"]
            weight            = row["Weightage (%)"]

            # Planned duration (days)
            planned_days = (p_end - p_start).days + 1
            if single_date >= p_end:
                # Entire weight counts as completed
                exp_sum += weight
            elif p_start <= single_date < p_end:
                # Partially complete based on how far into planned period we are
                days_into_planned = (single_date - p_start).days + 1
                exp_sum += weight * (days_into_planned / planned_days)

            # Actual duration (days)
            actual_days = (a_end - a_start).days + 1
            if single_date >= a_end:
                # Entire weight counts as completed
                act_sum += weight
            elif a_start <= single_date < a_end:
                # Partially complete based on how far into actual period we are
                days_into_actual = (single_date - a_start).days + 1
                act_sum += weight * (days_into_actual / actual_days)

        expected_cum.append(exp_sum)
        actual_cum.append(act_sum)

    # ----- 5) Plot Expected vs. Actual Cumulative Progress (Line Chart) -----
    plt.figure(figsize=(10, 5))
    plt.plot(full_dates, expected_cum, color="blue", label="Expected Cumulative %")
    plt.plot(full_dates, actual_cum,   color="red",  label="Actual Cumulative %")
    plt.fill_between(full_dates, expected_cum, color="blue", alpha=0.1)
    plt.fill_between(full_dates, actual_cum,   color="red",  alpha=0.1)

    plt.xlabel("Date")
    plt.ylabel("Cumulative Completion (%)")
    plt.title("Expected vs. Actual Learning Progress")
    plt.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("expected_vs_actual_progress.png")
    plt.show()

    # ----- 6) Plot Gantt‐Style Timeline (Planned vs. Actual for each topic) -----
    plt.figure(figsize=(10, 6))
    for idx, row in df.iterrows():
        topic    = row["Topic"]
        p_start  = row["Planned Start"]
        p_end    = row["Planned End"]
        a_start  = row["Actual Start"]
        a_end    = row["Actual End"]

        y = idx  # each topic on its own horizontal position

        # Plot planned as a thick, light-gray bar
        plt.barh(
            y,
            (p_end - p_start).days + 1,
            left=p_start,
            height=0.4,
            color="lightgray",
            label="Planned" if idx == 0 else ""  # only label once
        )

        # Plot actual as a narrower, dark-gray bar on top
        plt.barh(
            y - 0.15,
            (a_end - a_start).days + 1,
            left=a_start,
            height=0.3,
            color="dimgray",
            label="Actual" if idx == 0 else ""
        )

    plt.yticks(range(len(df)), df["Topic"])
    ax = plt.gca()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Date")
    plt.title("Gantt‐Style Timeline: Planned vs. Actual")
    plt.legend()
    plt.tight_layout()
    plt.savefig("gantt_timeline.png")
    plt.show()

    return df, full_dates, expected_cum, actual_cum


if __name__ == "__main__":
    # Running this module will:
    # 1) Read "learning_progress.csv"
    # 2) Compute productivity metrics
    # 3) Save two charts:
    #      - expected_vs_actual_progress.png
    #      - gantt_timeline.png
    #
    df_metrics, dates, exp_line, act_line = analyze_from_csv("learning_progress.csv")
    # If you want to inspect the DataFrame of computed metrics:
    print(df_metrics)
