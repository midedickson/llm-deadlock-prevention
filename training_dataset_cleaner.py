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
    LOCKED_BY,
    EXPLANATION,
)


# Function to generate explanations based on the Deadlock column
def generate_explanation(row):
    if row[DEADLOCK] == "Yes":
        explanation = "Yes, this situation leads to a deadlock due to multiple processes locking resources without release, creating a circular wait condition."
    else:
        explanation = "No, this situation does not lead to a deadlock as the resource requests can be satisfied without causing a cyclical dependency among the processes."
    row.append(explanation)


def generate_locked_by(row):
    if row[LOCK_STATUS] == "Locked":
        row.append("Process X")
    else:
        row.append(None)


with open("process_simulation_data.csv") as simulation_csv_file:
    reader = csv.reader(simulation_csv_file)

    headers = next(reader)
    jsonl_content = ""
    for row in reader:
        generate_locked_by(row)
        generate_explanation(row)
        print(row)
        system_content = (
            f"System Log: Timestamp {row[TIMESTAMP]}, Process {row[PROCESS_ID]} has requested {row[RESOURCE_REQUEST]} for {row[MESSAGE_TYPE]} operation. "
            f"Current lock status on {row[RESOURCE_REQUEST]} is {row[LOCK_STATUS].lower()}, and it is locked by {row[LOCKED_BY]}. The transaction status is {row[TRANSACTION_STATUS].lower()}. "
            f"The system load is at {row[SYSTEM_LOAD]}, indicating {'high_activity' if float(row[SYSTEM_LOAD]) > 0.7 else 'moderate activity'}."
        )
        entry = {
            "messages": [
                {"role": "system", "content": system_content},
                {
                    "role": "user",
                    "content": "Is there a potential deadlock according to this log entry?",
                },
                {
                    "role": "assistant",
                    "content": row[EXPLANATION],
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
