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
        entry = {
            "messages": [
                {
                    "role": "system",
                    "content": f"The system log entry is as follows: Timestamp: {row[TIMESTAMP]}, "
                    f"ProcessID: {row[PROCESS_ID]}, ResourceRequest: {row[RESOURCE_REQUEST]}, "
                    f"MessageType: {row[MESSAGE_TYPE]}, LockStatus: {row[LOCK_STATUS]}, "
                    f"TransactionStatus: {row[TRANSACTION_STATUS]}, SystemLoad: {row[SYSTEM_LOAD]}",
                },
                {
                    "role": "user",
                    "content": "Is there a potential deadlock according to this log entry?",
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
