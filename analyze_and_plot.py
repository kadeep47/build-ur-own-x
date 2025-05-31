# analyze_and_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from math import pi

def analyze_from_csv(filepath="learning_progress.csv"):
    """
    1. Read CSV with columns:
         Topic, Weightage (%), Planned Start, Planned End,
         Actual Start, Actual End, Level
    2. Compute each topic’s “Actual Days” and “Productivity (%/day)”.
    3. Build a full date range (earliest Planned Start → latest Planned End).
    4. For each date in that range, compute:
         - expected cumulative % (linear interpolation across planned period)
         - actual   cumulative % (linear interpolation across actual period)
    5. Plot & save:
         • expected_vs_actual_progress.png  (two lines + markers)
         • gantt_timeline.png               (planned bars in blue, actual in red)
         • productivity_bar_chart.png       (bars colored by Level)
         • calendar_heatmap.png             (daily increments heatmap)
         • radar_spider_chart.png           (topic vs productivity on a spider chart)
    """

    # ----- 1) Load CSV -----
    df = pd.read_csv(filepath)

    # Convert date columns to datetime
    for col in ["Planned Start", "Planned End", "Actual Start", "Actual End"]:
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")

    # Ensure weightage is float
    df["Weightage (%)"] = df["Weightage (%)"].astype(float)

    # ----- 2) Compute Actual Days & Productivity (%/day) -----
    df["Actual Days"] = (df["Actual End"] - df["Actual Start"]).dt.days + 1
    df["Productivity (%/day)"] = df["Weightage (%)"] / df["Actual Days"]

    # ----- 3) Build full date range for the entire sprint -----
    overall_start = df["Planned Start"].min()
    overall_end   = df["Planned End"].max()
    full_dates = pd.date_range(start=overall_start, end=overall_end, freq="D")

    expected_cum = []
    actual_cum   = []

    # ----- 4) Compute cumulative sums for each day -----
    for single_date in full_dates:
        exp_sum = 0.0
        act_sum = 0.0
        for _, row in df.iterrows():
            p_start, p_end = row["Planned Start"], row["Planned End"]
            a_start, a_end = row["Actual Start"], row["Actual End"]
            weight = row["Weightage (%)"]

            # --- Expected portion: linear interpolation across the planned window ---
            planned_days = (p_end - p_start).days + 1
            if single_date >= p_end:
                exp_sum += weight
            elif p_start <= single_date < p_end:
                days_into_planned = (single_date - p_start).days + 1
                exp_sum += weight * (days_into_planned / planned_days)

            # --- Actual portion: linear interpolation across the actual window ---
            actual_days = (a_end - a_start).days + 1
            if single_date >= a_end:
                act_sum += weight
            elif a_start <= single_date < a_end:
                days_into_actual = (single_date - a_start).days + 1
                act_sum += weight * (days_into_actual / actual_days)

        expected_cum.append(exp_sum)
        actual_cum.append(act_sum)

    # ----- 5a) Plot Expected vs. Actual Progress (Line + Markers) -----
    plt.figure(figsize=(10, 5))

    plt.plot(full_dates, expected_cum, color="blue", label="Expected Cumulative %")
    plt.plot(full_dates, actual_cum,   color="red",  label="Actual   Cumulative %")

    # Fill under the curves
    plt.fill_between(full_dates, expected_cum, color="blue", alpha=0.1)
    plt.fill_between(full_dates, actual_cum,   color="red",  alpha=0.1)

    # Add markers at each topic’s actual completion date
    for _, row in df.iterrows():
        a_end = row["Actual End"]
        if overall_start <= a_end <= overall_end:
            idx = (a_end - overall_start).days
            y_val = actual_cum[idx]
            plt.scatter(a_end, y_val, color="red", edgecolors="black", zorder=5, s=50)
            plt.text(
                a_end,
                y_val + 1.5,
                f"{row['Topic']} done",
                color="darkred",
                fontsize=8,
                rotation=90,
                va="bottom"
            )

    # Format x-axis: weekly ticks, vertical labels
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=90)

    plt.xlabel("Date")
    plt.ylabel("Cumulative Completion (%)")
    plt.title("Expected vs. Actual Learning Progress")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("expected_vs_actual_progress.png")
    plt.show()

    # ----- 5b) Plot Gantt‐Style Timeline (Planned vs. Actual) -----
    plt.figure(figsize=(10, 6))

    for idx, row in df.iterrows():
        topic = row["Topic"]
        p_start, p_end = row["Planned Start"], row["Planned End"]
        a_start, a_end = row["Actual Start"], row["Actual End"]
        y = idx

        # Planned bar in BLUE
        plt.barh(
            y,
            (p_end - p_start).days + 1,
            left=p_start,
            height=0.4,
            color="skyblue",
            edgecolor="navy",
            label="Planned" if idx == 0 else ""
        )
        # Actual bar in RED
        plt.barh(
            y - 0.15,
            (a_end - a_start).days + 1,
            left=a_start,
            height=0.3,
            color="salmon",
            edgecolor="darkred",
            label="Actual" if idx == 0 else ""
        )

    plt.yticks(range(len(df)), df["Topic"])
    ax2 = plt.gca()
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=90)
    plt.xlabel("Date")
    plt.title("Gantt‐Style Timeline: Planned (blue) vs. Actual (red)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("gantt_timeline.png")
    plt.show()

    # ----- 5c) Plot Bar Chart of Productivity (%/day) by Topic (colored by Level) -----
    plt.figure(figsize=(8, 5))

    # Map Level → Color
    level_to_color = {
        "easy":   "seagreen",
        "medium": "goldenrod",
        "hard":   "indianred"
    }
    bar_colors = [level_to_color.get(lvl.lower(), "gray") for lvl in df["Level"].astype(str)]

    plt.bar(df["Topic"], df["Productivity (%/day)"], color=bar_colors, edgecolor="black")
    plt.xlabel("Topic")
    plt.ylabel("Productivity (% per day)")
    plt.title("Productivity Rate by Topic (Colored by Level)")
    plt.xticks(rotation=45, ha="right")
    # Create a custom legend
    handles = [
        plt.Line2D([0], [0], color=level_to_color["easy"],   lw=10),
        plt.Line2D([0], [0], color=level_to_color["medium"], lw=10),
        plt.Line2D([0], [0], color=level_to_color["hard"],   lw=10)
    ]
    plt.legend(handles, ["easy", "medium", "hard"], title="Level")
    plt.tight_layout()
    plt.savefig("productivity_bar_chart.png")
    plt.show()

    # ----- 5d) Plot Calendar Heatmap of Daily “Actual %” Increments -----
    # Compute daily increment: difference of actual_cum between consecutive days
    actual_array = np.array(actual_cum)
    daily_increment = np.zeros_like(actual_array)
    daily_increment[0] = actual_array[0]  # first day’s completed %
    daily_increment[1:] = actual_array[1:] - actual_array[:-1]

    # Build a 2D array: rows = week index, cols = day of week (Mon=0,...Sun=6)
    start = overall_start
    num_weeks = int(np.ceil(len(full_dates) / 7))
    heatmap_data = np.zeros((num_weeks, 7))

    for i, single_date in enumerate(full_dates):
        week_idx = i // 7
        day_idx  = single_date.weekday()  # Monday=0, Sunday=6
        heatmap_data[week_idx, day_idx] = daily_increment[i]

    plt.figure(figsize=(10, num_weeks * 0.5 + 2))
    # Use a colormap that highlights higher values
    cmap = plt.get_cmap("YlOrRd")
    im = plt.imshow(
        heatmap_data,
        aspect="auto",
        cmap=cmap,
        origin="lower",
        interpolation="nearest"
    )

    plt.colorbar(im, label="Daily % Completed")
    plt.title("Calendar Heatmap: Daily Learning Progress Δ (%)")

    # Label y-axis with week numbers or starting date of each week
    week_labels = []
    for w in range(num_weeks):
        week_start = (start + pd.Timedelta(days=w * 7)).strftime("%Y-%m-%d")
        week_labels.append(week_start)
    plt.yticks(range(num_weeks), week_labels)

    # Label x-axis with weekdays
    plt.xticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

    plt.tight_layout()
    plt.savefig("calendar_heatmap.png")
    plt.show()

    # ----- 5e) Plot Radar/Spider Chart of Productivity by Topic -----
    # Each axis = one Topic, value = Productivity (%/day)
    categories = list(df["Topic"])
    N = len(categories)

    # Compute angles for each axis in the radar (in radians)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # close the loop

    # Values for each topic
    values = list(df["Productivity (%/day)"])
    values += values[:1]  # repeat first value at end to close the loop

    # Create polar subplot
    plt.figure(figsize=(8, 8))
    ax3 = plt.subplot(111, polar=True)
    ax3.set_theta_offset(pi / 2)
    ax3.set_theta_direction(-1)

    # Draw one line per topic set
    ax3.plot(angles, values, color="teal", linewidth=2, linestyle="solid")
    ax3.fill(angles, values, color="teal", alpha=0.25)

    # Add category labels
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories, fontsize=9)

    # Draw y‐labels (radial)
    max_prod = max(values)
    step = max_prod / 5.0
    y_ticks = np.arange(0, max_prod + step, step)
    ax3.set_rlabel_position(0)
    ax3.set_yticks(y_ticks[1:])       # skip 0
    ax3.set_yticklabels([f"{round(y, 1)}" for y in y_ticks[1:]], fontsize=8)
    ax3.set_ylim(0, max_prod)

    plt.title("Radar Chart: Productivity (%/day) by Topic", y=1.10)
    plt.tight_layout()
    plt.savefig("radar_spider_chart.png")
    plt.show()

    return df, full_dates, expected_cum, actual_cum


if __name__ == "__main__":
    df_metrics, dates, exp_line, act_line = analyze_from_csv("learning_progress.csv")
    print(df_metrics)
