# Backend Skills Sprint Tracker

Track each backend topic, its weightage in your learning plan, the planned timeline, and your actual timeline. Once you fill in your actual dates, a Python script can compute your daily productivity rate and cumulative completion.

> **Instructions**:
> 1. For each row below:
>    - **Weightage (%)**: What percentage this topic contributes to your total learning curve (total must be 100%).
>    - **Planned Start** / **Planned End**: The dates you originally scheduled for this topic (`YYYY-MM-DD`).
>    - **Actual Start** / **Actual End**: Fill these in once you begin and finish the topic (`YYYY-MM-DD`).
> 2. After filling in “Actual Start” and “Actual End” for each topic, run the Python script (`analyze_and_plot("learning_progress.md")`) to see your productivity charts.

| Topic       | Weightage (%) | Planned Start | Planned End   | Actual Start | Actual End   |
|-------------|---------------|---------------|---------------|--------------|--------------|
| Git & Shell | 10            | 2025-07-01    | 2025-07-10    |              |              |
| HTTP Server | 10            | 2025-07-11    | 2025-07-20    |              |              |
| Webapp      | 15            | 2025-07-21    | 2025-08-05    |              |              |
| Redis       | 20            | 2025-08-06    | 2025-08-16    |              |              |
| Kafka       | 20            | 2025-08-17    | 2025-08-27    |              |              |
| Docker      | 10            | 2025-08-28    | 2025-09-06    |              |              |
| Microservices | 15          | 2025-09-07    | 2025-09-21    |              |              |

> **Notes**:
> - Adjust the “Weightage (%)” column so that the sum of all rows = 100.  
> - You can add or remove rows (topics) as you see fit, but keep the same columns.  
> - Once you fill in “Actual Start” / “Actual End,” run the Python script below to generate two charts:
>    1. **`productivity_rate_by_topic.png`** (bar chart of % per day)  
>    2. **`cumulative_completion.png`** (bar chart showing total % complete so far)

---