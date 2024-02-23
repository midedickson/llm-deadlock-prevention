from ai_factory import ModelFactory
import os
import time

training_file = ModelFactory.get_instance().files.create(
    file=open("processed_simulation_data.jsonl", "rb"), purpose="fine-tune"
)

file_data = training_file.model_dump()
file_name = file_data.get("id")


fine_tune_job = ModelFactory.get_instance().fine_tuning.jobs.create(
    training_file=file_name, model="gpt-3.5-turbo"
)

tuning_list = ModelFactory.get_instance().fine_tuning.jobs.list()

if len(tuning_list.data) == 0:
    print("No running jobs found")
    os._exit()


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
