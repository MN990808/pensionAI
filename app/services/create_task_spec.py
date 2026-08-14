# create_task_spec.py: Converts validated dialogue analysis into a versioned executable TaskSpec.

from uuid import uuid4

from app.domain.models import DialogueState, Intent, TaskSpec


_agent_by_intent = {
    Intent.SIMPLE_LOOKUP: "knowledge_agent",
    Intent.ACCOUNT_TASK: "account_agent",
    Intent.PERSONAL_ADVICE: "advisor_agent",
    Intent.PRODUCT_LOOKUP: "product_agent",
}

_tool_by_intent = {
    Intent.SIMPLE_LOOKUP: ["knowledge_search"],
    Intent.ACCOUNT_TASK: ["account_read"],
    Intent.PERSONAL_ADVICE: ["knowledge_search", "suitability_check"],
    Intent.PRODUCT_LOOKUP: ["product_search", "product_document_fetch"],
}


def create_task_spec(state: DialogueState) -> TaskSpec:
    """Build the minimum task contract for the current vertical slice."""
    required = [] if state.pension_type else ["pension_type"]
    risk = "low" if state.intent == Intent.SIMPLE_LOOKUP else "high"
    return TaskSpec(
        task_id=f"task-{uuid4()}",
        objective=state.user_goal,
        intent=state.intent,
        assigned_agent=_agent_by_intent[state.intent],
        required_inputs=required,
        allowed_tools=_tool_by_intent[state.intent],
        risk_level=risk,
        success_criteria=["Every factual claim has evidence", "Verifier returns PASS"],
        assumptions=state.assumptions,
    )
