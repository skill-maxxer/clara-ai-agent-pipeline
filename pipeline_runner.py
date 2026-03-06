import subprocess
from pathlib import Path


def run_step(description, command):
    print(f"\n{description}")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"Error during step: {description}")
        exit(1)


def main():
    demo_folder = Path("dataset/demo_calls")
    onboarding_folder = Path("dataset/onboarding_calls")

    demo_files = list(demo_folder.glob("*.txt"))
    onboarding_files = list(onboarding_folder.glob("*.m4a"))

    print(f"\nFound {len(demo_files)} demo call transcript(s)")
    print(f"Found {len(onboarding_files)} onboarding recording(s)")

    for demo_file in demo_files:
        print(f"\nProcessing demo transcript: {demo_file.name}")
        run_step(
            "Analyzing demo call",
            f"python scripts/analyze_demo_call.py {demo_file}"
        )
        run_step(
            "Generating V1 agent prompt",
            "python scripts/gen_agent_prompt.py"
        )

    for onboarding_file in onboarding_files:
        print(f"\nProcessing onboarding recording: {onboarding_file.name}")
        run_step(
            "Transcribing onboarding call",
            f"python scripts/transcribe_onboarding.py {onboarding_file}"
        )
        run_step(
            "Analyzing onboarding call",
            "python scripts/analyze_onboarding_call.py"
        )
        run_step(
            "Generating V2 agent prompt",
            "python scripts/gen_v2_agent_prompt.py"
        )
        run_step(
            "Generating agent changelog",
            "python scripts/gen_agent_changelog.py"
        )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()