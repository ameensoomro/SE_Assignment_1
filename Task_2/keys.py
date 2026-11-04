
import secrets
import json

# Generate three unique API keys
keys = {
    "Consumer_1": secrets.token_urlsafe(32),
    "Consumer_2": secrets.token_urlsafe(32),
    "Consumer_3": secrets.token_urlsafe(32)
}

# Save keys locally
with open("Task_2/api_keys.json", "w") as file:
    json.dump(keys, file, indent=4)

print("Three API keys generated successfully!")
print(json.dumps(keys, indent=4))