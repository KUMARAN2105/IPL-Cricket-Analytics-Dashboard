import pandas as pd
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_matches(file_path: pathlib.Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    # Example cleanup steps; adjust for your IPL dataset schema.
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def main() -> None:
    match_file = RAW_DIR / "matches.csv"
    if not match_file.exists():
        raise FileNotFoundError(f"Expected dataset not found: {match_file}")

    matches = load_matches(match_file)
    matches_clean = clean_matches(matches)
    output_file = PROCESSED_DIR / "matches_clean.csv"
    matches_clean.to_csv(output_file, index=False)
    print(f"Processed matches saved to {output_file}")


if __name__ == "__main__":
    main()
