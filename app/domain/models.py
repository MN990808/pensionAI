# models.py: Defines versioned request, dialogue, task, evidence, verification, and response contracts.

from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Intent(str, Enum):
    SIMPLE_LOOKUP = "simple_lookup"
    ACCOUNT_TASK = "account_task"
    PERSONAL_ADVICE = "personal_advice"
    PRODUCT_LOOKUP = "product_lookup"


class NextAction(str, Enum):
    CLARIFY = "clarify"
    RETRIEVE = "retrieve"


class ChatStatus(str, Enum):
    PASS = "PASS"
    NEEDS_CLARIFICATION = "NEEDS_CLARIFICATION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=128)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    llm_mode: str


class Evidence(BaseModel):
    document_id: str
    title: str
    content: str
    keywords: list[str] = Field(default_factory=list)
    authority_level: str
    effective_date: date
    source_uri: str
    is_sample: bool = False


class Clarification(BaseModel):
    slot: str
    question: str
    options: list[str] = Field(default_factory=list)


class DialogueState(BaseModel):
    schema_version: str = "1.0"
    state_version: int = 1
    user_goal: str
    intent: Intent
    pension_type: str | None = None
    assumptions: list[str] = Field(default_factory=list)
    ambiguities: list[str] = Field(default_factory=list)


class TaskSpec(BaseModel):
    schema_version: str = "1.0"
    task_id: str
    objective: str
    intent: Intent
    assigned_agent: str
    required_inputs: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
    risk_level: str
    success_criteria: list[str]
    assumptions: list[str] = Field(default_factory=list)


class VerificationResult(BaseModel):
    passed: bool
    code: str
    checks: dict[str, bool]


class ChatResponse(BaseModel):
    schema_version: str = "1.0"
    request_id: str
    status: ChatStatus
    intent: Intent
    answer: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    clarification: Clarification | None = None
    verification: VerificationResult | None = None
    trace: dict[str, Any] = Field(default_factory=dict)
