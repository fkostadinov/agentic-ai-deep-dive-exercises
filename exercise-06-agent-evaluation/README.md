# Exercise 06 - Agent Evaluation

## Objective

Build and run a simple evaluation workflow for an Azure AI agent.

In this exercise, you will:

* create an agent version programmatically,
* define evaluation criteria,
* run an eval job against a small dataset,
* poll for completion,
* inspect the resulting output items.

This exercise shifts the focus from building agents to **measuring agent behavior**.

---

## Learning Goals

By completing this exercise, you will learn:

* why agent evaluation matters beyond manual spot-checking
* how to create an Azure AI agent from code
* how to define structured eval input data
* how to configure multiple evaluators for the same run
* how to run and monitor an evaluation job
* how to inspect eval outputs after completion

---

## Scenario

You have a simple assistant agent that answers general questions.

Instead of testing it manually one prompt at a time, you want to evaluate it in a more systematic way.

The script in this exercise:

1. creates a version of an Azure AI agent,
2. defines an eval with several criteria,
3. sends a small set of test queries,
4. runs the agent on those queries,
5. scores the responses,
6. prints the results when the run completes.

This mirrors a real workflow where agent quality needs to be checked repeatedly as prompts, models, or tools evolve.

---

## Architecture Overview

The workflow follows this flow:

Test items
-> eval data source
-> Azure AI agent target
-> evaluation run
-> polling loop
-> result counts
-> output item inspection

---

## Files

* `create-agent-and-evaluate.py` - main implementation
* `.env.example` - example environment variables
* `.env` - local environment variables (not committed)
* `requirements.txt` - dependencies

---

## Setup

### 1. Create a virtual environment

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

* `azure-ai-projects`
* `python-dotenv`

Note:

* The script also uses Azure identity and an OpenAI-compatible client provided by the Azure AI Projects client stack.

---

### 3. Configure environment variables

Copy:

```bash
cp .env.example .env
```

Or on Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Fill in:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<foundry-project-name>.services.ai.azure.com/api/projects/<foundry-project-name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5-nano
AZURE_AI_AGENT_NAME=<agent-name>
```

Important:

* `AZURE_AI_PROJECT_ENDPOINT` must point to your Azure AI Foundry project endpoint
* `AZURE_AI_MODEL_DEPLOYMENT_NAME` must match an existing model deployment in the project
* `AZURE_AI_AGENT_NAME` is the agent name used when creating a new version

---

### 4. Make sure Azure authentication works

The script uses `DefaultAzureCredential()`.

That means you must already be authenticated in a way the Azure SDK can use, for example:

* Azure CLI login
* Visual Studio Code Azure login
* managed identity in Azure

---

## Running the Evaluation

```bash
python create-agent-and-evaluate.py
```

You should see output similar to:

```text
Agent created (id: ..., name: ..., version: ...)
Evaluation created (id: ..., name: ...)
Evaluation run created (id: ...)
Waiting for eval run to complete... current status: queued
Waiting for eval run to complete... current status: running

[OK] Evaluation run completed successfully!
Result Counts: ...
```

If the run succeeds, the script also prints the returned output items.

---

## Implementation Details

### Key Components

* `AIProjectClient(...)`
  Connects to the Azure AI project.

* `project_client.agents.create_version(...)`
  Creates a new version of the named agent.

* `DataSourceConfigCustom(...)`
  Defines the schema for eval input items.

* `testing_criteria`
  Configures the evaluators used during the run.

* `openai_client.evals.create(...)`
  Creates the eval definition.

* `openai_client.evals.runs.create(...)`
  Starts an eval run against the configured agent target.

* `openai_client.evals.runs.retrieve(...)`
  Polls the run status until it completes or fails.

* `openai_client.evals.runs.output_items.list(...)`
  Retrieves output items for inspection after completion.

---

## Evaluation Criteria Used

The sample configures three evaluators:

* `violence_detection`
  Checks whether the response contains violent or unsafe content.

* `fluency`
  Measures the quality and readability of the generated response.

* `task_adherence`
  Checks whether the agent output follows the intended task behavior.

This shows that a single eval can combine multiple quality dimensions.

---

## Test Data Used

The sample sends two example queries:

* `What is the capital of France?`
* `How do I reverse a string in Python?`

These are intentionally simple so you can focus on the evaluation flow rather than the difficulty of the task itself.

---

## Tasks

### Task 1 - Run the Script

Run the evaluation end-to-end and confirm that:

* the agent version is created
* the eval is created
* the run starts successfully
* the polling loop eventually completes

---

### Task 2 - Inspect the Evaluation Setup

Read the script and identify:

* where the agent is created
* where the eval schema is defined
* where the evaluation criteria are configured
* where the dataset is supplied

---

### Task 3 - Expand the Dataset

Add more test items to the `content` list, for example:

* factual questions
* coding questions
* ambiguous questions
* prompts that test safety behavior

Observe how the evaluation results change.

---

### Task 4 - Change the Agent Instructions

Modify the agent instructions:

```python
"You are a helpful assistant that answers general questions"
```

Try a stricter or more specialized instruction set and compare evaluation outcomes.

---

### Task 5 - Add More Evaluation Dimensions

Experiment with additional evaluators if available in your environment.

For example, you could explore:

* groundedness
* relevance
* safety-related checks
* task-specific custom criteria

---

### Task 6 - Compare Model Deployments

Change `AZURE_AI_MODEL_DEPLOYMENT_NAME` to another deployed model and rerun the same eval.

Observe:

* whether fluency changes
* whether task adherence changes
* whether response style changes

---

### Task 7 - Clean Up Resources

Review the commented cleanup lines at the end of the script:

* eval deletion
* agent deletion

Decide whether to enable cleanup after you finish experimenting.

---

## Bonus Tasks

* store evaluation results in a file for later comparison
* turn the hardcoded test items into a JSON or CSV input file
* create separate eval suites for safety, coding, and factual QA
* compare multiple prompt versions of the same agent
* build a small report summarizing pass/fail patterns

---

## Notes

* Evaluation is not a replacement for human review, but it makes testing more repeatable
* Small datasets are useful for exploration, but larger datasets are needed for confidence
* The same agent can behave differently after prompt or model changes, so repeatable evals are valuable
* `DefaultAzureCredential()` depends on your local Azure authentication setup

---

## Key Takeaway

Agent development is not complete when the agent "works once".

Reliable agent systems need a feedback loop:

* define test cases
* run evaluations consistently
* compare results over time
* improve prompts, models, or tools based on evidence

That evaluation loop is what turns experimentation into engineering.
