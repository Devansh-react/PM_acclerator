from langchain.prompts import ChatPromptTemplate
from utils.logger import logger

def resolve_location(query: str, llm) -> str | None:
    """
    Uses an LLM to extract the location from user query.
    Supports:
    - City names (e.g., "New York", "Delhi NCR")
    - Postal codes (e.g., "10001")
    - Coordinates (e.g., "40.7128, -74.0060")

    Returns a normalized string that can be used by the Weather API.
    """

    prompt = ChatPromptTemplate.from_template(
        """
        You are a location extraction assistant for a weather application.

        Your task is to analyze the following user query and extract the location information in a format suitable for weather lookup:
        "{query}"

        Extraction guidelines:
        - If the query contains coordinates (latitude and longitude), return them in "lat,long" format. Accept both decimal and DMS formats, and handle negative values.
        - If the query contains a postal code, return only the postal code (digits and/or letters). Accept international formats, including ZIP, PIN, and alphanumeric codes.
        - If the query contains a city or region name, return only the clean name of the city or region, without any extra words. Remove any prefixes/suffixes like "city of", "near", "in", etc.
        - If the query contains multiple locations, return only the most relevant one for weather lookup.
        - Ignore any references to time, weather conditions, or unrelated entities.
        - Do not include any additional words such as "weather", "forecast", "temperature", or explanations.
        - Do not add punctuation, explanations, or any extra text.
        - If no location can be identified in the query, return "UNKNOWN".
        - If the query contains ambiguous or conflicting locations, return "UNKNOWN".
        - If the query contains a landmark or place name (e.g., "Eiffel Tower"), return the city or region where it is located.
        - If the query contains a country name, return only if no more specific location is present.

        Your response must be only the extracted location or "UNKNOWN".
        """
    )

    try:
        response = llm.invoke(prompt.format(query=query))
        location = response.content.strip()

        # Final cleanup
        location = location.replace("?", "").replace(".", "").strip()

        if location.upper() == "UNKNOWN":
            logger.warning("❌ Could not detect location.")
            return None

        logger.info(f"Extracted location via LLM: {location}")
        return location

    except Exception as e:
        logger.error(f"Location resolver failed: {e}")
        return None
