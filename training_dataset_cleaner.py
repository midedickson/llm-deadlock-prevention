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


# Function to generate explanations based on the Deadlock column
def generate_explanation(row):
    if row[DEADLOCK] == "Yes":
        explanation = "Yes, this situation leads to a deadlock due to multiple processes locking resources without release, creating a circular wait condition."
    else:
        explanation = "No, this situation does not lead to a deadlock as the resource requests can be satisfied without causing a cyclical dependency among the processes."
    return explanation


with open("process_simulation_data.csv") as simulation_csv_file:
    reader = csv.reader(simulation_csv_file)
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
                {
                    "role": "assistant",
                    "content": generate_explanation(row),
                },
            ]
        }
        jsonl_content += json.dumps(entry) + "\n"
    simulation_csv_file.close()

    # Save the JSONL content to a file
    jsonl_file_path = "processed_simulation_data.jsonl"
    with open(jsonl_file_path, "w") as file:
        file.write(jsonl_content)
        file.close()
