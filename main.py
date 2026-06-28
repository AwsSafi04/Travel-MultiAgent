import uuid
from supervisor import create_supervisor_agent


def stream_response(agent, query: str, config: dict):

    """Stream the agent's response and print messages"""
    print(f" User: {query}\n")
    print("-" * 50)

    for step in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    ):
        for update in step.values():
            if isinstance(update, dict):
                for message in update.get("messages", []):
                    # Check and print tool call
                    if hasattr(message, "tool_calls") and message.tool_calls:
                        for tool_call in message.tool_calls:
                            print(f"\n Calling: {tool_call['name']}")

                    elif hasattr(message, "text") and message.text:
                        if message.__class__.__name__ == "AIMessage":
                            print(f"\n Assistant:\n{message.text}")


def main():
    """Run an interactive mode for queries"""
    print("\n"+ "=" * 70)
    print("SMART TRAVEL PLANNER - Interactive Mode")
    print("=" * 70 + "\n")

    print("Initializing agents....")

    try:
        supervisor = create_supervisor_agent(
            model_name="openai:gpt-4o-mini",
            use_memory=True
        )

        print(" Ready! Type your planning questions.\n")
        print("Commands: 'quit' to exit, 'new' for new conversation\n")

    except Exception as e:
        print(f" Error: {e}")
        return
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:

            query = input("\n You: ").strip()

            if query.lower() == "quit":
                print("\n Goodbye! Happy Travels!")
                break
            elif query.lower() == "new":
                thread_id = str(uuid.uuid4())
                config = {"configurable": {"thread_id": thread_id}}
                print(" Started new conversation!")
                continue
            elif not query:
                continue

            stream_response(supervisor, query, config)

        except KeyboardInterrupt:
            print("\n\n Goodbye!")
            break


if __name__ == "__main__":
    main()