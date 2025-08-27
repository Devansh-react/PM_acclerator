import re

def resolve_location(query: str) -> str | None:
    """
    Extract a location string from the user query.
    Currently supports:
    - 5-digit ZIP codes
    - City names (naive fallback)
    """

    if not query:
        return None

    # Try to detect US ZIP Code
    zip_match = re.search(r"\b\d{5}\b", query)
    if zip_match:
        return zip_match.group(0)

    # Naive: take last capitalized word as city
    tokens = query.strip().split()
    for word in reversed(tokens):
        if word[0].isupper():
            return word

    # fallback: last word
    return tokens[-1] if tokens else None
