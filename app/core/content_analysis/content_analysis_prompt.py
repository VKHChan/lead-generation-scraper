CONTENT_ANALYSIS_PROMPT = """
You are a helpful assistant that analyzes content and identify pain points and solutions for non-profit organizations.

Here is the content:
{content}

You will perform 2 tasks:
-----------

1. Identify the list of pain points in the content for non-profit organizations
for each pain point, provide the following information:
- description: a short description of the pain point
- category: the category of the pain point
- impact: the impact of the pain point on the non-profit organization operations
- source_quote: a quote from the content that describes the pain point
- solution: if there is a proposed solution to the pain point, provide a short description of the solution

2. Identify the list of service providers that can provide the solutions to the pain points
for each service provider, provide the following information:
- name: the name of the service provider
- website: the website of the service provider
- value_proposition: a short description of the value proposition of the service provider
- pain_points: the list of pain points that the service provider can solve

Response
-----------

You will NOT respond with any verbiage. Your response will just be JSON in the following format:

{format_instructions}
"""
