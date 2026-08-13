# Python Code Review & Pull Request Guidelines

A successful Python Pull Request (PR) and code review process balances automated enforcement with meaningful human feedback. High-performing teams separate the "robot work" (formatting, linting) from the "human work" (architecture, security, edge cases).

The following guidelines break down how to structure PR descriptions and what specific items to look for during a Python-focused review.

---

## Part 1: PR Author Guidelines (Writing the PR)

A great PR description saves the reviewer time and reduces the back-and-forth communication loop. Authors should structure their PRs using a standard template containing these core elements:

* **The "Why" First:** Start with a 2-3 sentence summary of the business goal or the bug being fixed. Do not just say what changed—explain why it matters.
* **Context Links:** Explicitly link to the relevant ticketing system (e.g., Jira, GitHub Issues) or technical specification document.
* **Scope and Size:** Keep the code delta small, ideally under 400 lines of code. If a change is massive, split it into sequential, stacked PRs to prevent reviewer fatigue.
* **Testing Protocol:** Detail exactly how the changes were verified. List the specific pytest or unittest commands run, and attach logs or screenshots for visual frontend/API response changes.
* **Self-Review Check:** Before assigning reviewers, the author must open their own diff on the platform, check for accidental debugging remnants (like print() statements or commented-out code), and leave clarifying comments on non-obvious algorithms.
* **Mandatory Inline & Checks Tab Annotations:** By default, every new PR must include line-level inline annotations across all code diffs and Checks tab runs for all code issues, security fixes, and architectural refactorings, explicitly detailing the engineering rationale behind each change.

---

## Part 2: PR Reviewer Checklist (Python-Specific Technical Focus)

Reviewers should ignore basic syntax spacing and instead focus on Pythonic architecture, security, and performance. 

### 1. Delegation to Automation (The Baseline)
If these criteria fail, the review should stop immediately until CI/CD pipelines turn green.
* **Formatting Check:** Do not argue about spaces, quotes, or line wraps. Ensure automated formatters like Black or Ruff have successfully run via pre-commit hooks.
* **Static Analysis:** Verify that linters like Flake8 or Pylint have passed with zero warnings.
* **Type Hint Accuracy:** Ensure Mypy or Microsoft's Pyright static type checkers run successfully against the new code.
* **Checks Tab & Inline Annotations:** Ensure all automated checks and code issues feature inline line-level annotations on the Checks tab / diff view explaining the engineering rationale behind every fix.

### 2. Pythonic Idioms & Style
Ensure the code honors PEP 8 standards and community best practices.
* **Naming Conventions:** Check that functions, variables, and modules use snake_case. Ensure classes use PascalCase and constants use UPPER_CASE.
* **Avoid Anti-Patterns:** Watch out for the dangerous `except: pass` block. Require specific exceptions (e.g., `except KeyError:`) to avoid swallowing critical errors.
* **Mutable Defaults:** Flag functions that use mutable structures as default arguments, like `def append_to(element, target=[]):`. These should always be replaced with `target=None` and initialized inside the function.
* **Context Managers:** Mandate the use of `with open(...) as f:` statements for file handling and socket connections to guarantee proper resource cleanup.

### 3. Performance & Resource Management
Look out for common bottlenecks native to Python data structures.
* **Membership Testing:** Check if lookup operations are happening inside large lists. If ordering does not matter, push authors to convert lists to sets (O(1) vs O(n) time complexity).
* **String Concatenation:** Ensure loops building text strings use `''.join(list_of_strings)` instead of repeated `+` operators, which trigger excessive memory reallocations.
* **Generator Usage:** For processing massive datasets or files, confirm the code uses generators (`yield`) or generator expressions rather than loading entire lists into RAM.

### 4. Security & Robustness
* **Secrets Exposure:** Audit the diff to make sure no hardcoded API keys, passwords, or tokens are committed. Force the use of environment variables parsed via tools like python-dotenv.
* **SQL Injection Prevention:** Confirm all database interactions utilize parameterized queries or an ORM like SQLAlchemy instead of raw f-strings.

---

## Part 3: Feedback & Communication Guidelines

The tone of a code review directly impacts team velocity and psychological safety. 

* **Comment the Code, Not the Person**
  * Bad Example: "You forgot to close this connection."
  * Good Example: "This database connection isn't wrapped in a context manager, which could leak resources."

* **Ask Questions Over Giving Orders**
  * Bad Example: "Change this to a dictionary lookup."
  * Good Example: "Would using a dictionary lookup here improve the time complexity for large sets?"

* **Differentiate Nitpicks**
  * Bad Example: "Rename this variable to total_user_count."
  * Good Example: "**Nit:** Rename this to total_user_count for consistency, but not a blocker for approval."

* **Praise Good Work**
  * Bad Example: *(Silence on clean code)*
  * Good Example: "This refactor is incredibly clean and easy to follow. Great work here!"
