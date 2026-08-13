# My agent: Code Review & Pull Request Assistant
One-liner: A conversational agent that helps developers review code diffs, enforce team style guides, and catch security vulnerabilities with structured PR review cards.

Tool coverage:
- Memory: Remembers team coding standards, repository architecture preferences, and recurring PR feedback
- Tools: Parses git diffs, checks style guide compliance, flags security vulnerabilities, and generates review summaries
- Catalog/UI: Renders PR review summary cards and issue severity tables
- Image gen: Generates visual architecture diagrams or code flowcharts for PR changes
- Sandbox: Executes code snippets, calculates complexity metrics, or runs linters

Core rails (everyone): memory, tools, eval, deploy, frontend
My stretch menu (pick later): A2UI review cards/tables, code complexity sandbox calculations, architecture diagram generation
First eval question: "Review this PR diff for security vulnerabilities, style compliance, and performance bottlenecks: `def login(user, pwd): db.execute('SELECT * FROM users WHERE u=' + user)`"
