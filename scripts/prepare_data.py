import pathlib

import pandas as pd

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
POWERBI_DIR = BASE_DIR / "powerbi"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
POWERBI_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(file_path: pathlib.Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def clean_batting_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip().replace("/", "_").replace(" ", "_") for col in df.columns]

    numeric_columns = ["runs", "balls", "4s", "6s", "SR", "battingPos"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "Out_Not_Out" not in df.columns and "Out/Not_Out" in df.columns:
        df = df.rename(columns={"Out/Not_Out": "Out_Not_Out"})

    df["teamInnings"] = df["teamInnings"].astype(str)
    df["batsmanName"] = df["batsmanName"].astype(str)
    df["matchID"] = df["matchID"].astype(str)
    return df


def save_dataframe(df: pd.DataFrame, file_path: pathlib.Path) -> None:
    df.to_csv(file_path, index=False)
    print(f"Saved data: {file_path}")


def main() -> None:
    match_file = RAW_DIR / "matches.csv"
    if match_file.exists():
        matches = load_csv(match_file)
        matches_clean = clean_matches(matches)
        save_dataframe(matches_clean, PROCESSED_DIR / "matches_clean.csv")
    else:
        print(f"Warning: match dataset not found: {match_file}")

    batting_file = BASE_DIR / "batting_summary.csv"
    if batting_file.exists():
        batting = load_csv(batting_file)
        batting_clean = clean_batting_summary(batting)
        save_dataframe(batting_clean, PROCESSED_DIR / "batting_summary_clean.csv")
        save_dataframe(batting_clean, POWERBI_DIR / "batting_summary_clean.csv")
    else:
        print(f"Warning: batting summary dataset not found: {batting_file}")


if __name__ == "__main__":
    main()
