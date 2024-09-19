## Creating Crew AI crew for meeting prep
Follow the instructions below to run the crew ai meeting prep agent. The other files needed to run the code are in this directory.

### 1. Install LangTrace and other requirements in Terminal

```bash
pip install -r requirements.txt
pip installl langtrace_python_sdk
```
#### Export environment variables
```python
export LANGTRACE_API_KEY=<your-api-key>
export OPENAI_API_KEY=<your-openai-api-key>
```

Note: If you are self-hosting, set the LANGTRACE_API_HOST environment variable to the URL of your Langtrace instance.

```
export LANGTRACE_API_HOST=<your-langtrace-instance-url>
```

### 2. Handle Imports

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_key=<your_api_key>)
from crewai import Crew

from tasks import MeetingPreparationTasks
from agents import MeetingPreparationAgents
```
### 3. Setup Command Line Interface for user to interact with

```python
tasks = MeetingPreparationTasks()
agents = MeetingPreparationAgents()

print("## Welcome to the Meeting Prep Crew")
print('-------------------------------')
participants = input("What are the emails for the participants (other than you) in the meeting?\n")
context = input("What is the context of the meeting?\n")
objective = input("What is your objective for this meeting?\n")

```

### 4. Create Agents

```python
researcher_agent = agents.research_agent()
industry_analyst_agent = agents.industry_analysis_agent()
meeting_strategy_agent = agents.meeting_strategy_agent()
summary_and_briefing_agent = agents.summary_and_briefing_agent()
```
### 5. Create Tasks

```python
research = tasks.research_task(researcher_agent, participants, context)
industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, participants, context)
meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context, objective)
summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context, objective)

meeting_strategy.context = [research, industry_analysis]
summary_and_briefing.context = [research, industry_analysis, meeting_strategy]
```


### 6. Create Crew responsible for handling agents and tasks

```python 
crew = Crew(
	agents=[
		researcher_agent,
		industry_analyst_agent,
		meeting_strategy_agent,
		summary_and_briefing_agent
	],
	tasks=[
		research,
		industry_analysis,
		meeting_strategy,
		summary_and_briefing
	]
)
```

### 8. Launch Crew

```python
result = crew.kickoff()
```


### 9. Print results
```python
print("\n\n################################################")
print("## Here is the result")
print("################################################\n")
print(result)
```


