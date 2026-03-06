import json
import re
from pathlib import Path


def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

def detect_business_hours(text):
    lower = text.lower()
    if "monday" in lower and "friday" in lower:
        return "Monday to Friday"

    return None

def detect_priority_context(text):
    triggers = [
        "after hours",
        "emergency",
        "property manager",
        "gas station",
        "dispatch"
    ]

    sentences = re.split(r"[.!?]", text)
    matches = []

    for s in sentences:
        lower = s.lower()
        if any(t in lower for t in triggers):
            matches.append(s.strip())

    return matches[:3] if matches else None

def extract_pricing(text):
    result = {
        "service_call_fee": None,
        "hourly_rate": None
    }
    service_match = re.search(
        r"(service|call\s*out|call\s*fee)[^\d]{0,20}\$?(\d+)",
        text,
        re.IGNORECASE
    )
    if service_match:
        result["service_call_fee"] = int(service_match.group(2))

    hourly_match = re.search(
        r"\$?(\d+)[^\n]{0,20}(hour|hourly|per\s*hour)",
        text,
        re.IGNORECASE
    )
    if hourly_match:
        result["hourly_rate"] = int(hourly_match.group(1))

    return result

def analyze_onboarding_transcript(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    profile = {
        "service_call_fee": None,
        "hourly_rate": None,
        "business_hours": detect_business_hours(text),
        "priority_context": detect_priority_context(text),
        "notification_email": extract_email(text)
    }
    pricing = extract_pricing(text)

    profile["service_call_fee"] = pricing["service_call_fee"]
    profile["hourly_rate"] = pricing["hourly_rate"]

    return profile

def main():
    input_file = "outputs/onboarding_transcript.txt"
    output_file = "outputs/customer_profile.json"
    profile = analyze_onboarding_transcript(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

    print("Customer profile saved to:", output_file)

if __name__ == "__main__":
    main()