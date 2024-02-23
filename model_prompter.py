from ai_factory import ModelFactory
import json
import time


# get most recent fine tuned model
tuning_list = ModelFactory.get_instance().fine_tuning.jobs.list()
expected_running_job = tuning_list.data[0]


job_id = expected_running_job.id
print(expected_running_job.status)
while expected_running_job.status != "succeeded":
    print(expected_running_job.status)
    if expected_running_job.status == "failed":
        break
    if expected_running_job.status == "queued":
        break
    time.sleep(30)
    # Retrieve the state of a fine-tune
    expected_running_job = ModelFactory.get_instance().fine_tuning.jobs.retrieve(job_id)

fine_tuned_model = expected_running_job.fine_tuned_model


# read the lines of the validation jsonl file
with open("processed_validation_data.jsonl") as validation_jsonl_file:
    json_lines = validation_jsonl_file.readlines()
    for json_line in json_lines:
        payload = json.loads(json_line)
        completion = ModelFactory.get_instance().chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=payload["messages"],
        )
        print(completion.choices[0].message)
        time.sleep(1)
