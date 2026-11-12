"""stage03_transform_jugurtha.py - Module 4 Script.

(EDIT YOUR VERSION OF THIS FILE)

Source: validated JSON object
Sink: Polars DataFrame

Purpose

  Transform validated JSON data into a structured format.

Analytical Questions

- Which fields are needed from the JSON data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

Edit your Python file to:
- extract the fields needed for your analysis,
- normalize records into a consistent structure,
- create any derived fields required.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

import polars as pl

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    json_data: list[dict[str, Any]],
    LOG: logging.Logger,
) -> pl.DataFrame:
    """Transform JSON into a structured DataFrame.

    Args:
        json_data (list[dict[str, Any]]): Validated JSON data.
        LOG (logging.Logger): The logger instance.

    Returns:
        pl.DataFrame: The transformed dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    records: list[dict[str, Any]] = []

    for record in json_data:
        records.append(
            {
                "post_id": record["postId"],
                "comment_id": record["id"],
                "name": record["name"],
                "email": record["email"],
                "body": record["body"],
            }
        )

    df: pl.DataFrame = pl.DataFrame(records)

    # Derived fields
    df = df.with_columns(
        [
            pl.col("name").str.len_chars().alias("name_length"),
            pl.col("body").str.len_chars().alias("body_length"),
            pl.col("body")
            .str.to_lowercase()
            .str.extract_all(r"\b\w+\b")
            .list.len()
            .alias("body_word_count"),
        ]
    )

    LOG.info("Transformation complete.")
    LOG.info(f"DataFrame preview:\n{df.head()}")
    LOG.info("Sink: Polars DataFrame created")

    # Return the transformed DataFrame for use in the next stage.
    return df
