"""Claude API client wrapper with retry logic and structured output."""

import anthropic
import json
import time
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from config import get_settings


_client: Optional[anthropic.Anthropic] = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        settings = get_settings()
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_claude(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    tools: Optional[list] = None,
) -> dict:
    """
    Call Claude API with retry logic.

    Returns:
        {
            "content": str,          # Text response
            "tool_calls": list,      # Any tool use blocks
            "usage": dict,           # Token usage
            "latency_ms": int,       # Round-trip time
            "model": str,            # Model used
        }
    """
    client = get_client()
    settings = get_settings()

    start = time.time()

    kwargs = {
        "model": settings.claude_model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }

    if tools:
        kwargs["tools"] = tools

    response = client.messages.create(**kwargs)

    latency_ms = int((time.time() - start) * 1000)

    # Parse response
    text_content = ""
    tool_calls = []

    for block in response.content:
        if block.type == "text":
            text_content += block.text
        elif block.type == "tool_use":
            tool_calls.append({
                "id": block.id,
                "name": block.name,
                "input": block.input,
            })

    return {
        "content": text_content,
        "tool_calls": tool_calls,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
        "latency_ms": latency_ms,
        "model": settings.claude_model,
    }


def call_claude_json(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
) -> dict:
    """
    Call Claude and parse response as JSON.
    Adds explicit JSON instruction to the prompt.
    """
    json_instruction = "\n\nRespond ONLY with valid JSON. No markdown, no backticks, no explanation."
    result = call_claude(
        system_prompt=system_prompt + json_instruction,
        user_message=user_message,
        max_tokens=max_tokens,
        temperature=0.0,
    )

    # Clean and parse JSON
    content = result["content"].strip()
    # Remove potential markdown code fences
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            raise ValueError(f"Failed to parse JSON from Claude response: {content[:200]}")

    result["parsed"] = parsed
    return result
