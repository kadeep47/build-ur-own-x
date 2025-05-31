import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def parse_markdown_table(filepath):
    """
    Parse the first Markdown table found in the file and return a DataFrame.
    Expects the columns: 
        "Topic", "Weightage (%)", 
        "Planned Start", "Planned End", 
        "Actual Start", "Actual End"
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    table_lines = []
    is_table = False
    for line in lines:
        stripped = line.strip()
        # Identify table rows by the leading and trailing '|'
        if stripped.startswith("|") and stripped.endswith("|"):
            # Skip the separator row (|---|---|...|)
            if set(stripped.replace("|", "").replace("-", "").strip()) == set():
                continue
            table_lines.append(stripped)
            is_table = True
        elif is_table:
            # Stop once the table section ends (first non-table line after starting)
            break

    # Convert the Markdown rows into a list of lists
    rows = [row.strip("|").split("|") for row in table_lines]
    header = [h.strip() for h in rows[0]]            # first row = column names
    data = [[cell.strip() for cell in r] for r in rows[1:]]  # remaining rows = data

    df = pd.DataFrame(data, columns=header)
    return df

def analyze_and_plot(filepath="learning_progress.md"):
    """
    1. Parses the Markdown file.
    2. Converts columns to proper types.
    3. Calculates planned vs. actual durations.
    4. Computes productivity rate = Weightage (%) / Actual Days.
    5. Plots:
       - bar chart: Productivity Rate by Topic
       - bar chart: Cumulative Completion (%)
    6. Saves:
       - productivity_rate_by_topic.png
       - cumulative_completion.png
    """

    # 1) Parse the table
    df = parse_markdown_table(filepath)

    # 2) Convert types
    df["Weightage (%)"] = df["Weightage (%)"].astype(float)
    df["Planned Start"] = pd.to_datetime(df["Planned Start"], format="%Y-%m-%d")
    df["Planned End"]   = pd.to_datetime(df["Planned End"],   format="%Y-%m-%d")
    df["Actual Start"]  = pd.to_datetime(df["Actual Start"],  format="%Y-%m-%d", errors="coerce")
    df["Actual End"]    = pd.to_datetime(df["Actual End"],    format="%Y-%m-%d", errors="coerce")

    # 3) Calculate durations (adding +1 day to include both endpoints)
    df["Planned Days"] = (df["Planned End"] - df["Planned Start"]).dt.days + 1
    df["Actual Days"]  = (df["Actual End"] - df["Actual Start"]).dt.days + 1

    # 4) Compute productivity = weightage / actual days (as % per day)
    df["Productivity (%/day)"] = df["Weightage (%)"] / df["Actual Days"]

    # Determine which topics are completed (Actual End ≤ Today)
    today = datetime.now().date()
    df["Completed"] = df["Actual End"].dt.date <= today

    # Total weight of completed topics → cumulative completion %
    total_completed_weight = df.loc[df["Completed"], "Weightage (%)"].sum()
    completion_percent = total_completed_weight  # since weights sum to 100

    # 5) Plot Productivity Rate per Topic
    plt.figure(figsize=(10, 5))
    plt.bar(df["Topic"], df["Productivity (%/day)"])
    plt.xlabel("Topic")
    plt.ylabel("Productivity (% per day)")
    plt.title("Productivity Rate by Topic")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("productivity_rate_by_topic.png")
    plt.show()

    # Plot Cumulative Completion
    plt.figure(figsize=(6, 4))
    plt.bar(["Overall Completion"], [completion_percent])
    plt.ylim(0, 100)
    plt.ylabel("Completion (%)")
    plt.title("Cumulative Learning Completion")
    plt.tight_layout()
    plt.savefig("cumulative_completion.png")
    plt.show()

    return df