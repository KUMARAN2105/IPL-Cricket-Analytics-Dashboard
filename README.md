# IPL Cricket Analytics Dashboard

Power BI project for IPL cricket analytics, focused on building interactive dashboards and reports from match, player, and team data.

## Project Goals

- Create a Power BI dashboard for IPL performance analysis
- Support match, player, team, and venue analytics
- Provide data preparation scripts to clean and transform cricket datasets
- Keep the project organized for collaboration and future expansion

## Repository Structure

- `powerbi/` - Power BI artifacts, report files, and documentation
- `data/` - Raw and processed datasets for the dashboard
- `scripts/` - Data transformation and preparation scripts

## Getting Started

1. Place IPL datasets in `data/raw/` or `data/`.
2. Create a Python virtual environment and install dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Run the preprocessing script:

   ```powershell
   .\.venv\Scripts\python.exe scripts\prepare_data.py
   ```

   This will generate:
   - `data/processed/matches_clean.csv`
   - `data/processed/batting_summary_clean.csv`
   - `powerbi/batting_summary_clean.csv`

4. Generate the batting dashboard from `batting_summary.csv`:

   ```powershell
   .\.venv\Scripts\python.exe scripts\create_batting_dashboard.py
   ```

   The dashboard HTML file will be saved to `dashboard/batting_dashboard.html`.

5. Add your Power BI report file (`.pbix` or `.pbit`) to `powerbi/`.
6. Open Power BI Desktop and open the report from the `powerbi/` folder.

   Example PowerShell command once a report exists:

   ```powershell
   Start-Process "D:\KUMARAN\IPL-Cricket-Analytics-Dashboard\powerbi\ipl-cricket-analytics.pbix"
   ```

   Or use the helper script:

   ```powershell
   .\open_powerbi_report.ps1
   ```

## Notes

- `data/processed/matches_clean.csv` is the output from the preprocessing script.
- The repository currently does not include a Power BI report file.
- Add a `.pbix` file to `powerbi/` before opening Power BI.
- Keep large binary files under version control only if necessary.

