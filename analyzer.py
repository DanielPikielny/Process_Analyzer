from openai import OpenAI
from schema import (
    StepsOutput,
    InefficienciesOutput,
    AutomationsOutput,
    ToolsOutput,
    CostEstimatesOutput,
    ProcessStepItem,
    InefficiencyItem,
    AutomationItem,
    ToolItem,
    CostEstimateItem,
    validate_output,
)
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _call_llm_structured(system_prompt: str, user_content: str, schema):
    """
    Shared helper: calls the OpenAI API with structured output enforcement.
    Returns a parsed Pydantic object, or None on failure.
    """
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            response_format=schema,
        )
        return response.choices[0].message.parsed
    except Exception as e:
        logger.error(f"[{schema.__name__}] OpenAI structured output call failed: {e}")
        return None


def _items_to_json(items: list) -> str:
    """Serialize a list of Pydantic items to a JSON string for use in prompts."""
    return json.dumps([item.model_dump() for item in items], indent=2)

def extract_steps(text: str) -> list[ProcessStepItem] | None:
    """Extract sequential process steps with confidence scores and explanations."""
    system = (
        "You are a business process analyst. "
        "Read the workflow description and extract each clear, sequential step. "
        "For each step, provide a confidence score (0.0–1.0) reflecting how certain "
        "you are it represents a real step, and a brief explanation of why it exists."
    )
    result = _call_llm_structured(system, text, StepsOutput)
    if result is None:
        return None
    return result.process_steps

def find_inefficiencies(steps: list[ProcessStepItem]) -> list[InefficiencyItem] | None:
    """Identify inefficiencies with impact rating, confidence score, and explanation."""
    system = (
        "You are a business process analyst specializing in identifying inefficiencies. "
        "Given a list of process steps, identify specific bottlenecks, manual pain points, "
        "or risks. For each, provide an impact level (low/medium/high), a confidence score "
        "(0.0–1.0), and a brief explanation of why the inefficiency exists and how it manifests."
    )
    user = f"Process steps:\n{_items_to_json(steps)}"
    result = _call_llm_structured(system, user, InefficienciesOutput)
    if result is None:
        return None
    return result.inefficiencies

def suggest_automations(
    steps: list[ProcessStepItem],
    inefficiencies: list[InefficiencyItem],
) -> list[AutomationItem] | None:
    """Suggest automation opportunities with confidence scores and explanations."""
    system = (
        "You are an automation consultant. "
        "Given a list of process steps and their inefficiencies, suggest concrete automation "
        "opportunities. For each, provide a confidence score (0.0–1.0) for feasibility and "
        "a brief explanation of why it would help and which inefficiency it addresses."
    )
    user = (
        f"Process steps:\n{_items_to_json(steps)}\n\n"
        f"Inefficiencies:\n{_items_to_json(inefficiencies)}"
    )
    result = _call_llm_structured(system, user, AutomationsOutput)
    if result is None:
        return None
    return result.automation_opportunities

def suggest_tools(automations: list[AutomationItem]) -> list[ToolItem] | None:
    """Recommend tools with confidence scores and explanations."""
    system = (
        "You are a software tools expert. "
        "Given a list of automation opportunities, recommend specific software tools or platforms. "
        "For each, provide a confidence score (0.0–1.0) for how well it fits and a brief "
        "explanation of why it is recommended and what it covers."
    )
    user = f"Automation opportunities:\n{_items_to_json(automations)}"
    result = _call_llm_structured(system, user, ToolsOutput)
    if result is None:
        return None
    return result.suggested_tools

def estimate_costs(
    automations: list[AutomationItem],
    tools: list[ToolItem],
) -> list[CostEstimateItem] | None:
    """Estimate rough implementation costs for automations and tools."""
    system = (
        "You are a business technology consultant with expertise in software pricing. "
        "Given a list of automation opportunities and recommended tools, provide rough cost "
        "estimates for each. Estimates can be monetary (e.g. '$20/month', 'Free tier available') "
        "or effort-based (e.g. '2–4 dev days'). Include brief notes on what drives the cost "
        "and any important caveats or assumptions."
    )
    user = (
        f"Automation opportunities:\n{_items_to_json(automations)}\n\n"
        f"Suggested tools:\n{_items_to_json(tools)}"
    )
    result = _call_llm_structured(system, user, CostEstimatesOutput)
    if result is None:
        return None
    return result.cost_estimates

def analyze_process(text: str) -> dict:
    """
    Run the full multi-step structured analysis pipeline:
      1. Extract process steps
      2. Find inefficiencies
      3. Suggest automations
      4. Suggest tools
      5. Estimate costs
    Returns a validated result dict, or a dict with an "error" key on failure.
    """
    steps = extract_steps(text)
    if steps is None:
        return {"error": "Failed to extract process steps."}

    inefficiencies = find_inefficiencies(steps)
    if inefficiencies is None:
        return {"error": "Failed to identify inefficiencies."}

    automations = suggest_automations(steps, inefficiencies)
    if automations is None:
        return {"error": "Failed to suggest automations."}

    tools = suggest_tools(automations)
    if tools is None:
        return {"error": "Failed to suggest tools."}

    costs = estimate_costs(automations, tools)
    if costs is None:
        return {"error": "Failed to estimate costs."}

    result = {
        "process_steps": steps,
        "inefficiencies": inefficiencies,
        "automation_opportunities": automations,
        "suggested_tools": tools,
        "cost_estimates": costs,
    }

    if not validate_output(result):
        logger.error(f"Pipeline output failed final validation: {list(result.keys())}")
        return {"error": "Pipeline produced an incomplete result."}

    return result
