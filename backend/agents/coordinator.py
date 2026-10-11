import time

from agents.fall_safety import analyze_fall_safety
from agents.equipment_safety import analyze_equipment_safety
from backend.agents.infection_hygiene import analyze_infection_safety


def analyze_room(image_url: str) -> dict:
    """Run agents sequentially with a 5-second delay between calls."""

    agent_functions = [
        ("fall_safety", analyze_fall_safety),
        ("equipment_safety", analyze_equipment_safety),
        ("patient_care", analyze_infection_safety),
    ]

    results = {}
    errors = {}

    for index, (name, function) in enumerate(agent_functions):
        try:
            results[name] = function(image_url)
        except Exception as exc:
            errors[name] = str(exc)

        if index < len(agent_functions) - 1:
            time.sleep(5)

    findings = []

    for agent_name, result in results.items():
        for finding in result.get("findings", []):
            findings.append({
                **finding,
                "source_agent": agent_name,
                "needs_verification": True,
            })

    return {
        "agents": results,
        "findings": findings,
        "errors": errors,
        "needs_verification": bool(findings) or bool(errors),
        "status": "complete" if not errors else "partial",
    }
