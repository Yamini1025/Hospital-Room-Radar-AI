import os
import json
from urllib.request import Request, urlopen
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv(
    "GROQ_MODEL",
    "qwen/qwen3.8-27b"
)

SYSTEM_PROMPT = """
You are the Patient and Fall Safety Agent for Hospital Room Radar AI.

Your job is to identify CLEAR, VISIBLY SUPPORTED fall and mobility
hazards in hospital room images. Accuracy matters more than the
number of findings. Do not invent hazards to fill the report.

CHECK FOR:
- Loose cables lying across open walking areas
- Objects on the floor in a patient's walking path
- Furniture clearly obstructing the route between the bed and
  the main doorway
- Mobility aids that are visibly blocked or inaccessible
- Clearly visible wet-looking floor areas in walking paths

SPATIAL REASONING RULES:
1. Distinguish the main walking path from the room's perimeter,
   corners, alcoves, and secondary doorways.
2. A chair parked against a wall is NOT an obstruction unless
   the image clearly shows it intruding into the main walking path.
3. A doorway is NOT blocked just because furniture is visible
   somewhere nearby. Look for actual overlap with the entrance.
4. Cables bundled, tethered, secured, or routed along walls or
   equipment poles are NOT trip hazards by themselves.
5. Only flag a cable when it is visibly loose across an open
   walking area or creates another clearly evidenced hazard.
6. Do not infer a hazard from an object's color, proximity, or
   mere presence in the room.
7. If perspective, occlusion, or image quality makes the layout
   uncertain, state the uncertainty rather than claiming a hazard.
8. Do not invent details about objects or their positions.

DECISION RULE:
- Report only clear, evidence-supported potential hazards.
- If no clear hazard is visible, return an empty findings array.
- Do not force findings simply because this is a safety audit.
- Prefer a false negative over an unsupported safety claim.
- Never certify a room as completely safe.

Return ONLY valid JSON in this structure:
{
  "agent": "Patient & Fall Safety Agent",
  "findings": [
    {
      "hazard": "Short description",
      "evidence": "Specific visible evidence",
      "risk_level": "Low, Medium, or High",
      "confidence": 0.0,
      "needs_verification": true
      "recommended_action": "Practical check or corrective action"
    }
  ],
  "summary": "Brief summary of visible findings",
  "needs_verification": true
}

If there are no clear hazards, return:
{
  "agent": "Patient & Fall Safety Agent",
  "findings": [],
  "summary": "No clear fall or mobility hazards were identified in the visible image.",
  "needs_verification": false
}

Confidence is a subjective model estimate, not a calibrated probability.
A human must verify findings before taking action.
"""

def analyze_fall_safety(image_url: str) -> dict:
    """Analyze one hospital room image for potential fall hazards."""
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
                            "Inspect this image for visible patient "
                            "fall and mobility hazards. Return JSON only."
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
    result["agent"] = "Patient & Fall Safety Agent"
    return result