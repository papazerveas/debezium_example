import pandas as pd
import json

pdf = pd.read_parquet("./data/local_mysql57_apifon_callbacks_test_client", engine="pyarrow")
# pdf.count()
# print(pdf.head(n=100 ))


pdf["json_str"] = pdf["json_str"].apply(json.loads)

# Step 2: Extract nested field
df["payload"] = df["parsed"].apply(lambda x: x.get("payload", {}).get("after", {}).get("payload"))

# (Optional) Step 3: Parse the payload string as a real dict if it's JSON
df["payload_json"] = df["payload"].apply(json.loads)

# Preview
print(df[["payload", "payload_json"]])
