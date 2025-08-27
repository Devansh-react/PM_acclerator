from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

def build_intent_classifier(llm):
    """
    Classifies user query intent.
    Returns: "weather" | "smalltalk" | "other"
    """
    prompt = """
    You are an intent classifier.
    Decide the intent of this query: "{query}".
    Valid intents: weather, smalltalk, other.
    Respond with only one word, exactly matching one of the valid intents.
    Do not explain, repeat, or add anything else.
    If unsure, respond with "other".
    """
    prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(llm=llm, prompt=prompt, output_parser=StrOutputParser())
    return chain

def classify_intent(query: str, llm) -> str:
    chain = build_intent_classifier(llm)
    intent = chain.run({"query": query})
    return intent.strip().lower()
