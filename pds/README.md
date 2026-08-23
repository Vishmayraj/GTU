# Python for Data Science (PDS)

Practicals for the PDS course, GTU. All ten practicals build a single pipeline
on the same dataset: a synthetic Apache/Nginx `access.log` is loaded, parsed,
cleaned, labeled, feature-engineered, balanced, aggregated, visualized, and
finally used to train a classifier that detects attacks (SQL injection, path
traversal, brute-force login attempts) in web server traffic.

## Structure

```
pds/
├── generator_log.py       # generates the synthetic access.log used by every practical
├── logs/
│   └── access.log          # generated log file (gitignored, not committed)
├── visuals/                 # saved plots from Practical 8
├── Practical_1.ipynb   ...  Practical_8.ipynb
```

Practicals 9 and 10 (classifier and reusable pipeline) are still in progress.

## Setup

Clone the repo and `cd` into this subject folder -- the venv and
`requirements.txt` for PDS live here, not at the repo root, since other
subjects don't need pandas/scikit-learn/etc.:

```bash
git clone https://github.com/Vishmayraj/GTU
cd GTU/pds
```

Create and activate a virtual environment:

```bash
python -m venv venv

# activate it
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

When you're done, `deactivate` exits the virtual environment.

Then generate the log file the practicals read from (it's gitignored, so
you need to create it locally):

```bash
python generator_log.py
```

This writes `pds/logs/access.log` with ~40,000 benign requests plus SQLi,
path traversal, brute-force, and bot/scanner traffic mixed in, so every
downstream practical has real signal to work with. It's deterministic
(seeded), so re-running it regenerates the same data.

Once the log file exists, open the notebooks in order -- each one reads the
output of the previous stage.

## Practicals

| # | Title | What it does |
|---|---|---|
| 1 | Load and Explore the Unstructured Access Log Data | Reads raw `access.log`, inspects random lines, identifies the fields in Combined Log Format |
| 2 | Convert Unstructured Log Data into a Structured Dataset | Regex-parses each line into IP, timestamp, method, path, status, size, referrer, user-agent; loads into a DataFrame |
| 3 | Clean the Data and Preprocess | Parses timestamps, handles missing/inconsistent entries, normalizes URL paths, lowercases and trims strings |
| 4 | Label Requests as Benign or Attack | Flags SQLi (`OR 1=1`, `UNION SELECT`, etc.), path traversal (`../`), and brute-force login patterns; adds a `label` column |
| 5 | Feature Engineering for Anomaly Detection | Requests per IP, time between requests, status code frequency, user-agent parsing, URL entropy |
| 6 | Balance the Dataset | Analyzes the benign/attack imbalance, applies SMOTE and random over/undersampling |
| 7 | Data Wrangling for Aggregated Analysis | Groups by IP, resamples traffic hourly/daily, builds pivot tables, filters bots and internal IPs |
| 8 | Data Visualization and EDA | Requests/hour, top attacking IPs, attack categories over time, status code distributions, IP-vs-request-type heatmap (plots saved to `visuals/`) |
| 9 | Build a Classifier *(in progress)* | Logistic Regression / Random Forest on the engineered features, evaluated with accuracy and confusion matrix |
| 10 | Reusable Data Pipeline *(in progress)* | Wraps loading, parsing, labeling, preprocessing, and feature engineering into one automated pipeline |

## Notes

- `logs/access.log` is not committed -- it's regenerated locally via
  `generator_log.py` so the repo stays small and every run starts from a
  known, reproducible dataset.
- Notebooks assume they're run from the `pds/` directory (paths like
  `logs/access.log` are relative to it).