import re

# https://learn.microsoft.com/en-us/purview/sit-defn-us-social-security-number
keywords = [
    "SSA Number",
    "social security number",
    "social security #",
    "social security#",
    "social security no",
    "Social Security#",
    "Soc Sec",
    "SSN",
    "SSNS",
    "SSN#",
    "SS#",
    "SSID"]


# This function:
# 1. Finds all instances of SSN-like strings
# 2. Looks for keywords within 300 characters of the SSN-like string
# 3. Outputs a dictionary where the key is the SSN and keywords and confidence
#    are values (high confidence for keyword present and low for not present)
def find_ssns(text, id, path):
    pattern = r'\d{3}[-\s]?\d{2}[-\s]?\d{4}'
    matches = list(re.finditer(pattern, text))

    if not matches:
        return {}, id

    text_lower = text.lower()
    # todo: make all the keywords lowercase already to save time
    keywords_lower = [k.lower() for k in keywords]
    processed_matches = {}

    for i, match in enumerate(matches):
        start = max(match.start() - 150, 0)
        end = min(match.end() + 150, len(text))
        surrounding = text_lower[start:end]

        found_keyword = next(
            (k for k in keywords_lower if k in surrounding),
            None
        )

        processed_matches[f"match_{id}"] = {
            "ssn": match.group(),
            "keyword": found_keyword,
            "confidence": "high" if found_keyword else "low",
            "context": text[start:end],
            "path": str(path)
        }

        id += 1

    return processed_matches, id
