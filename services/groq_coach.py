import json
import os

from groq import Groq

from config.prompts import COACH_SYSTEM_PROMPT
from utils.scoring import calculate_overall_score


MODEL = "openai/gpt-oss-120b"


def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return Groq(api_key=api_key)


def evaluate_response(
    profile,
    hr_message,
    candidate_response,
    round_number
):

    client = get_client()

    prompt = f"""
Evaluate this salary negotiation response.

Candidate:
- Role: {profile['role']}
- Experience: {profile['experience']} years
- Current salary: ₹{profile['current_salary']:,.0f}
- Target salary: ₹{profile['target_salary']:,.0f}
- Skills: {profile['skills']}
- Achievements: {profile['achievements']}

Round: {round_number}/5

HR said:
{hr_message}

Candidate said:
{candidate_response}

Return ONLY a JSON object with these exact fields:

confidence: integer 0-100
persuasiveness: integer 0-100
evidence: integer 0-100
communication: integer 0-100
professionalism: integer 0-100
strategy: integer 0-100
strengths: array containing 1-2 short strings
weaknesses: array containing 1-2 short strings
feedback: one short string
better_response: one short string

Keep every text field concise.
Do not include markdown.
Do not include explanations outside JSON.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": COACH_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_completion_tokens=1500,
        response_format={
            "type": "json_object"
        }
    )

    raw = response.choices[0].message.content

    try:
        result = json.loads(raw)

    except json.JSONDecodeError:

        return {
            "confidence": 0,
            "persuasiveness": 0,
            "evidence": 0,
            "communication": 0,
            "professionalism": 0,
            "strategy": 0,
            "overall": 0,
            "strengths": [
                "AI evaluation could not be parsed."
            ],
            "weaknesses": [
                "Please try the response again."
            ],
            "feedback": (
                "The AI evaluation was incomplete."
            ),
            "better_response": candidate_response
        }

    metrics = [
        "confidence",
        "persuasiveness",
        "evidence",
        "communication",
        "professionalism",
        "strategy"
    ]

    for metric in metrics:

        try:
            result[metric] = int(result.get(metric, 0))
        except (TypeError, ValueError):
            result[metric] = 0

        result[metric] = max(
            0,
            min(100, result[metric])
        )

    result["overall"] = calculate_overall_score(result)

    if not isinstance(result.get("strengths"), list):
        result["strengths"] = []

    if not isinstance(result.get("weaknesses"), list):
        result["weaknesses"] = []

    result["feedback"] = str(
        result.get("feedback", "")
    )

    result["better_response"] = str(
        result.get("better_response", candidate_response)
    )

    return result