import json
from pathlib import Path


def load_agent_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_services(services):
    triggers = [
        "do you",
        "can you",
        "i'm looking",
        "i was wondering",
        "we want",
        "looking for"
    ]
    cleaned = []
    for s in services:
        s = s.lower().strip()
        if len(s) < 25:
            continue
        if any(t in s for t in triggers):
            cleaned.append(s)

    cleaned = list(set(cleaned))

    return cleaned[:8]


def build_prompt(spec):
    services_list = clean_services(spec.get("detected_services", []))
    services = "\n".join(f"- {s}" for s in services_list)
    behaviors = "\n".join(
        f"- {b}" for b in spec.get("agent_behaviors", [])
    )
    prices = spec.get("detected_prices", [])
    pricing_text = ", ".join(str(p) for p in prices) if prices else "Not specified"
    prompt = f"""
You are Clara, an AI call answering assistant for an electrical services business.
Your responsibilities:
{behaviors}

Services offered may include:
{services}

Pricing mentioned in conversation:
{pricing_text}

When answering calls:
- greet the caller politely
- understand the customer's electrical issue
- collect caller name and contact information
- determine the type of service requested
- schedule a service appointment if appropriate
- filter out spam or sales calls

Business hours call flow:
- greet the caller
- ask the purpose of the call
- collect caller name and phone number
- understand the service request
- schedule an appointment or route appropriately
- if the caller asks for a human, attempt to transfer the call
- if transfer fails, collect details and promise follow-up
- ask if they need anything else before ending the call

After-hours call flow:
- greet the caller and inform them the office may be closed
- ask the purpose of the call
- determine whether the issue is an emergency
- if emergency, collect name, phone number, and address immediately
- attempt call transfer if emergency support is available
- if transfer fails, apologize and confirm someone will follow up
- if not an emergency, collect details and confirm follow-up during business hours
- ask if the caller needs anything else before closing

Always maintain a professional and helpful tone.
"""

    return prompt.strip()

def main():
    spec_file = Path("outputs/v1_agent_spec.json")
    output_file = Path("outputs/accounts/bens-electric/v1/v1_agent_prompt.txt")
    spec = load_agent_spec(spec_file)
    prompt = build_prompt(spec)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    print("V1 agent prompt saved to:", output_file)

if __name__ == "__main__":
    main()