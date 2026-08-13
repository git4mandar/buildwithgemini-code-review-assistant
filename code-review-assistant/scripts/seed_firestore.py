from google.cloud import firestore

# HARDCODED GCP PROJECT ID (Do NOT use GOOGLE_CLOUD_PROJECT or google.auth.default())
PROJECT_ID = "qwiklabs-gcp-04-71f8c49abd0b"

db = firestore.Client(project=PROJECT_ID)

COLLECTION_NAME = "code_reviews"

SEED_DATA = [
    {
        "review_id": "CR-101",
        "repo": "core-auth-service",
        "pr_title": "Implement JWT token refresh mechanism",
        "author": "alice_dev",
        "status": "CHANGES_REQUESTED",
        "missing_details": [
            "Missing Google-style docstrings in token_utils.py",
            "Missing type hints for refresh_token signature",
        ],
        "security_issues": [
            "JWT secret fallback stored in plain text string",
        ],
        "created_at": "2026-08-10T14:20:00Z",
    },
    {
        "review_id": "CR-102",
        "repo": "payment-gateway",
        "pr_title": "Add Stripe webhook signature validation",
        "author": "bob_engineer",
        "status": "APPROVED",
        "missing_details": [],
        "security_issues": [],
        "created_at": "2026-08-11T09:15:00Z",
    },
    {
        "review_id": "CR-103",
        "repo": "user-dashboard",
        "pr_title": "Refactor user profile query and export",
        "author": "charlie_ui",
        "status": "PENDING",
        "missing_details": [
            "Missing unit tests for export_user_data()",
            "Docstrings missing return type description",
        ],
        "security_issues": [
            "Unsanitized SQL query parameter in user search filter",
        ],
        "created_at": "2026-08-12T16:45:00Z",
    },
    {
        "review_id": "CR-104",
        "repo": "core-auth-service",
        "pr_title": "Add OAuth2 password grant rate limiter",
        "author": "alice_dev",
        "status": "APPROVED",
        "missing_details": [],
        "security_issues": [],
        "created_at": "2026-08-13T10:00:00Z",
    },
]

def seed():
    print(f"Seeding Firestore collection '{COLLECTION_NAME}' in project '{PROJECT_ID}'...")
    collection_ref = db.collection(COLLECTION_NAME)
    for item in SEED_DATA:
        doc_ref = collection_ref.document(item["review_id"])
        doc_ref.set(item)
        print(f"  ✓ Seeded document: {item['review_id']} ({item['pr_title']})")
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
