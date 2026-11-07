"""Check response format without claiming factual or financial correctness."""
import re

HEADINGS = ["Recommendation", "Justification", "Portfolio impact", "Uncertainty"]


def extract_decision(answer: str) -> str | None:
    matches = re.findall(r"(?im)^Recommendation:\s*(Do Not Buy|Buy|Neutral)\s*$", answer)
    return matches[0].title() if len(matches) == 1 else None


def validate_answer(answer: str, source_ids: set[str] | None = None) -> dict:
    if not isinstance(answer, str):
        raise ValueError("Model output must be text.")
    errors, sections = [], {}
    matches = list(re.finditer(r"(?im)^(Recommendation|Justification|Portfolio impact|Uncertainty):\s*", answer))
    names = [m.group(1).lower() for m in matches]
    if names != [h.lower() for h in HEADINGS]:
        errors.append("Expected exactly four sections in the requested order.")
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(answer)
        sections[match.group(1).lower()] = answer[match.end():end].strip()
    if extract_decision(answer) is None:
        errors.append("Recommendation must contain one exact allowed label.")
    if any(not sections.get(h.lower(), "") for h in HEADINGS):
        errors.append("Required sections must contain text.")
    cited = set(re.findall(r"\[source:([^\]]+)\]", answer))
    if source_ids is not None and cited - source_ids:
        errors.append("Answer cites unknown source IDs.")
    return {"valid": not errors, "errors": errors, "decision": extract_decision(answer),
            "cited_source_ids": sorted(cited),
            "scope": "Format/citation-ID checks only; factual grounding is not verified."}
