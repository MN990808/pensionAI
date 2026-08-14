# orchestrator.py: Coordinates routing, dialogue policy, retrieval, generation, and independent verification.

from uuid import uuid4

from app.dialogue.policy import DialoguePolicy
from app.dialogue.rule_router import RuleRouter
from app.domain.models import (
    ChatRequest,
    ChatResponse,
    ChatStatus,
    DialogueState,
    Evidence,
    Intent,
    NextAction,
    TaskSpec,
    VerificationResult,
)
from app.providers.base import ResponseProvider
from app.retrieval.base import Retriever
from app.services.create_task_spec import create_task_spec
from app.verification.verifier import Verifier


class PensionOrchestrator:
    """Single writer and workflow coordinator for the MVP."""

    def __init__(self, retriever: Retriever, provider: ResponseProvider) -> None:
        self._retriever = retriever
        self._provider = provider
        self._router = RuleRouter()
        self._policy = DialoguePolicy()
        self._verifier = Verifier()

    async def handle(self, request: ChatRequest) -> ChatResponse:
        """Execute one guarded dialogue turn."""
        request_id = str(uuid4())
        state = self._analyze(request)
        task = create_task_spec(state)
        action = self._policy.select(state.intent, state.pension_type)
        if action == NextAction.CLARIFY:
            return self._clarification_response(request_id, state, task)
        evidence = await self._retriever.search(request.message)
        if not evidence:
            return self._no_evidence_response(request_id, state, task)
        answer = await self._provider.complete(request.message, evidence)
        verification = self._verifier.verify(task, answer, evidence)
        return self._answer_response(request_id, state, task, answer, evidence, verification)

    def _analyze(self, request: ChatRequest) -> DialogueState:
        intent = self._router.classify(request.message)
        pension_type = self._router.extract_pension_type(request.message)
        return DialogueState(
            user_goal=request.message,
            intent=intent,
            pension_type=pension_type,
        )

    def _clarification_response(
        self,
        request_id: str,
        state: DialogueState,
        task: TaskSpec,
    ) -> ChatResponse:
        clarification = self._policy.clarification(state.intent)
        return ChatResponse(
            request_id=request_id,
            status=ChatStatus.NEEDS_CLARIFICATION,
            intent=state.intent,
            clarification=clarification,
            trace=self._trace(state, task),
        )

    def _no_evidence_response(
        self,
        request_id: str,
        state: DialogueState,
        task: TaskSpec,
    ) -> ChatResponse:
        return ChatResponse(
            request_id=request_id,
            status=ChatStatus.INSUFFICIENT_EVIDENCE,
            intent=state.intent,
            answer="현재 공개 샘플 지식에는 이 질문을 뒷받침할 근거가 없습니다.",
            trace=self._trace(state, task),
        )

    def _answer_response(
        self,
        request_id: str,
        state: DialogueState,
        task: TaskSpec,
        answer: str,
        evidence: list[Evidence],
        verification: VerificationResult,
    ) -> ChatResponse:
        status = ChatStatus.PASS if verification.passed else ChatStatus.VERIFICATION_FAILED
        return ChatResponse(
            request_id=request_id,
            status=status,
            intent=state.intent,
            answer=answer if verification.passed else None,
            evidence=evidence,
            assumptions=state.assumptions,
            verification=verification,
            trace=self._trace(state, task),
        )

    def _trace(self, state: DialogueState, task: TaskSpec) -> dict[str, object]:
        return {
            "state_version": state.state_version,
            "task_id": task.task_id,
            "assigned_agent": task.assigned_agent,
        }
