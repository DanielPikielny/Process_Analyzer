from pydantic import BaseModel, Field
from typing import Literal

class ProcessStepItem(BaseModel):
    description: str = Field(description="The process step as a clear, concise action.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 that this is a real step in the workflow.")
    explanation: str = Field(description="Brief explanation of why this step exists in the process.")


class InefficiencyItem(BaseModel):
    description: str = Field(description="A specific bottleneck, manual pain point, or risk.")
    impact: Literal["low", "medium", "high"] = Field(description="The estimated impact level of this inefficiency on the process.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 that this is a genuine inefficiency.")
    explanation: str = Field(description="Brief explanation of why this inefficiency exists and how it manifests.")


class AutomationItem(BaseModel):
    description: str = Field(description="A concrete automation opportunity.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 that this automation is feasible.")
    explanation: str = Field(description="Brief explanation of why this automation would help and which inefficiency it addresses.")


class ToolItem(BaseModel):
    name: str = Field(description="Name of the software tool or platform.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 that this tool is a good fit.")
    explanation: str = Field(description="Brief explanation of why this tool is recommended and what it covers.")


class CostEstimateItem(BaseModel):
    item: str = Field(description="The automation or tool being estimated.")
    estimate: str = Field(description="Rough cost estimate, e.g. '$20/month', '2–4 dev days', 'Free tier available'.")
    notes: str = Field(description="Brief explanation of what drives the cost and any important caveats.")

class StepsOutput(BaseModel):
    """Schema for Step 1: extracted process steps."""
    process_steps: list[ProcessStepItem]


class InefficienciesOutput(BaseModel):
    """Schema for Step 2: identified inefficiencies."""
    inefficiencies: list[InefficiencyItem]


class AutomationsOutput(BaseModel):
    """Schema for Step 3: suggested automation opportunities."""
    automation_opportunities: list[AutomationItem]


class ToolsOutput(BaseModel):
    """Schema for Step 4: recommended tools."""
    suggested_tools: list[ToolItem]


class CostEstimatesOutput(BaseModel):
    """Schema for Step 5: cost estimates."""
    cost_estimates: list[CostEstimateItem]

class AnalysisResult(BaseModel):
    """Combined schema representing the full pipeline output."""
    process_steps: list[ProcessStepItem]
    inefficiencies: list[InefficiencyItem]
    automation_opportunities: list[AutomationItem]
    suggested_tools: list[ToolItem]
    cost_estimates: list[CostEstimateItem]

def validate_output(data: dict) -> bool:
    """Validate a result dict against the full AnalysisResult schema."""
    try:
        AnalysisResult(**data)
        return True
    except Exception:
        return False
