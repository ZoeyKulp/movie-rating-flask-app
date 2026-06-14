import pandas as pd
import numpy as np
import ast
import re

BAD_VALUES = ["\\N", "N/A", "NA", "NULL", "###", "@@@", "[citation needed]", "Not Found", ""]
TOP_GENRES = ["Drama", "Comedy", "Action", "Thriller", "Romance", "Horror", "Documentary", "Crime", "Adventure", "Animation"]

def prepare_data(df):
    df = df.copy()

    # שלב 1: ניקוי bad values
    for col in df.columns:
        df[col] = df[col].replace(BAD_VALUES, np.nan)

    # שלב 2: המרות נומריות
    df["startYear"] = pd.to_numeric(df["startYear"], errors="coerce")
    df.loc[df["startYear"] == 0,   "startYear"] = np.nan
    df.loc[df["startYear"] < 1888, "startYear"] = np.nan
    df.loc[df["startYear"] > 2026, "startYear"] = np.nan
    df["runtimeMinutes"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce")

    # שלב 3: פרסור ז'אנרים
    def parse_genres(x):
        if pd.isna(x):
            return []
        x_str = str(x).strip()
        if x_str in ["", "[]", "nan"]:
            return []
        try:
            result = ast.literal_eval(x_str)
            if isinstance(result, list):
                return [str(g).strip() for g in result if str(g).strip()]
        except:
            pass
        x_str = (
            x_str
            .replace("[", "").replace("]", "")
            .replace("'", "").replace('"', "")
        )
        return [g.strip() for g in x_str.split(",") if g.strip()]

    df["genres_list"] = df["genres"].apply(parse_genres)

    # שלב 4: פיצ'רים בינאריים לפי ז'אנר
    for genre in TOP_GENRES:
        col_name = f'is_{genre.lower().replace("-", "_")}'
        df[col_name] = df["genres_list"].apply(
            lambda x, g=genre: 1 if g in x else 0
        )

    # שלב 5: num_genres ו-runtime_per_genre
    df["num_genres"] = df["genres_list"].apply(len)
    df["runtime_per_genre"] = df.apply(
        lambda row: row["runtimeMinutes"] / row["num_genres"]
        if row["num_genres"] > 0 and pd.notna(row["runtimeMinutes"])
        else np.nan,
        axis=1
    )

    # שלב 6: is_english
    def get_is_english(x):
        if pd.isna(x):
            return np.nan
        x_str = str(x).strip()
        if not x_str or x_str.lower() == "nan":
            return np.nan
        return 1 if "english" in x_str.lower() else 0

    df["is_english"] = df["Language"].apply(get_is_english)

    # שלב 7: is_us
    def get_is_usa(x):
        if pd.isna(x):
            return np.nan
        x_str = str(x).strip()
        if not x_str or x_str.lower() == "nan":
            return np.nan
        x_str = x_str.replace("<br/>", " ").replace("<br", " ")
        x_str = x_str.replace("'", "").replace('"', "").replace("[", "").replace("]", "")
        x_str = re.sub(r'\b\d+\b', ' ', x_str)
        x_lower = " ".join(x_str.split()).lower()
        usa_terms = ["united states", "united states of america", "usa", "u.s.", "u.s.a"]
        return 1 if any(term in x_lower for term in usa_terms) else 0

    df["is_us"] = df["Country"].apply(get_is_usa)

    # שלב 8: בחירת עמודות סופיות
    selected_cols = [
        "startYear", "runtimeMinutes", "num_genres", "runtime_per_genre",
        "is_drama", "is_comedy", "is_action", "is_thriller", "is_romance",
        "is_horror", "is_documentary", "is_crime", "is_adventure", "is_animation",
        "is_english", "is_us",
    ]

    # safety
    for col in selected_cols:
        if col not in df.columns:
            df[col] = np.nan

    # Leakage guard
    LEAKAGE_COLS = ['averageRating', 'numVotes', 'BoxOffice']
    leakage_found = [col for col in LEAKAGE_COLS if col in selected_cols]
    assert len(leakage_found) == 0, f"Leakage columns detected: {leakage_found}"

    return df[selected_cols]
