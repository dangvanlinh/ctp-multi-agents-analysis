"""API providers: Claude, GPT, Gemini — return (text, usage_dict)."""

import sys

# Model config
CLAUDE_OPUS = "claude-opus-4-20250514"
CLAUDE_SONNET = "claude-sonnet-4-20250514"


def call_claude(system_prompt, user_message, model=None):
    """Gọi Claude API. Returns (text, usage_dict)."""
    model = model or CLAUDE_SONNET
    try:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        usage = {
            "model": response.model or model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return response.content[0].text, usage
    except ImportError:
        print("❌ Cần cài: pip install anthropic")
        sys.exit(1)
    except Exception as e:
        return f"[Claude Error: {e}]", None


def stream_claude(system_prompt, user_message, model=None):
    """Yield text chunks từ Claude streaming API.
    After iteration, call .usage on the returned generator to get usage dict.
    """
    model = model or CLAUDE_SONNET
    import anthropic
    client = anthropic.Anthropic()
    with client.messages.stream(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text
        # Capture usage after stream completes
        msg = stream.get_final_message()
        stream_claude._last_usage = {
            "model": msg.model or model,
            "input_tokens": msg.usage.input_tokens,
            "output_tokens": msg.usage.output_tokens,
        }


def get_last_stream_usage():
    """Get usage from the last stream_claude call."""
    usage = getattr(stream_claude, "_last_usage", None)
    stream_claude._last_usage = None
    return usage


def call_gpt(system_prompt, user_message):
    """Gọi GPT-4o API. Returns (text, usage_dict)."""
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        usage = {
            "model": response.model or "gpt-4o",
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }
        return response.choices[0].message.content, usage
    except ImportError:
        print("⚠️  OpenAI not installed, skipping GPT reviewer")
        return None, None
    except Exception as e:
        return f"[GPT Error: {e}]", None


def call_gemini(system_prompt, user_message):
    """Gọi Gemini API. Returns (text, usage_dict)."""
    try:
        import google.generativeai as genai
        genai.configure()
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction=system_prompt
        )
        response = model.generate_content(user_message)
        usage = None
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            um = response.usage_metadata
            usage = {
                "model": "gemini-2.0-flash",
                "input_tokens": getattr(um, "prompt_token_count", 0),
                "output_tokens": getattr(um, "candidates_token_count", 0),
            }
        return response.text, usage
    except ImportError:
        print("⚠️  Google GenAI not installed, skipping Gemini reviewer")
        return None, None
    except Exception as e:
        return f"[Gemini Error: {e}]", None
