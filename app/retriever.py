import json
import re

# -----------------------------
# Load SHL Product Catalogue
# -----------------------------
with open("app/shl_product_catalog.json", "r", encoding="utf-8") as file:
    data = file.read()

# Remove invalid control characters
data = re.sub(r"[\x00-\x1F]+", " ", data)

catalogue = json.loads(data)


# -----------------------------------------
# Search Catalogue
# -----------------------------------------
def search_catalogue(query):

    query = query.lower()

    stop_words = {
        "i", "need", "a", "an", "the",
        "assessment", "assessments",
        "test", "tests",
        "for", "to", "want",
        "looking", "actually",
        "make", "it", "please",
        "developer", "engineer",
        "role", "experience",
        "year", "years",
        "with", "required",
        "require", "candidate",
        "skills", "skill"
    }

    keywords = [
        word
        for word in re.findall(r"\w+", query)
        if word not in stop_words
    ]

    results = []

    for item in catalogue:

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        keys = " ".join(item.get("keys", [])).lower()

        searchable = f"{name} {description} {keys}"

        score = 0

        # -------------------------
        # Technology Filters
        # -------------------------

        if "python" in keywords and "python" not in searchable:
            continue

        if "javascript" in keywords and "javascript" not in searchable:
            continue

        if "java" in keywords:
            if "javascript" in searchable:
                continue
            if "java" not in searchable:
                continue

        if "sql" in keywords and "sql" not in searchable:
            continue

        # -------------------------
        # Scoring
        # -------------------------

        for word in keywords:

            # Highest priority: exact assessment name
            if word == "python" and "python" in name:
                score += 200

            elif word == "java" and "java 8" in name:
                score += 200

            elif word == "sql" and "sql" in name:
                score += 200

            # Name
            elif word in name:
                score += 100

            # Keys
            elif word in keys:
                score += 50

            # Description
            elif word in description:
                score += 20

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in results[:10]]


# -----------------------------------------
# Find Assessment by Name
# -----------------------------------------
def find_assessment(name):

    name = name.lower().strip()

    # Exact name match
    for item in catalogue:
        if item.get("name", "").lower() == name:
            return item

    # Contains full phrase
    for item in catalogue:
        if name in item.get("name", "").lower():
            return item

    # Best word match
    best_match = None
    best_score = 0

    words = re.findall(r"\w+", name)

    for item in catalogue:

        assessment_name = item.get("name", "").lower()

        score = 0

        for word in words:
            if word in assessment_name:
                score += 10

        if score > best_score:
            best_score = score
            best_match = item

    return best_match