import json
from pathlib import Path

def load_v1_prompt():
    path = Path("outputs/v1_agent_prompt.txt")
    return path.read_text(encoding="utf-8")

def load_customer_profile():
    path = Path("outputs/customer_profile.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_v2_prompt(v1_prompt, profile):
    additions = []
    if profile.get("service_call_fee"):
        additions.append(
            f"- Inform customers that there is a service call fee of ${profile['service_call_fee']}."
        )
    if profile.get("hourly_rate"):
        additions.append(
            f"- After the service call, work is billed at approximately ${profile['hourly_rate']} per hour."
        )
    if profile.get("business_hours"):
        additions.append(
            f"- The business operates primarily during {profile['business_hours']}."
        )
    if profile.get("priority_context"):
        additions.append(
            "- Be aware that some existing customers may require after-hours or priority handling."
        )

    additions_text = "\n".join(additions)

    updated_prompt = f"""
{v1_prompt}

Additional instructions from onboarding call:
{additions_text}

Always remain polite, helpful, and focused on collecting the necessary job details.
"""

    return updated_prompt.strip()


def main():
    v1_prompt = load_v1_prompt()
    profile = load_customer_profile()

    v2_prompt = build_v2_prompt(v1_prompt, profile)

    output_path = Path("outputs/v2_agent_prompt.txt")
    output_path.write_text(v2_prompt, encoding="utf-8")

    print("Updated agent prompt saved to:", output_path)


if __name__ == "__main__":
    main()