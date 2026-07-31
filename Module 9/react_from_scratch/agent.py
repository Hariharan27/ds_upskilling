import json
import os

from dotenv import load_dotenv
from together import Together
from together.types.chat import completion_create_params
from together.types.chat.completion_create_params import (
    MessageChatCompletionSystemMessageParam,
    MessageChatCompletionUserMessageParam,
    MessageChatCompletionToolMessageParam,
    MessageChatCompletionAssistantMessageParam,
    ToolChoiceParam,
)

from tool_registry import TOOL_DEFINITIONS, get_tool

load_dotenv()

print(bool(os.getenv("TOGETHER_API_KEY")))

client = Together(
    api_key=os.getenv("TOGETHER_API_KEY"),
)

MODEL = "openai/gpt-oss-20b"

def run_agent(
        user_input: str,
) -> None:

    messages: list[completion_create_params.Message] = [
        MessageChatCompletionSystemMessageParam(
            role="system",
            content=(
                "You are a travel planning agent. "
                "Your goal is to create a practical travel plan "
                "that satisfies the user's requirements and budget. "

                "Use the available tools to obtain information required "
                "to make decisions. "

                "Never invent or guess values that can be obtained from tools. "

                "When multiple independent pieces of information are needed, "
                "you may request those tools together. "

                "When a tool requires values produced by another tool, "
                "wait until you receive those tool results before calling "
                "the dependent tool. "

                "Base your final answer only on information provided by the user "
                "and observations returned by tools. "
            ),
        ),
        MessageChatCompletionUserMessageParam(
            role="user",
            content=user_input,
        ),
    ]

    max_iterations = 5

    for iteration in range(max_iterations):

        print(
            f"\nAgent Iteration: {iteration + 1}"
        )

        # 1. Let the LLM decide the next action
        response = client.chat.completions.create(
            messages=messages,
            model=MODEL,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # 2. Stop when the LLM produces a final answer
        if not message.tool_calls:
            print("\nFinal Response:")
            print(message.content)
            return

        print(
            f"\nNumber of tool calls: "
            f"{len(message.tool_calls)}"
        )

        # 3. Convert response-side tool calls
        # into request-side tool call messages
        assistant_tool_calls: list[ToolChoiceParam] = [
            ToolChoiceParam(
                id=tool_call.id,
                type="function",
                function={
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            )
            for tool_call in message.tool_calls
        ]

        # 4. Record the LLM's actions in conversation history
        messages.append(
            MessageChatCompletionAssistantMessageParam(
                role="assistant",
                content=message.content or "",
                tool_calls=assistant_tool_calls,
            )
        )

        # 5. Execute every tool selected by the LLM
        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(
                f"Tool Name: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            # 6. Resolve the actual Python function
            tool = get_tool(
                tool_name
            )

            if not tool:
                raise ValueError(
                    f"Tool {tool_name} not found."
                )

            # 7. Execute the action
            result = tool(
                **arguments
            )

            print(
                f"Observation: {result}"
            )

            # 8. Record the observation
            messages.append(
                MessageChatCompletionToolMessageParam(
                    role="tool",
                    tool_call_id=tool_call.id,
                    content=json.dumps(result),
                )
            )

        # After this point, the for-loop naturally
        # starts the next agent iteration.
        #
        # The next LLM call receives:
        # User goal
        # + previous tool calls
        # + tool observations

    # 9. Safety boundary
    # Reached only if every iteration requested more tools
    raise RuntimeError(
        f"Agent exceeded the maximum "
        f"{max_iterations} iterations."
    )