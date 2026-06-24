import pathlib

import pandas as pd
import plotly.express as px
import plotly.io as pio

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "batting_summary.csv"
OUTPUT_DIR = BASE_DIR / "dashboard"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "batting_dashboard.html"


def load_batting_data(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.copy()
    df.columns = [col.strip().replace("/", "_").replace(" ", "_") for col in df.columns]
    df["runs"] = pd.to_numeric(df["runs"], errors="coerce")
    df["balls"] = pd.to_numeric(df["balls"], errors="coerce")
    df["4s"] = pd.to_numeric(df["4s"], errors="coerce")
    df["6s"] = pd.to_numeric(df["6s"], errors="coerce")
    df["SR"] = pd.to_numeric(df["SR"], errors="coerce")
    df["battingPos"] = pd.to_numeric(df["battingPos"], errors="coerce")
    return df


def build_dashboard(df: pd.DataFrame) -> str:
    title = "IPL Batting Summary Dashboard"

    total_innings = len(df)
    total_runs = int(df["runs"].sum())
    average_runs = df["runs"].mean()
    average_sr = df["SR"].mean()
    total_fours = int(df["4s"].sum())
    total_sixes = int(df["6s"].sum())
    not_out_count = int((df["Out_Not_Out"] == "Not_Out").sum())
    out_count = int((df["Out_Not_Out"] == "Out").sum())

    summary = (
        f"<h1>{title}</h1>"
        f"<p><strong>Total innings:</strong> {total_innings}</p>"
        f"<p><strong>Total runs scored:</strong> {total_runs}</p>"
        f"<p><strong>Average runs per innings:</strong> {average_runs:.2f}</p>"
        f"<p><strong>Average strike rate:</strong> {average_sr:.2f}</p>"
        f"<p><strong>Total fours:</strong> {total_fours}</p>"
        f"<p><strong>Total sixes:</strong> {total_sixes}</p>"
        f"<p><strong>Outs:</strong> {out_count}, <strong>Not outs:</strong> {not_out_count}</p>"
    )

    top_batsmen = (
        df.groupby("batsmanName")
        .agg(total_runs=("runs", "sum"), innings=("runs", "count"), average_sr=("SR", "mean"))
        .sort_values("total_runs", ascending=False)
        .reset_index()
        .head(10)
    )

    top_batsmen_fig = px.bar(
        top_batsmen,
        x="batsmanName",
        y="total_runs",
        title="Top 10 Batsmen by Total Runs",
        labels={"batsmanName": "Batsman", "total_runs": "Total Runs"},
    )

    position_summary = (
        df.groupby("battingPos")
        .agg(
            avg_runs=("runs", "mean"),
            avg_sr=("SR", "mean"),
            innings=("runs", "count"),
        )
        .reset_index()
        .sort_values("battingPos")
    )

    position_runs_fig = px.line(
        position_summary,
        x="battingPos",
        y="avg_runs",
        title="Average Runs by Batting Position",
        labels={"battingPos": "Batting Position", "avg_runs": "Average Runs"},
        markers=True,
    )

    position_sr_fig = px.line(
        position_summary,
        x="battingPos",
        y="avg_sr",
        title="Average Strike Rate by Batting Position",
        labels={"battingPos": "Batting Position", "avg_sr": "Average Strike Rate"},
        markers=True,
    )

    team_runs = (
        df.groupby("teamInnings")
        .agg(total_runs=("runs", "sum"), innings=("runs", "count"))
        .reset_index()
        .sort_values("total_runs", ascending=False)
    )

    team_runs_fig = px.bar(
        team_runs,
        x="teamInnings",
        y="total_runs",
        title="Total Runs by Team",
        labels={"teamInnings": "Team", "total_runs": "Total Runs"},
    )

    status_fig = px.pie(
        df,
        names="Out_Not_Out",
        title="Dismissal Status Distribution",
    )

    figs = [top_batsmen_fig, position_runs_fig, position_sr_fig, team_runs_fig, status_fig]

    html_parts = []
    for index, fig in enumerate(figs):
        html_parts.append(
            pio.to_html(
                fig,
                full_html=False,
                include_plotlyjs="cdn" if index == 0 else False,
            )
        )

    page = f"<html><head><title>{title}</title></head><body>{summary}{''.join(html_parts)}</body></html>"
    return page


def save_dashboard(html: str, path: pathlib.Path) -> None:
    path.write_text(html, encoding="utf-8")


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Batting summary dataset not found: {DATA_FILE}")

    df = load_batting_data(DATA_FILE)
    html = build_dashboard(df)
    save_dashboard(html, OUTPUT_FILE)
    print(f"Batting dashboard created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
