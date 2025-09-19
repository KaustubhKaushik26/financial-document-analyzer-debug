## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor

# Task 1: Verify the financial document
verification = Task(
  description="""Verify that the document at the given file path, '{file_path}', is a legitimate financial report.
  Check for standard financial sections like 'Income Statement', 'Balance Sheet', and 'Cash Flow Statement'.
  If the document is not a valid financial report, you MUST stop the entire process immediately and report the issue.""",
  expected_output="A confirmation that the document is a valid financial report or an error message if it is not.",
  agent=verifier
)

# Task 2: Analyze the financial document
analyze_financial_document = Task(
    description="""Analyze the financial document at '{file_path}' in detail.
    Extract key financial metrics, such as revenue, profit margins, and cash flow.
    Identify major trends, growth drivers, and potential areas of concern.
    Your analysis should be comprehensive and based exclusively on the data in the document.
    The user has the following query: {query}""",

    expected_output="""A detailed, multi-paragraph financial analysis report formatted in markdown.
  The report should include sections for Key Metrics, Trends, and a Concluding Summary.""",
    agent=financial_analyst,
    context=[verification] # This task depends on the verification task
)

# Task 3: Assess risks based on the analysis
risk_assessment = Task(
  description="""Based on the financial analysis, conduct a thorough risk assessment.
  Identify potential market, credit, and operational risks.
  Use the search tool to find current market conditions and assess how they might impact the company's financial health.""",
  expected_output="""A markdown report detailing potential risks, categorized by type (Market, Credit, Operational).
  For each risk, provide a brief explanation and a potential mitigation strategy.""",
  agent=risk_assessor,
  context=[analyze_financial_document] # This task depends on the financial analysis
)

# Task 4: Provide investment recommendation
investment_analysis = Task(
    description="""Synthesize the financial analysis and risk assessment to provide a comprehensive investment recommendation.
    Your recommendation should be balanced, considering both the potential upside and the identified risks.
    Address the original user query: {query}""",
    
    expected_output="""A final, client-ready investment report in markdown format.
    It should include:
    1. A summary of the financial analysis.
    2. A summary of the key risks.
    3. A clear investment recommendation (e.g., Buy, Hold, Sell).
    4. Justification for the recommendation, citing specific data points from the analysis.""",

    agent=investment_advisor,
    context=[analyze_financial_document, risk_assessment] # This task uses the results of the previous two
)