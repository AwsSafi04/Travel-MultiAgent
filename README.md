# Smart Travel Planner

A multi-agent travel planning system built with LangChain/LangGraph using the SubAgents pattern. A central supervisor agent routes requests to specialized subagents and synthesizes their results into a travel plan.

## Architecture

```
User Request
     │
     ▼
┌─────────────────┐
│   SUPERVISOR    │  routes requests + synthesizes results
└────────┬────────┘
         │
 ┌───────┼───────────┬────────────┐
 ▼       ▼           ▼            ▼
FLIGHTS  HOTELS  ACTIVITIES  ITINERARY
 AGENT   AGENT    AGENT        AGENT
```

## Project Structure

```
.
├── main.py              # Entry point with demo scenarios
├── supervisor.py        # Supervisor agent + subagent tool wrappers
├── subagents/
│   ├── __init__.py
│   ├── flights.py       # Flight search specialist
│   ├── hotels.py        # Hotel search specialist
│   ├── activities.py    # Activities & restaurants specialist
│   └── itinerary.py     # Itinerary planning specialist
├── tools/
│   ├── __init__.py
│   └── mock_data.py     # Mock travel data
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set your API key:

```bash
export OPENAI_API_KEY='your-key-here'
# or
export ANTHROPIC_API_KEY='your-key-here'
```

## Usage

```bash
python main.py
```

Runs three demo scenarios: a full trip plan (all subagents), a single-domain request (hotels only), and a follow-up that uses conversation memory.

## How It Works

The supervisor is a `create_agent` instance whose tools are the wrapped subagents:

```python
supervisor = create_agent(
    model,
    tools=[search_flights, search_hotels, search_activities, create_itinerary],
    system_prompt=SUPERVISOR_PROMPT,
    checkpointer=InMemorySaver(),
)
```

Each subagent is exposed to the supervisor as a tool:

```python
@tool
def search_flights(request: str) -> str:
    """Search for flights to a destination."""
    result = flights_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text
```

### Key APIs

| Component         | Import                                                   |
| ----------------- | ------------------------------------------------------- |
| Create agent      | `from langchain.agents import create_agent`             |
| Define tool       | `from langchain.tools import tool`                      |
| Initialize model  | `from langchain.chat_models import init_chat_model`     |
| Memory            | `from langgraph.checkpoint.memory import InMemorySaver` |

## Extending

**Add a subagent:** create `subagents/new_agent.py` with its own `create_agent` and tools, wrap it as a `@tool` in `supervisor.py`, then add it to the supervisor's tools list.

**Use real APIs:** replace the mock functions in `tools/mock_data.py` with real calls — e.g. Amadeus or Skyscanner for flights, Booking.com for hotels, TripAdvisor or Viator for activities.

## References

- [LangChain Multi-Agent docs](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [SubAgents Pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)
- [Personal Assistant Tutorial](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant)

## License

MIT