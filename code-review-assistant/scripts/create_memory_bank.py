import os
import vertexai

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-71f8c49abd0b")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-east1")

print(f"Creating Memory Bank in project={PROJECT_ID}, location={LOCATION}...")
client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

memory_bank = client.agent_engines.create()

resource_name = memory_bank.api_resource.name
memory_bank_id = resource_name.split("/")[-1]
print("MEMORY_BANK_ID:", memory_bank_id)
print("Resource name:", resource_name)
