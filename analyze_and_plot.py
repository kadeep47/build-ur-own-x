# analyze_and_plot.py (UPDATED)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def analyze_from_csv(filepath="learning_progress.csv"):
    """
    1. Read CSV with columns:
         Topic, Weightage (%), Planned Start, Planned End,
         Actual Start, Actual End, Level
    2. Compute each topic’s “Actual Days” and “Productivity (%/day)”.
    3. Build a date range from earliest Planned Start → latest Planned End.
    4. For each date in that range, compute:
         - expected cumulative % (linear interpolation)
         - actual   cumulative % (linear interpolation)
    5. Plot:
         • expected_vs_actual_progress.png  → two lines + markers at actual completions
         • gantt_timeline.png               → Gantt bars (planned in blue, actual in red)
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

    # ----- 3) Build full date range for plotting cumulative progress -----
    overall_start = df["Planned Start"].min()
    overall_end   = df["Planned End"].max()
    full_dates = pd.date_range(start=overall_start, end=overall_end, freq="D")

    expected_cum = []
    actual_cum   = []

    # ----- 4) Compute cumulative sums day by day -----
    for single_date in full_dates:
        exp_sum = 0.0
        act_sum = 0.0
        for _, row in df.iterrows():
            p_start, p_end    = row["Planned Start"], row["Planned End"]
            a_start, a_end    = row["Actual Start"], row["Actual End"]
            weight            = row["Weightage (%)"]

            # --- Expected portion ---
            planned_days = (p_end - p_start).days + 1
            if single_date >= p_end:
                exp_sum += weight
            elif p_start <= single_date < p_end:
                days_into_planned = (single_date - p_start).days + 1
                exp_sum += weight * (days_into_planned / planned_days)

            # --- Actual portion ---
            actual_days = (a_end - a_start).days + 1
            if single_date >= a_end:
                act_sum += weight
            elif a_start <= single_date < a_end:
                days_into_actual = (single_date - a_start).days + 1
                act_sum += weight * (days_into_actual / actual_days)

        expected_cum.append(exp_sum)
        actual_cum.append(act_sum)

    # ----- 5) Plot Expected vs. Actual Cumulative Progress -----
    plt.figure(figsize=(10, 5))

    # Plot the two lines
    plt.plot(full_dates, expected_cum, color="blue", label="Expected Cumulative %")
    plt.plot(full_dates, actual_cum,   color="red",  label="Actual   Cumulative %")

    # Fill under curves (semi-transparent)
    plt.fill_between(full_dates, expected_cum, color="blue", alpha=0.1)
    plt.fill_between(full_dates, actual_cum,   color="red",  alpha=0.1)

    # Add markers at each topic’s actual completion date
    for _, row in df.iterrows():
        a_end = row["Actual End"]
        weight = row["Weightage (%)"]
        # Find the index of a_end in full_dates
        if a_end < full_dates[0] or a_end > full_dates[-1]:
            continue
        idx = (a_end - full_dates[0]).days  # integer index
        y_val = actual_cum[idx]
        plt.scatter(a_end, y_val, color="red", edgecolors="k", zorder=5)
        plt.text(a_end, y_val + 1.5, f"{row['Topic']} done", 
                 color="darkred", fontsize=8, rotation=90, va="bottom")

    # Format x-axis: weekly ticks, vertical labels
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))  # every Monday
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=90)

    plt.xlabel("Date")
    plt.ylabel("Cumulative Completion (%)")
    plt.title("Expected vs. Actual Learning Progress")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("expected_vs_actual_progress.png")
    plt.show()

    # ----- 6) Plot Gantt-Style Timeline (Planned vs. Actual) -----
    plt.figure(figsize=(10, 6))

    for idx, row in df.iterrows():
        topic    = row["Topic"]
        p_start, p_end = row["Planned Start"], row["Planned End"]
        a_start, a_end = row["Actual Start"], row["Actual End"]
        y = idx  # place each topic on its own horizontal line

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
    plt.title("Gantt-Style Timeline: Planned vs. Actual")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("gantt_timeline.png")
    plt.show()

    return df, full_dates, expected_cum, actual_cum


if __name__ == "__main__":
    df_metrics, dates, exp_line, act_line = analyze_from_csv("learning_progress.csv")
    print(df_metrics)
