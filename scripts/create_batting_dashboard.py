import pathlib

import pandas as pd
import pathlib

import pandas as pd
import plotly.express as px
import plotly.io as pio

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "batting_summary.csv"
OUTPUT_DIR = BASE_DIR / "dashboard"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "batting_dashboard.html"
STYLES_FILE = OUTPUT_DIR / "styles.css"
LOGO_FILE = BASE_DIR / "powerbi" / "logo.png"


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

    # summary as a set of cards for the top of the dashboard
    summary = (
        "<div class=\"summary\">"
        + f"<div class=\"title\"><h1>{title}</h1></div>"
        + "<div class=\"cards\">"
        + f"<div class=\"card\"><div class=\"card-value\">{total_runs}</div><div class=\"card-label\">Total runs</div></div>"
        + f"<div class=\"card\"><div class=\"card-value\">{total_innings}</div><div class=\"card-label\">Innings</div></div>"
        + f"<div class=\"card\"><div class=\"card-value\">{average_runs:.2f}</div><div class=\"card-label\">Avg runs</div></div>"
        + f"<div class=\"card\"><div class=\"card-value\">{average_sr:.2f}</div><div class=\"card-label\">Avg SR</div></div>"
        + f"<div class=\"card\"><div class=\"card-value\">{total_fours}</div><div class=\"card-label\">Fours</div></div>"
        + f"<div class=\"card\"><div class=\"card-value\">{total_sixes}</div><div class=\"card-label\">Sixes</div></div>"
        + "</div></div>"
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

    # Additional charts for richer analysis
    runs_dist_fig = px.histogram(
        df,
        x="runs",
        nbins=20,
        title="Distribution of Runs per Innings",
        labels={"runs": "Runs", "count": "Count"},
    )

    strike_rate_scatter = px.scatter(
        df,
        x="balls",
        y="runs",
        color="SR",
        size="4s",
        hover_data=["batsmanName", "SR"],
        title="Balls Faced vs Runs Scored (colored by SR)",
        labels={"balls": "Balls Faced", "runs": "Runs", "SR": "Strike Rate"},
    )

    dismissal_by_pos = df[df["battingPos"] <= 11].copy()
    dismissal_pos_fig = px.bar(
        dismissal_by_pos,
        x="battingPos",
        color="Out_Not_Out",
        title="Dismissals by Batting Position",
        labels={"battingPos": "Position", "Out_Not_Out": "Status"},
    )

    high_scores = df[df["runs"] >= 30].copy().sort_values("runs", ascending=False).head(15)
    high_scores_fig = px.bar(
        high_scores,
        x="batsmanName",
        y="runs",
        color="SR",
        title="High Scores (30+ runs) - Top 15",
        labels={"batsmanName": "Batsman", "runs": "Runs", "SR": "Strike Rate"},
    )

    figs = [
        top_batsmen_fig,
        position_runs_fig,
        position_sr_fig,
        team_runs_fig,
        status_fig,
        runs_dist_fig,
        strike_rate_scatter,
        dismissal_pos_fig,
        high_scores_fig,
    ]

    # assemble charts into a grid
    chart_divs = []
    for index, fig in enumerate(figs):
        fig_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn" if index == 0 else False)
        chart_divs.append(f"<div class=\"chart\">{fig_html}</div>")

        charts_html = "\n".join(chart_divs)

        head = (
                "<head>"
                + "<meta charset=\"utf-8\">"
                + "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
                + f"<title>{title}</title>"
                + "<link rel=\"stylesheet\" href=\"styles.css\">"
                + "</head>"
        )

        # header with optional logo and action buttons
        logo_rel = "powerbi/logo.png" if LOGO_FILE.exists() else None
        logo_img = f"<img src='{logo_rel}' alt='logo' class='logo'/>" if logo_rel else ""
        header_html = (
                "<header class='header'>"
                + "<div class='header-left'>"
                + logo_img
                + f"<div class='header-title'><h2>{title}</h2></div>"
                + "</div>"
                + "<div class='header-right'>"
                + "<button id='printBtn' class='btn'>Print</button>"
                + "<button id='downloadBtn' class='btn'>Download Charts</button>"
                + "</div>"
                + "</header>"
        )

        # small JS to wire up print and download actions for Plotly charts
        script = '''
<script>
document.addEventListener('DOMContentLoaded', function(){
    const printBtn = document.getElementById('printBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    if(printBtn) printBtn.addEventListener('click', ()=> window.print());
    if(downloadBtn) downloadBtn.addEventListener('click', async ()=>{
        const plots = document.querySelectorAll('.plotly-graph-div');
        for(let i=0;i<plots.length;i++){
            const plot = plots[i];
            try{
                const url = await Plotly.toImage(plot, {format:'png', height:800, width:1200});
                const a = document.createElement('a');
                a.href = url;
                a.download = `chart-${i+1}.png`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            }catch(e){console.warn('Export failed', e)}
        }
    });
});
</script>
'''

        body = f"<body>{header_html}{summary}<div class=\"charts-grid\">{charts_html}</div>{script}</body>"
        page = f"<html>{head}{body}</html>"
        return page


def save_dashboard(html: str, path: pathlib.Path) -> None:
    path.write_text(html, encoding="utf-8")


def write_styles(path: pathlib.Path) -> None:
    css = """
:root{--bg:#0f1724;--card:#0b1220;--accent:#1f6feb;--muted:#9aa4b2;--card-radius:8px}
*{box-sizing:border-box}
body{font-family:Inter,Segoe UI,Arial,sans-serif;margin:0;background:var(--bg);color:#e6eef6}
.summary{padding:20px}
.title h1{margin:0 0 12px 0;font-size:20px}
.cards{display:flex;flex-wrap:wrap;gap:12px}
.card{background:var(--card);padding:14px;border-radius:var(--card-radius);min-width:120px;flex:1 1 120px}
.card-value{font-size:20px;font-weight:700;color:var(--accent)}
.card-label{font-size:12px;color:var(--muted);margin-top:6px}
.charts-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;padding:16px}
.chart{background:transparent;padding:8px;border-radius:6px}
@media (max-width:600px){.cards{flex-direction:column}}
/* header styles */
.header{display:flex;justify-content:space-between;align-items:center;padding:14px 20px;background:linear-gradient(90deg,rgba(255,255,255,0.02),transparent)}
.header-left{display:flex;align-items:center;gap:12px}
.logo{height:40px}
.header-title h2{margin:0;font-size:16px;color:#dceefc}
.header-right .btn{background:var(--accent);border:none;color:white;padding:8px 12px;border-radius:6px;margin-left:8px;cursor:pointer}
.header-right .btn:hover{opacity:0.9}
"""
    path.write_text(css, encoding="utf-8")


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Batting summary dataset not found: {DATA_FILE}")

    df = load_batting_data(DATA_FILE)
    html = build_dashboard(df)
    # write CSS file for styling and then save the HTML dashboard
    try:
        write_styles(STYLES_FILE)
    except Exception:
        pass
    save_dashboard(html, OUTPUT_FILE)
    print(f"Batting dashboard created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
