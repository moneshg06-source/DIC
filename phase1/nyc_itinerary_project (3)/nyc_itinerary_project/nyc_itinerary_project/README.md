# When to Go, Not Just Where: Time-Aware Itinerary Planning for NYC (Phase 1)

## Setup in VS Code (about 10 minutes, plus download time)

1. Unzip this folder and open it in VS Code: **File → Open Folder… → `nyc_itinerary_project`**.
2. Install the VS Code extensions **Python** and **Jupyter** (by Microsoft) if you don't have them.
3. Open a terminal (**Terminal → New Terminal**) and run:

   ```bash
   python -m venv .venv
   # Windows:      .venv\Scripts\activate
   # Mac / Linux:  source .venv/bin/activate
   pip install -r requirements.txt
   python src/download_data.py
   ```

   The download script fetches all three datasets into `data/raw/`. The Google file is the biggest,
   so give it a few minutes. If any download fails, the script prints the manual link.
4. Open `src/nyc_itinerary_phase1.ipynb`, click **Select Kernel** (top right) and choose the `.venv` interpreter.
5. Click **Run All**. Figures are saved to `figures/` and the cleaned data to `data/processed/`.

## Folder layout

```
nyc_itinerary_project/
├── src/
│   ├── nyc_itinerary_phase1.ipynb   <- 10 preprocessing steps + 10 EDA steps
│   └── download_data.py             <- downloads the 3 raw datasets
├── data/
│   ├── raw/                         <- filled by download_data.py
│   └── processed/                   <- created by the notebook
├── figures/                         <- created by the notebook (PNGs for report.pdf)
├── requirements.txt
└── .vscode/settings.json            <- makes notebook paths resolve correctly
```

## What the notebook contains

- **Part 1, Preprocessing Steps 1-10:** keep/rename columns and fix types, remove duplicates,
  convert to NYC local time, handle missing values, remove rows outside NYC or closed places,
  clean text labels, group categories into 7 travel themes, convert price text to numbers,
  remove users/places with too few check-ins, create time features (hour, weekday, season, sunset period).
- **Part 2, EDA 1-10:** summary statistics, popularity distribution, busiest hour per theme,
  day × hour heatmap, sunset effect, map of check-ins, Brooklyn Bridge crowd by hour,
  weather vs crowd, Google ratings, correlation matrix.

## Data sources and citations (cite these in the report)

| Dataset | Link |
|---|---|
| Foursquare NYC check-ins | https://sites.google.com/site/yangdingqi/home/foursquare-dataset (also on Kaggle: https://www.kaggle.com/chetanism/foursquare-nyc-and-tokyo-checkin-dataset) |
| Google Local metadata, New York | https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/ (file `meta-New_York.json.gz`) |
| Brooklyn Bridge pedestrian counts | https://data.cityofnewyork.us/Transportation/Brooklyn-Bridge-Automated-Pedestrian-Counts-Demons/6fi9-q3ta |

- D. Yang, D. Zhang, V. W. Zheng, Z. Yu. "Modeling User Activity Preference by Leveraging User Spatial Temporal Characteristics in LBSNs." *IEEE Trans. SMC: Systems*, 45(1), 129–142, 2015.
- J. Li, J. Shang, J. McAuley. "UCTopic: Unsupervised Contrastive Learning for Phrase Representations and Topic Mining." ACL 2022.
- A. Yan, Z. He, J. Li, T. Zhang, J. McAuley. "Personalized Showcases: Generating Multi-Modal Explanations for Recommendations." SIGIR 2023.
- NYC DOT. *Brooklyn Bridge Automated Pedestrian Counts Demonstration Project.* NYC Open Data.

## Troubleshooting

- **`FileNotFoundError` in the setup cell:** a dataset is missing from `data/raw/`. Re-run `python src/download_data.py`.
- **Foursquare download blocked by Google Drive:** download it manually from the Kaggle link and drop the CSV into `data/raw/`.
- **Useful categories dropped:** Step 7 prints the most common dropped labels. Add a keyword to `THEMES`.

## For the submission zip

The Brightspace zip needs `report.pdf` + `src/`. Don't include `data/` (it's large); the README
links and `download_data.py` let graders reproduce everything.
