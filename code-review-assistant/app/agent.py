# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.cloud import firestore
from google.genai import types


MODEL = "gemini-3.6-flash"

# HARDCODED GCP PROJECT ID for Agent Platform compatibility
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-04-71f8c49abd0b"
firestore_db = firestore.Client(project=FIRESTORE_PROJECT_ID)
FIRESTORE_COLLECTION = "code_reviews"


def search_code_reviews(repo: str = "", status: str = "") -> list[dict]:
    """Searches code reviews in the Firestore database by repository name or status.

    Args:
        repo: Optional repository name to filter by (e.g., 'core-auth-service').
        status: Optional status to filter by ('APPROVED', 'CHANGES_REQUESTED', 'PENDING').

    Returns:
        A list of code review dictionaries matching the query parameters.
    """
    collection_ref = firestore_db.collection(FIRESTORE_COLLECTION)
    docs = collection_ref.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        if repo and repo.lower() not in data.get("repo", "").lower():
            continue
        if status and status.upper() != data.get("status", "").upper():
            continue
        results.append(data)
    return results


def get_code_review_details(review_id: str) -> dict:
    """Retrieves a specific code review record from Firestore by its review ID.

    Args:
        review_id: The unique code review identifier (e.g. 'CR-101').

    Returns:
        A dictionary containing the code review record details.
    """
    doc_ref = firestore_db.collection(FIRESTORE_COLLECTION).document(review_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Code review '{review_id}' not found."}


def save_code_review(
    review_id: str,
    repo: str,
    pr_title: str,
    status: str,
    author: str,
    missing_details: list[str] = None,
    security_issues: list[str] = None,
) -> str:
    """Saves or updates a code review record in the Firestore database.

    Args:
        review_id: Unique code review identifier (e.g., 'CR-105').
        repo: Repository name (e.g., 'core-auth-service').
        pr_title: Pull request title.
        status: Review status ('APPROVED', 'CHANGES_REQUESTED', 'PENDING').
        author: Username of PR author.
        missing_details: List of missing details (e.g., missing docstrings, missing type hints).
        security_issues: List of security vulnerabilities or risks found.

    Returns:
        A confirmation string indicating the record was saved.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {
        "review_id": review_id,
        "repo": repo,
        "pr_title": pr_title,
        "status": status.upper(),
        "author": author,
        "missing_details": missing_details or [],
        "security_issues": security_issues or [],
        "created_at": now_iso,
    }
    doc_ref = firestore_db.collection(FIRESTORE_COLLECTION).document(review_id)
    doc_ref.set(record)
    return f"Successfully saved code review '{review_id}' to Firestore."


RAG_CORPUS_NAME = "projects/977430187658/locations/us-central1/ragCorpora/7554832355379118080"


def consult_pr_guidelines(query: str) -> str:
    """Searches the official code review & PR guidelines corpus for relevant guidelines and standards.

    Args:
        query: What to look up in the code review guidelines (e.g. 'type hints', 'docstrings', 'PR review checklist', 'security requirements').

    Returns:
        The matched passages from the code review guidelines corpus.
    """
    import vertexai
    from vertexai.preview import rag

    try:
        vertexai.init(project="qwiklabs-gcp-04-71f8c49abd0b", location="us-central1")
        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=RAG_CORPUS_NAME)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=5),
        )
        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]
        return "\n\n---\n\n".join(passages) or "No relevant guidelines found."
    except Exception as e:
        return f"Retrieval failed: {e}"


def run_linter_check(code_snippet: str) -> dict:
    """Runs static linting checks on a Python code snippet to catch missing details.

    Inspects code for missing function docstrings, missing return type annotations,
    and security anti-patterns (such as hardcoded secrets or unsafe eval/exec calls).

    Args:
        code_snippet: The Python source code string to analyze.

    Returns:
        A dictionary containing missing type hints, missing docstrings, security risks,
        and an overall compliance status.
    """
    missing_type_hints = []
    missing_docstrings = []
    security_risks = []

    lines = code_snippet.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def ") and "(" in stripped and ")" in stripped:
            func_name = stripped.split("def ")[1].split("(")[0].strip()
            if "->" not in stripped:
                missing_type_hints.append(f"Function '{func_name}' is missing return type hint.")
            if ":" in stripped and not ('"""' in code_snippet or "'''" in code_snippet):
                missing_docstrings.append(f"Function '{func_name}' is missing Google-style docstring.")

        if "eval(" in stripped or "exec(" in stripped:
            security_risks.append("Security risk: Use of dynamic execution (eval/exec) detected.")
        if "SELECT" in stripped and "+" in stripped:
            security_risks.append("Security risk: Potential SQL injection via string concatenation.")

    total_issues = len(missing_type_hints) + len(missing_docstrings) + len(security_risks)
    status = "PASSED" if total_issues == 0 else "ACTION_REQUIRED"

    return {
        "status": status,
        "missing_type_hints": missing_type_hints,
        "missing_docstrings": missing_docstrings,
        "security_risks": security_risks,
        "total_issues_found": total_issues,
    }


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_secret_agent_id() -> str:
    """Returns the unique local agent proof token ID.

    Returns:
        A unique token string proving this local agent code is running.
    """
    return "PROOF-TOKEN-LOCAL-SIMPLE-AGENT-99482"


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    q = query.lower()
    if "sf" in q or "san francisco" in q:
        tz_identifier = "America/Los_Angeles"
    elif "bombay" in q or "mumbai" in q or "india" in q:
        tz_identifier = "Asia/Kolkata"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')} (Local Agent Proof Token: PROOF-TOKEN-LOCAL-SIMPLE-AGENT-99482)"


async def generate_memories_callback(callback_context: CallbackContext):
    """Callback to extract memories from session at end of turn."""
    await callback_context.add_session_to_memory()
    return None


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an expert Code Review & Pull Request Assistant. "
        "Your mission is to remember and enforce ALL team preferences, coding standards, "
        "and missing code review details across sessions.\n\n"
        "Memory & Review Rules:\n"
        "1. Automatically recall preloaded user memories regarding coding standards, preferred docstring formats, type hint rules, test requirements, and security guidelines.\n"
        "2. If needed, use LoadMemoryTool to query past memory for specific code review details or team conventions.\n"
        "3. You have access to Firestore tools (search_code_reviews, get_code_review_details, save_code_review) to inspect and persist code review records.\n"
        "4. You can call run_linter_check to perform static analysis on Python code snippets.\n"
        "5. You can call consult_pr_guidelines to retrieve official code review & pull request guidelines.\n"
        "6. When reviewing code, explicitly inspect and report ALL missing details:\n"
        "   - Missing type hints or annotations\n"
        "   - Missing or incomplete docstrings (Google-style)\n"
        "   - Missing unit tests or edge case handling\n"
        "   - Security risks (SQL injection, hardcoded secrets, unsafe input)\n"
        "   - Performance bottlenecks and style guide violations\n"
        "7. Explicitly state any newly noted preferences or missing review rules so they are captured into long-term Memory Bank.\n"
        "8. When opening or posting new PRs, ALWAYS include line-level inline annotations across all code diffs and Checks tab runs for all code issues by default, explaining the engineering reasoning for each fix."
    ),
    tools=[
        PreloadMemoryTool(),
        LoadMemoryTool(),
        search_code_reviews,
        get_code_review_details,
        save_code_review,
        run_linter_check,
        consult_pr_guidelines,
        get_weather,
        get_current_time,
        get_secret_agent_id,
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)





