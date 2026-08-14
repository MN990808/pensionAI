# policy.py: Selects the next dialogue action from validated intent and slot state.

from app.domain.models import Clarification, Intent, NextAction


class DialoguePolicy:
    """Rule-owned next-action policy for high-risk missing slots."""

    _pension_required = {Intent.ACCOUNT_TASK, Intent.PERSONAL_ADVICE}

    def select(self, intent: Intent, pension_type: str | None) -> NextAction:
        """Clarify when a material pension-type slot is absent."""
        if intent in self._pension_required and pension_type is None:
            return NextAction.CLARIFY
        return NextAction.RETRIEVE

    def clarification(self, intent: Intent) -> Clarification:
        """Return one high-information clarification question."""
        if intent == Intent.ACCOUNT_TASK:
            question = "조회하려는 계좌가 DB, DC, IRP, 연금저축 중 무엇인가요?"
        else:
            question = "상담 기준이 되는 연금 유형을 먼저 알려주세요."
        return Clarification(
            slot="pension_type",
            question=question,
            options=["DB", "DC", "IRP", "연금저축"],
        )
