from agents.coordinator import analyze_room
from services.gemini import generate_report


def analyze_hospital_room(image_url: str) -> dict:
    """Run the safety agents and generate a final Gemini report."""

    analysis = analyze_room(image_url)

    if analysis["errors"]:
        return {
            **analysis,
            "final_report": None,
            "message": (
                "Analysis incomplete. One or more safety agents failed. "
                "Human review is required."
            ),
        }

    report = generate_report(analysis)

    return {
        **analysis,
        "final_report": report,
        "message": "Analysis completed. Verify findings before taking action.",
    }