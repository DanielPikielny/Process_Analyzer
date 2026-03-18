REQUIRED_FIELDS = [
    "process_steps",
    "inefficiencies",
    "automation_opportunities",
    "suggested_tools"
]

def validate_output(data):
    for field in REQUIRED_FIELDS:
        if field not in data:
            return False
    return True