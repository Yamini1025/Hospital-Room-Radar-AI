
import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EQUIPMENT_SAFETY_PROMPT = """
You are the Equipment and Environmental Safety Agent for HospitalRoomRadarAI.

Your job is to identify CLEAR, VISIBLY SUPPORTED equipment and
environmental hazards in hospital room images. Accuracy matters
more than the number of findings. Do not invent hazards.

CHECK FOR:
- Loose cables or tubing across open walking areas
- Equipment or furniture clearly obstructing doors or walking paths
- Equipment positioned in a visibly unstable or hazardous way
- Objects stored in locations that clearly create an obstruction
- Loose objects or clutter interfering with access to beds, equipment,
  or exits

SPATIAL REASONING RULES:
1. Distinguish the main walking path from walls, corners, and alcoves.
2. Equipment near a doorway is NOT an obstruction unless it clearly
   interferes with the entrance or walking path.
3. Cables secured, bundled, or routed along walls/equipment are NOT
   hazards unless they visibly extend across an open walking area.
4. Do not identify an object as a syringe, medication, or biohazard
   unless its identity is clearly visible.
5. Do not assume equipment is broken, unsecured, or malfunctioning
   unless this is visibly supported.
6. Do not invent measurements, regulations, or safety requirements.
7. If perspective, occlusion, or image quality creates uncertainty,
   state the uncertainty instead of assuming.

DECISION RULE:
- Report only clear, evidence-supported potential hazards.
- If no clear hazard is visible, return an empty findings array.
- Never force findings simply because this is a safety audit.
- Never certify a room as completely safe.

VERIFICATION RULE:
- If ANY hazard is identified, set that finding's "needs_verification"
  to true.
- Every finding must have "needs_verification": true, regardless of
  risk level, confidence, or urgency.
- The overall "needs_verification" must be true whenever the findings
  array contains at least one hazard.
- Only set "needs_verification": false when the findings array is empty.
- Confidence describes how clearly the hazard is visible; it does NOT
  determine whether verification is required.

Return ONLY valid JSON:
{
  "agent": "equipment_environmental_safety",
  "findings": [
    {
      "hazard": "Short description",
      "evidence": "Specific visible evidence",
      "risk_level": "Low, Medium, or High",
      "confidence": 0.0,
      "needs_verification": true,
      "recommended_action": "Practical check or corrective action"
    }
  ],
  "summary": "Brief summary of visible findings",
  "needs_verification": true
}

If there are no clear hazards, return:
{
  "agent": "equipment_environmental_safety",
  "findings": [],
  "summary": "No clear equipment or environmental hazards were identified in the visible image.",
  "needs_verification": false
}

Confidence is a subjective model estimate, not a calibrated probability.
A human must verify findings before taking action.
"""


def analyze_equipment_safety(image_url: str) -> dict:
    """Analyze a hospital-room image for equipment and environmental hazards."""

    if not image_url:
        raise ValueError("An image URL is required.")

    response = client.chat.completions.create(
        model=os.getenv("GROQ_VISION_MODEL"),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": EQUIPMENT_SAFETY_PROMPT,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            }
        ],
        temperature=0.1,
        max_tokens=700,
        response_format={"type": "json_object"},
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Groq returned an empty response.")

    parsed_result = json.loads(result)

    # Basic validation of the response structure.
    if not isinstance(parsed_result.get("findings"), list):
        raise ValueError("The agent returned an invalid findings structure.")

    if parsed_result.get("agent") != "equipment_environmental_safety":
        raise ValueError("The agent returned an unexpected agent identifier.")

    # Enforce the verification rule.
    if parsed_result["findings"]:
        parsed_result["needs_verification"] = True

        for finding in parsed_result["findings"]:
            finding["needs_verification"] = True
    else:
        parsed_result["needs_verification"] = False

    return parsed_result
