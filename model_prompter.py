from ai_factory import ModelFactory
import json
import time
import os

# get most recent fine tuned model
tuning_list = ModelFactory.get_instance().fine_tuning.jobs.list()
expected_running_job = tuning_list.data[0]


job_id = expected_running_job.id


print("Fine tuning job status is: ", expected_running_job.status)
if expected_running_job.status != "succeeded":
    # exit the script if fine tuning job is not yet succeeded
    os._exit(0)

fine_tuned_model = expected_running_job.fine_tuned_model


# read the lines of the validation jsonl file
with open("balanced_processed_validation_data.jsonl") as validation_jsonl_file:
    json_lines = validation_jsonl_file.readlines()
    for json_line in json_lines:
        payload = json.loads(json_line)
        # todo: decribe what data means
        completion = ModelFactory.get_instance().chat.completions.create(
            model=fine_tuned_model,
            messages=payload["messages"],
        )
        print(completion.choices[0].message)
        time.sleep(0.5)
