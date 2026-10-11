import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_VISION_MODEL")


PATIENT_ACCESSIBILITY_PROMPT = """
You are the Patient Accessibility Agent for HospitalRoomRadarAI.

Your job is to identify CLEAR, VISIBLY SUPPORTED concerns with
patient access to essential items, assistance, and medical equipment
in hospital room images. Accuracy matters more than the number of
findings. Do not invent hazards.

CHECK FOR:
- Nurse-call buttons, call cords, or call remotes that appear
  visibly out of reach, trapped behind furniture, or inaccessible
  from the patient's bed 
- If there is a call cord attached to any machine or device, check whether it is visibly reachable from the bed. 
  If not, report it as a potential accessibility concern.
- Mobility aids, such as walkers, wheelchairs, or canes, that appear
  inaccessible to a patient who may need them
- IV stands or other patient-associated equipment that appear
  positioned so the patient cannot readily access or use them
  when access would reasonably be needed
- Essential personal items, such as water, eyeglasses, or
  frequently used belongings, placed visibly beyond the patient's
  apparent reach
- Patient controls or bedside items blocked by furniture or
  other objects, preventing apparent access from the bed
- Bedside assistance devices or essential items placed in locations
  that appear difficult for the patient to access independently
- Disconnected or unplugged cords

SPATIAL REASONING RULES:
1. Judge accessibility relative to the patient's visible position,
   especially the bed, rather than the room in general.
2. A nurse-call device on the bed or bedside table is NOT a hazard
   unless it appears inaccessible, obstructed, or out of reach.
3. Mobility aids near the bed are NOT automatically inaccessible.
   Flag them only when visible placement suggests the patient
   cannot readily reach or access them.
4. An IV stand or medical device is NOT inaccessible simply because
   it is beside the bed. Look for clear evidence of blocked access.
5. Do not assume the patient's mobility, physical abilities,
   treatment needs, or ability to reach an item unless supported
   by visible evidence.
6. Do not assume an item is missing just because it is not visible.
7. Do not confuse general walking-path obstructions, trip hazards,
   or wet floors with patient accessibility concerns. Leave those
   hazards to the Patient & Fall Safety Agent.
8. If perspective, occlusion, or image quality makes accessibility
   uncertain, state the uncertainty instead of assuming.

DECISION RULE:
- Report only clear, evidence-supported potential accessibility
  concerns.
- Describe the visible placement and explain why it may limit
  patient access.
- If no clear concern is visible, return an empty findings array.
- Never force findings simply because this is a safety audit.
- Never certify a room as completely safe.

VERIFICATION RULE:
- Every finding must have "needs_verification": true.
- The overall "needs_verification" must be true whenever the
  findings array contains at least one concern.
- Only set the overall value to false when the findings array
  is empty.
- Image-based observations must be verified by a human.

OUTPUT FORMAT:
Return valid JSON only, with this structure:
{
  "agent": "Patient Accessibility Agent",
  "findings": [
    {
      "hazard": "Short description of the accessibility concern",
      "evidence": "What is visibly shown in the image",
      "risk_level": "low, medium, or high",
      "confidence": "low, medium, or high",
      "needs_verification": true,
      "recommended_action": "Practical action to check or improve access"
    }
  ],
  "summary": "Brief summary of the visible accessibility concerns",
  "needs_verification": true
}

If no clear accessibility concerns are visible, return:
{
  "agent": "Patient Accessibility Agent",
  "findings": [],
  "summary": "No clear patient accessibility concerns are visible
  in the image.",
  "needs_verification": false
}

Return JSON only. Do not include Markdown or additional commentary.
"""

def analyze_patient_accessibility(image_url: str) -> dict:
    """Analyze a hospital-room image for patient accessibility concerns."""

    if not image_url:
        raise ValueError("An image URL is required.")

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,
        max_tokens=700,
        messages=[
            {
                "role": "system",
                "content": PATIENT_ACCESSIBILITY_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Inspect this image for clear patient accessibility "
                            "concerns, such as an inaccessible nurse-call button, "
                            "mobility aid, or essential patient item. Return JSON only."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The agent returned an empty response.")

    parsed_result = json.loads(content)
    parsed_result["agent"] = "Patient Accessibility Agent"

    return parsed_result