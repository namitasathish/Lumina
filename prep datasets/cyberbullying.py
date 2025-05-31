import os
import pandas as pd
import uuid

# Base directory of this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to datasets
master_path = os.path.join(base_dir, "..", "datasets", "master_dataset.csv")
cyberbullying_path = os.path.join(base_dir, "..", "datasets", "cyberbullying_tweets.csv")
save_path = master_path  # overwrite master dataset

# Load existing master dataset
master_df = pd.read_csv(master_path)

# Load cyberbullying data
cyber_df = pd.read_csv(cyberbullying_path)

# Rename columns for consistency
cyber_df = cyber_df.rename(columns={
    "tweet_text": "comment_text",
    "cyberbullying_type": "cyberbullying_type"
})

# Add required label columns not in cyberbullying dataset, fill with 0
label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
for col in label_columns:
    cyber_df[col] = 0

# Add 'source' column
cyber_df["source"] = "cyberbullying"

# Add missing 'id' column with unique UUIDs
cyber_df["id"] = [uuid.uuid4().hex[:16] for _ in range(len(cyber_df))]

# Ensure 'cyberbullying_type' column exists in master dataset
if "cyberbullying_type" not in master_df.columns:
    master_df["cyberbullying_type"] = pd.NA

# Reorder columns to match
column_order = ["id", "comment_text"] + label_columns + ["source", "cyberbullying_type"]

master_df = master_df[column_order]
cyber_df = cyber_df[column_order]

# Combine datasets
final_df = pd.concat([master_df, cyber_df], ignore_index=True)

# Save combined dataset
final_df.to_csv(save_path, index=False)
print("Combined dataset saved to:", save_path)
