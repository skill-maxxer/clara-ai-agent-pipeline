import json
import re
from pathlib import Path

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
        "detected_services": services,
        "detected_prices": money_values,
        "agent_behaviors": [
            "answer inbound calls",
            "collect caller information",
            "schedule appointments",
            "filter spam calls"
        ]
    }

    return spec

def main():

    input_file = "dataset/demo_calls/bens_electric_demo.txt"
    output_file = "outputs/v1_agent_spec.json"
    spec = analyze_transcript(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    print("Agent spec written to:", output_file)


if __name__ == "__main__":
    main()