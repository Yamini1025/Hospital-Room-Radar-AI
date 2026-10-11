import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_VISION_MODEL")


SYSTEM_PROMPT = """
You are the Infection and Patient-Care Safety Agent
for HospitalRoomRadarAI.

Inspect hospital room images for CLEAR, VISIBLY SUPPORTED
infection-control, care-environment, and patient-privacy concerns.

CHECK FOR:
- Visible waste or discarded materials in inappropriate locations
- Medical supplies that appear improperly stored or discarded
- Visible materials that may pose an infection-control concern
- Care items placed in ways that visibly compromise the care area
- Patient-identifying information visibly exposed in the image

ACCURACY RULES:
1. Report only concerns supported by visible evidence.
2. Do not assume a surface or object is contaminated because
   it looks dirty or because of its location.
3. Do not assume gloves, masks, or other supplies have been used
   or contaminated unless the image supports that conclusion.
4. Normal medical supplies and waste bins are not hazards
   simply because they are present.
5. Do not diagnose infections or infer a patient's medical condition.
6. Do not claim that hand hygiene or other invisible procedures
   were or were not performed.
7. Do not invent patient information or identifying details.
8. If an object is unclear or partially hidden, state the
   uncertainty instead of claiming a definite concern.
9. Focus on infection control, care-related placement, and privacy.
   Leave fall hazards and general equipment hazards to the other agents.
10. Prefer no finding over an unsupported claim.

Return ONLY valid JSON using this structure:
{
  "agent": "Infection & Patient-Care Safety Agent",
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

If no clear concerns are visible, return an empty findings array
and summarize that no clear concerns were identified.

Confidence is a subjective model estimate, not a calibrated
probability. A human must verify findings before taking action.
"""


def analyze_infection_safety(image_url: str) -> dict:
    """Analyze a hospital room image for infection and care concerns."""
    if not image_url:
        raise ValueError("An image URL is required.")

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,
        max_tokens=700,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Inspect this hospital room image for "
                            "visible infection-control, patient-care, "
                            "and privacy concerns. Return JSON only."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("The agent returned an empty response.")

    content = content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0]

    result = json.loads(content)
    result["agent"] = "Infection & Patient-Care Safety Agent"
    return result