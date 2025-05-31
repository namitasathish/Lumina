
import pandas as pd
import argparse
import os
import re
import sys
import string


def parse_args():
    parser = argparse.ArgumentParser(
        description="Clean and merge toxicity/cyberbullying datasets into a unified intent CSV."
    )
    parser.add_argument(
        "--input", "-i",
        default="datasets/master_dataset.csv",
        help="Path to the master CSV (combined datasets). Default: datasets/master_dataset.csv"
    )
    parser.add_argument(
        "--output", "-o",
        default="datasets/clean_master_dataset.csv",
        help="Path for the cleaned output CSV. Default: datasets/clean_master_dataset.csv"
    )
    return parser.parse_args()

def clean_text(text):
    """
    Clean comment_text by:
    - Lowercasing
    - Removing URLs, mentions, hashtags
    - Removing emojis and special characters
    - Stripping extra whitespace
    """
    if pd.isnull(text):
        return ""

    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www.\S+", "", text)

    # Remove @mentions and #hashtags
    text = re.sub(r"[@#]\w+", "", text)

    # Remove emojis and non-text characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Optional lemmatization
    # text = " ".join([lemmatizer.lemmatize(w) for w in text.split()])

    return text

def map_intent(row, tox_cols):
    """
    Decide the single intent label for a row:
      1. Use `cyberbullying_type` if present;
      2. Else, pick the first flagged toxicity column;
      3. Otherwise, label as 'not_cyberbullying'.
    """
    cbt = row.get('cyberbullying_type')
    if pd.notnull(cbt) and str(cbt).strip() != "":
        return cbt

    for col in tox_cols:
        if row.get(col, 0) == 1:
            return col

    return 'not_cyberbullying'

def main():
    args = parse_args()
    input_path = args.input
    output_path = args.output

    if not os.path.isfile(input_path):
        sys.exit(f"ERROR: Input file not found: {input_path}")

    df = pd.read_csv(input_path, low_memory=False)

    tox_cols = ['severe_toxic', 'toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    required_cols = {'id', 'comment_text', 'source'} | set(tox_cols) | {'cyberbullying_type'}
    missing = required_cols - set(df.columns)
    if missing:
        sys.exit(f"ERROR: Missing expected columns in input: {sorted(missing)}")

    # Clean comment_text
    df['comment_text'] = df['comment_text'].apply(clean_text)

    # Generate unified intent
    df['intent'] = df.apply(map_intent, axis=1, tox_cols=tox_cols)

    # Trim to output columns
    clean_df = df[['id', 'comment_text', 'intent', 'source']].copy()

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    clean_df.to_csv(output_path, index=False)
    print(f" Cleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    main()
