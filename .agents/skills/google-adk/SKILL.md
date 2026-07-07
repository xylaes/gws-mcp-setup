---
name: google-adk
description: Guidance and code patterns for writing, maintaining, and developing AI agents using the Google Agent Development Kit (ADK).
---

# Google Agent Development Kit (ADK) Skill

Use this skill to guide your code generation, modification, and debugging when working with projects built using the Google Agent Development Kit (ADK).

## Core Concepts & Imports
Ensure you import correct classes based on ADK 2.0+ architecture:
```python
from google.adk import Agent, Context, Event, Workflow
from google.adk.events import RequestInput
```

---

## 1. Defining Tools
Tools are standard Python functions decorated with descriptive docstrings. The ADK parser converts docstrings into tool definitions for the LLM.
```python
def my_tool(param1: str, param2: float) -> dict:
    """Detailed description of what the tool does.

    Args:
        param1: Explanation of param1.
        param2: Explanation of param2.

    Returns:
        Structured response dictionary.
    """
    return {"status": "success", "result": f"{param1} -> {param2}"}
```

---

## 2. Defining Agents
Agents handle LLM reasoning. Use them for single-turn or multi-turn agentic steps.
```python
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    query: str = Field(description="Query to analyze")

my_agent = Agent(
    name="analyst_agent",
    model="gemini-2.5-flash",
    mode="single_turn",  # 'single_turn' or 'multi_turn'
    instruction="Analyze the input query and call the appropriate tool.",
    input_schema=InputSchema,
    tools=[my_tool],
)
```

---

## 3. Defining Graph-based Workflows
Workflows orchestrate multiple agents and function nodes using a graph-based routing engine.
```python
# A workflow is initialized by specifying the root node and routing edges
my_workflow = Workflow(
    name="my_workflow_agent",
    edges=[
        ("START", first_node_fn, router_fn),
        (
            router_fn,
            {
                "ROUTE_A": agent_node,
                "ROUTE_B": direct_node_fn,
            },
        ),
        (agent_node, end_node_fn),
    ],
)

# Entrypoint alias expected by the Agent Runtime (scaffolded apps)
app = my_workflow
```

---

## 4. Human-in-the-Loop (HITL) Checkpoints
To pause a workflow and wait for human input, write a node that yields `RequestInput`:
```python
def request_approval_node(node_input: dict, ctx: Context):
    # Save session state before yielding
    ctx.state["current_task"] = node_input
    
    # Yielding RequestInput pauses execution and waits for user input
    yield RequestInput(
        message="Please review the data and approve or reject.",
        payload=node_input,
    )

def process_decision_node(node_input: dict, ctx: Context) -> Event:
    # node_input here contains the response payload from the user's HITL action
    decision = node_input.get("decision", "reject")
    approved = decision == "approve"
    
    status = "approved" if approved else "rejected"
    return Event(output={"status": status})
```
*Note: Edges routing to `request_approval_node` will trigger the pause automatically.*
