import json
import re
from pathlib import Path
import sys

def extract_money_values(text):
    matches = re.findall(r"\$\s?\d+", text)
    return [int(m.replace("$", "").strip()) for m in matches]

def extract_possible_services(text):
    service_keywords = [
        "install",
        "installation",
        "repair",
        "replace",
        "replacement",
        "wiring",
        "hookup",
        "electrical",
        "charger",
        "generator",
        "outlet",
        "fixture"
    ]
    services = set()
    sentences = text.splitlines()
    for line in sentences:
        l = line.lower().strip()
        if len(l) < 15:
            continue
        if any(word in l for word in service_keywords):
            cleaned = " ".join(l.split())
            services.add(cleaned[:80])

    return list(services)

def analyze_transcript(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    services = extract_possible_services(text)
    money_values = extract_money_values(text)
    spec = {
        "account_id": "bens-electric",
        "agent_name": "Clara - Ben's Electric",
        "version": "v1",
        "voice_style": "professional and friendly",
        "services_supported": services,
        "pricing_signals": money_values,
        "agent_behaviors": [
            "answer inbound calls",
            "collect caller information",
            "schedule appointments",
            "filter spam calls"
        ],
        "system_prompt_summary": "AI call answering assistant for an electrical services business",
        "call_transfer_protocol": {
            "transfer_condition": "caller requests human assistance or emergency situation",
            "timeout_seconds": 60,
            "fallback_action": "collect caller information and promise follow-up"
        },
        "fallback_protocol": {
            "required_information": [
                "caller_name",
                "caller_phone",
                "service_address",
                "issue_description"
            ],
            "confirmation_message": "Thank the caller and confirm someone will follow up."
        }
    }

    return spec

def main():

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "dataset/demo_calls/bens_electric_demo.txt"
    output_file = "outputs/accounts/bens-electric/v1/v1_agent_spec.json"
    spec = analyze_transcript(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    print("Agent spec written to:", output_file)


if __name__ == "__main__":
    main()