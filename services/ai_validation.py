"""Simple AI output validation helpers.
These utilities provide structural and semantic checks for AI outputs
and can be imported by tests or by services in the future.
"""
from typing import Dict, Any


def validate_analysis_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that the AI analysis output contains expected keys and
    that numeric fields are within sensible ranges. Returns a dict with
    `valid` bool and `errors` list.
    """
    errors = []

    if not isinstance(output, dict):
        return {"valid": False, "errors": ["Output is not an object"]}

    # Required top-level keys
    required_keys = ["vegetation_health", "ndvi_value", "ai_insights"]
    for k in required_keys:
        if k not in output:
            errors.append(f"Missing key: {k}")

    # NDVI range check
    ndvi = output.get("ndvi_value")
    if ndvi is not None:
        try:
            ndvi_f = float(ndvi)
            if ndvi_f < -1.0 or ndvi_f > 1.0:
                errors.append(f"ndvi_value out of range: {ndvi}")
        except Exception:
            errors.append("ndvi_value is not a number")

    # vegetation_health sanity
    vh = output.get("vegetation_health")
    if vh is not None and not isinstance(vh, str):
        errors.append("vegetation_health should be a string")

    return {"valid": len(errors) == 0, "errors": errors}
