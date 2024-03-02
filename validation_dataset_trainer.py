import csv
import json
from constants import (
    TIMESTAMP,
    PROCESS_ID,
    RESOURCE_REQUEST,
    MESSAGE_TYPE,
    LOCK_STATUS,
    TRANSACTION_STATUS,
    SYSTEM_LOAD,
    DEADLOCK,
)

with open("process_validation_data.csv") as validation_csv_file:
    reader = csv.reader(validation_csv_file)
    jsonl_content = ""
    for row in reader:
        system_content = (
            f"System Log: Timestamp {row[TIMESTAMP]}, Process {row[PROCESS_ID]} has requested {row[RESOURCE_REQUEST]} for {row[MESSAGE_TYPE]} operation. "
            f"Current lock status is {row[LOCK_STATUS].lower()} and transaction status is {row[TRANSACTION_STATUS].lower()}. "
            f"The system load is at {row[SYSTEM_LOAD]}, indicating {"high_activity" if row[SYSTEM_LOAD] > 0.7 else "moderate activity"}."
        )
        entry = {
            "messages": [
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": "Given the system log entry above, analyze the likelihood of a deadlock scenario and provide your assessment.",
                },
            ],
            "expected_result": row[DEADLOCK],
        }
        jsonl_content += json.dumps(entry) + "\n"
    validation_csv_file.close()

    # Save the JSONL content to a file
    jsonl_file_path = "processed_validation_data.jsonl"
    with open(jsonl_file_path, "w") as file:
        file.write(jsonl_content)
        file.close()
