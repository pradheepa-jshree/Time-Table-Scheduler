def validate_csv_schema(df, required_cols: list, file_label: str) -> None:
    """
    Validate that all required columns exist in the dataframe.
    Raises ValueError if any required column is missing.
    """
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"{file_label}: Missing required columns: {', '.join(missing_cols)}"
        )


def validate_no_duplicates(df, id_col: str, file_label: str) -> None:
    """
    Validate that there are no duplicate IDs.
    Raises ValueError listing all duplicate IDs found.
    """
    duplicates = df[df.duplicated(subset=[id_col], keep=False)][id_col].unique().tolist()
    if duplicates:
        raise ValueError(
            f"{file_label}: Duplicate IDs found: {', '.join(map(str, duplicates))}"
        )
