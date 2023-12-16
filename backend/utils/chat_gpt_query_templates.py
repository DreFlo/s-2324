import json

def get_explain_company_prediction_query(prediction : dict, style : str) -> str:
    query = """
SECTION - INSTRUCTIONS:
    - You will generate text based on prediction data.
    - This text will be used to explain the prediction.
    - The text must explain the prediction in a way that is easy to understand.
    - The text must be in English.
    - The text must be formatted in paragraphs.
    - The text must be written out in full sentences.
    - Do not use bullet points.
    - The text must be written in the following style: %s
    - All of the prediction datapoints must be present in the text you generate.
    - The text must contain all of the contents specified in SECTION - TEXT CONTENTS, in the order they are specified.
    - The prediction data is in SECTION - DATA, it is in JSON format.

SECTION - DATA:
%s

SECTION - TEXT CONTENTS:
    - The name followed by the symbol in brackets.
    - What we recommend the user do, this is the recommendation.
    - The probability of the stock price going up, this is the probability.
    - The supporting features, include the feature name (separate the words with spaces) and the value.
    - The detracting features, include the feature name (separate the words with spaces) and the value.
""" % (style, json.dumps(prediction, indent=4))

    return query