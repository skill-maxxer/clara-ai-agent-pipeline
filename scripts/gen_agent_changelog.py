import json
from pathlib import Path

def load_customer_profile():
    path = Path("outputs/customer_profile.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_changelog(profile):
    lines = []
    lines.append("# Agent Changelog")
    
    lines.append("")
    lines.append("Updates after onboarding call:")

    if profile.get("service_call_fee"):
        lines.append(
            f"> Added service call fee policy: ${profile['service_call_fee']}."
        )
    if profile.get("hourly_rate"):
        lines.append(
            f"> Added hourly billing information: approximately ${profile['hourly_rate']} per hour."
        )
    if profile.get("business_hours"):
        lines.append(
            f"> Added business operating hours: {profile['business_hours']}."
        )
    if profile.get("priority_context"):
        lines.append(
            "> Added handling instructions for after-hours or priority customers."
        )

    return "\n".join(lines)


def main():
    profile = load_customer_profile()
    changelog = build_changelog(profile)

    output_path = Path("outputs/agent_changelog.txt")
    output_path.write_text(changelog, encoding="utf-8")

    print("Agent changelog saved to:", output_path)


if __name__ == "__main__":
    main()