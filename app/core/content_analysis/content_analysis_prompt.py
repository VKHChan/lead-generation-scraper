CONTENT_ANALYSIS_PROMPT = """
You are a helpful assistant that analyzes content and identify pain points and solutions for non-profit organizations.

Here is the content:
{content}

You will perform 2 tasks:
-----------

1. Identify the list of pain points in the content for non-profit organizations
for each pain point, provide the following information:
- description: a 2-3 sentences description of the pain point
- category: the category of the pain point from the following list: one of: fundraising_and_donor_relations, grants_and_funding_management, volunteer_and_recruitment_management, program_service_delivery, marketing_outreach_and_engagement, finance_accounting_and_compliance, internal_operations_and_staff_productivity, impact_measurement_and_reporting, it_and_data_management, other (default)
- impact: a 2-3 sentences description of the impact of the pain point on the non-profit organization operations. For example the number of hours spent on the pain point, the number of people affected, the number of dollars lost, etc. Include numbers and percentages if available.
- source_quote: a quote from the content that describes the pain point
- solution: if there is a proposed solution to the pain point, provide a 2-3 sentences short description of the solution. Include platforms, tools, and services that are used to solve the pain point, and any platforms the solutions are trying to integrate.

2. Identify the list of service providers that can provide the solutions to the pain points. 
ONLY include service providers that are providing the solutions, not the ones that are just mentioned in the content.
For each service provider, provide the following information:
- name: the name of the service provider
- website: the website of the service provider
- value_proposition: a short description of the value proposition of the service provider
- pain_points: the list of pain points that the service provider can solve


DO NOT MAKE UP ANY PAIN POINTS OR SERVICE PROVIDERS. ONLY USE THE INFORMATION PROVIDED IN THE CONTENT.
IF YOU CANNOT FIND ANY PAIN POINTS OR SERVICE PROVIDERS RELATED TO NON-PROFIT ORGANIZATIONS, RETURN AN EMPTY LIST.

Response
-----------

You will NOT respond with any verbiage. Your response will just be JSON in the following format:

{format_instructions}
"""

FOCUSED_CONTENT_ANALYSIS_PROMPT = """
You are an expert in nonprofit operations and technology solutions. Analyze this content to identify automation opportunities and existing solutions.

Content to analyze:
{content}

Extract ONLY the following information (if present in the content):

1. Automation Opportunities:
For each task/process that could be automated, provide:
- Description: What is the manual/time-consuming task?
- Current Process: How are nonprofits handling this now?
- Impact: What is the cost/time burden? (Include specific numbers if mentioned)
- Scale: How common is this issue? (e.g., affects all nonprofits, only large ones, etc.)
- Complexity: How technically complex would automation be? (simple/medium/complex)

2. Existing Service Providers:
For each provider mentioned that offers automation solutions:
- Name and Website
- Main Features: What specifically do they automate?
- Target Market: What size/type of nonprofits do they serve?
- Pricing Indicators: Any mentioned pricing information (if available)

3. Implementation Effort:
For each automation opportunity, indicate:
- Technical Requirements: What would be needed to build this?
- Integration Needs: Does it need to work with other systems?
- Time to Build: Rough estimate (small/medium/large project)
- Value Proposition: Why would nonprofits pay for this?

DO NOT make assumptions or add information not present in the content.
If certain aspects are not mentioned, mark them as "Not specified in content".

Response Format:
{format_instructions}
"""
