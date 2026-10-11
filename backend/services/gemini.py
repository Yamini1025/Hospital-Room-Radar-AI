import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


REPORT_PROMPT = """
You are the final report generator for HospitalRoomRadarAI.

You receive findings from three hospital-room safety agents:
- Patient and Fall Safety
- Equipment and Environmental Safety
- Patient Care and Infection Safety

Your job is to organize the findings into a clear, concise final report.

IMPORTANT:
- Only use findings provided by the safety agents.
- Do not invent hazards, evidence, measurements, regulations, or medical advice.
- Do not claim that a room is completely safe.
- "No visible concerns identified" is acceptable when there are no findings.
- Every reported finding requires human verification.
- Keep the report practical and easy for hospital staff to understand.

Return ONLY valid JSON in this structure:

{
  "overall_summary": "Brief summary of the room's visible safety findings.",
  "findings": [
    {
      "hazard": "Short description",
      "evidence": "Visible evidence provided by the agents",
      "risk_level": "Low, Medium, or High",
      "source_agent": "Agent that identified the finding",
      "recommended_action": "Practical next step",
      "needs_verification": true
    }
  ],
  "needs_verification": true
}

If there are no findings, return:

{
  "overall_summary": "No visible safety concerns were identified in the provided analysis.",
  "findings": [],
  "needs_verification": false
}
"""


def generate_report(analysis: dict) -> dict:
    """Generate a final hospital-room safety report from agent findings."""

    if not analysis:
        raise ValueError("Analysis data is required.")

    prompt = f"""
{REPORT_PROMPT}

Here is the safety-agent analysis:

{json.dumps(analysis, indent=2)}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "temperature": 0.1,
            "response_mime_type": "application/json",
        },
    )

    result = response.text

    if not result:
        raise ValueError("Gemini returned an empty response.")

    report = json.loads(result)

    if not isinstance(report.get("findings"), list):
        raise ValueError("Gemini returned an invalid findings structure.")

    if report["findings"]:
        report["needs_verification"] = True

        for finding in report["findings"]:
            finding["needs_verification"] = True
    else:
        report["needs_verification"] = False

    return report