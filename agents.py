## Importing libraries and files
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, LLM
from tools import file_read_tool, search_tool

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)
# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="""Provide a detailed and data-driven analysis of a given financial document.
    Your analysis must be objective, meticulous, and based solely on the information
    present in the document.""",
    verbose=True,
    memory=True,
    backstory=(
        "With a Ph.D. in Finance and over 15 years of experience at top-tier investment banks, you are a master of financial analysis. "
        "Your expertise lies in dissecting complex financial statements, identifying key performance indicators (KPIs), and "
        "uncovering underlying trends. You are known for your precision, objectivity, and a deep understanding of market dynamics. "
        "You do not make speculative claims; every insight is backed by hard data from the report."
    ),
    tools=[file_read_tool, search_tool],
    llm=llm,
    max_iter=5, # Increased for better reasoning
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="""Ensure the provided document is a valid and relevant financial report.
    Verify the document's authenticity and check for any obvious inconsistencies or missing data.
    Your decision is final.""",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance officer with an eagle eye for detail. Your entire career has been dedicated to ensuring the integrity of financial documents. "
        "You cross-reference every piece of data and are trusted to flag any document that doesn't meet the highest standards of financial reporting. "
        "You are methodical and thorough."
    ),
    tools=[file_read_tool], # This agent only needs to read the file
    llm=llm,
    max_iter=3,
    # max_rpm=1,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Prudent Investment Advisor",
    goal="""Based on the financial analysis, develop a balanced and strategic investment recommendation.
    Your advice should consider the user's long-term goals, risk tolerance, and the overall market conditions.""",
    verbose=True,
    backstory=(
        "You are a seasoned Certified Financial Planner (CFP) with a reputation for creating sensible, diversified investment portfolios. "
        "You avoid hype and focus on sustainable, long-term growth. You translate complex financial data into clear, actionable advice, "
        "helping clients navigate the market with confidence. Your recommendations are always well-reasoned and clearly justified."
    ),
     
    tools=[search_tool],
    llm=llm,
    max_iter=5,
    # max_rpm=1,
    allow_delegation=True
)


risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",
    goal="""Identify, analyze, and quantify potential risks associated with the investment opportunity.
    Provide a detailed report on market, credit, and operational risks, along with potential mitigation strategies.""",
    verbose=True,
    backstory=(
        "As a Chartered Financial Analyst (CFA) specializing in risk management, you see what others miss. "
        "You excel at stress-testing financial models and identifying potential vulnerabilities in an investment strategy. "
        "Your job is not to predict the future, but to prepare for it by providing a clear-eyed view of all potential risks. "
        "Your reports are critical for making informed, risk-aware investment decisions."
    ),
    tools=[search_tool],
    llm=llm,
    max_iter=5,
    # max_rpm=1,
    allow_delegation=False
)
