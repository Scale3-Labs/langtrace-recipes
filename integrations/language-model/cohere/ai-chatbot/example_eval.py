from inspect_ai import Task, task
from inspect_ai.dataset import csv_dataset
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import chain_of_thought, self_critique

@task
def example_eval():
    return Task(
        dataset=csv_dataset("langtracefs://<your_dataset_id>"),
        #ENSURE TO REPLACE THE 'your_dataset_id' placeholder with your actual dataset id which can be retrieved from your langtrace dashboard.
        #If you are unsure of how to retrieve this id please refer to step2 of the evaluations tutorial - https://github.com/Scale3-Labs/langtrace-recipes/blob/main/langtrace-features/evaluations/evaluations.md

        plan=[
            chain_of_thought(),
            self_critique()
        ],
        scorer=model_graded_qa()
    )
