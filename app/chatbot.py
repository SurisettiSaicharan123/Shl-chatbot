from app.retriever import search_catalogue, find_assessment


def chat(messages):

    # -----------------------------------
    # Get ONLY the latest user message
    # -----------------------------------
    conversation = ""

    for msg in reversed(messages):
        if msg["role"] == "user":
            conversation = msg["content"].strip().lower()
            break

    print("LATEST USER MESSAGE:", conversation)

    # -----------------------------------
    # Ask clarifying question
    # -----------------------------------
    if (
        "assessment" in conversation
        and not any(
            word in conversation
            for word in [
                "java",
                "python",
                "sql",
                "javascript",
                "developer",
                "engineer",
                "analyst",
                "manager",
                "experience",
                "year",
                "spring",
                "react",
                "aws"
            ]
        )
    ):
        return {
            "reply": "Sure, I can help. Could you tell me the job role, required skills, and experience level?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # Compare Assessments
    # -----------------------------------
    if conversation.startswith("compare"):

        text = conversation.replace("compare", "", 1).strip()

        parts = text.split(" and ")

        if len(parts) != 2:
            return {
                "reply": "Please specify two assessment names.\nExample: Compare Python (New) and Java 8",
                "recommendations": [],
                "end_of_conversation": True
            }

        first = find_assessment(parts[0].strip())
        second = find_assessment(parts[1].strip())

        if not first or not second:
            return {
                "reply": "I couldn't find one or both assessments.",
                "recommendations": [],
                "end_of_conversation": True
            }

        return {
            "reply": f"""Comparison of SHL Assessments

1. {first.get("name","")}
Type: {", ".join(first.get("keys", []))}
Description: {first.get("description","")}

2. {second.get("name","")}
Type: {", ".join(second.get("keys", []))}
Description: {second.get("description","")}
""",
            "recommendations": [
                {
                    "name": first.get("name", ""),
                    "url": first.get("link", ""),
                    "test_type": ", ".join(first.get("keys", []))
                },
                {
                    "name": second.get("name", ""),
                    "url": second.get("link", ""),
                    "test_type": ", ".join(second.get("keys", []))
                }
            ],
            "end_of_conversation": True
        }

    # -----------------------------------
    # Normal Recommendation
    # -----------------------------------
    results = search_catalogue(conversation)

    if not results:
        return {
            "reply": "Sorry, I couldn't find matching SHL assessments.",
            "recommendations": [],
            "end_of_conversation": True
        }

    recommendations = []

    for item in results:
        recommendations.append(
            {
                "name": item.get("name", ""),
                "url": item.get("link", ""),
                "test_type": ", ".join(item.get("keys", []))
            }
        )

    return {
        "reply": "Here are SHL assessments matching your requirements.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }
