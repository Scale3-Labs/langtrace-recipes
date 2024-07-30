from inspect_ai import Task, task
from inspect_ai.dataset import csv_dataset
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import chain_of_thought, self_critique

@task
def example_eval():
    return Task(
        dataset=csv_dataset("langtracefs://clz8kxoop0001rfhkkkl6mv10"),
        plan=[
            chain_of_thought(),
            self_critique()
        ],
        scorer=model_graded_qa()
    )
