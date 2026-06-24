# Power BI Artifacts

This folder is intended for Power BI report files and assets.

## Current status

No Power BI report file is included in this repository yet.

## Suggested workflow

1. Add your Power BI Desktop report file (`.pbix`) or template (`.pbit`) here.
2. Use `data/` as the source for your dataset files.
3. Keep report documentation and notes in this folder if needed.

## Example files

- `ipl-cricket-analytics.pbix` - main Power BI report
- `ipl-cricket-analytics.pbit` - template file

## Opening Power BI

Once a report file is added, you can open it directly from PowerShell:

```powershell
Start-Process "D:\KUMARAN\IPL-Cricket-Analytics-Dashboard\powerbi\ipl-cricket-analytics.pbix"
```

Or from the repository root, run:

```powershell
.\open_powerbi_report.ps1
```

## Power BI data for batting summary

The repository now exports a Power BI-ready batting dataset to:

- `powerbi/batting_summary_clean.csv`

To use it in Power BI Desktop:

1. Open Power BI Desktop.
2. Choose `Get data` → `Text/CSV`.
3. Select `powerbi/batting_summary_clean.csv`.
4. Load the table and create visuals such as:
   - Bar chart of total runs by batsman
   - Line chart of average strike rate by batting position
   - Pie chart for dismissal status distribution
   - Table of highest scoring innings
