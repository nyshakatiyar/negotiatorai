import os

from groq import Groq

from config.prompts import HR_SYSTEM_PROMPT
from utils.scoring import difficulty_description


MODEL = "openai/gpt-oss-120b"


def get_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return Groq(api_key=api_key)


def generate_hr_response(
    profile,
    conversation,
    round_number,
    current_offer,
    difficulty
):

    client = get_client()

    conversation_messages = []

    for message in conversation:

        role = (
            "assistant"
            if message["role"] == "hr"
            else "user"
        )

        conversation_messages.append(
            {
                "role": role,
                "content": message["content"]
            }
        )

    context = f"""
Candidate Profile:

Name: {profile['name']}
Role: {profile['role']}
Experience: {profile['experience']} years

Current Salary:
₹{profile['current_salary']:,.0f}

Target Salary:
₹{profile['target_salary']:,.0f}

Minimum Acceptable Salary:
₹{profile['minimum_salary']:,.0f}

Skills:
{profile['skills']}

Achievements:
{profile['achievements']}

Company Type:
{profile['company_type']}

Negotiation Round:
{round_number}/5

Current Offer:
₹{current_offer:,.0f}

HR Difficulty:
{difficulty}/5

Difficulty:
{difficulty_description(difficulty)}
"""

    messages = [
        {
            "role": "system",
            "content": HR_SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": context
        }
    ]

    messages.extend(conversation_messages)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()