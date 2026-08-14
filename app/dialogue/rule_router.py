# rule_router.py: Performs deterministic first-pass intent and pension-type extraction before LLM analysis.

from app.domain.models import Intent


class RuleRouter:
    """Conservative deterministic router for the MVP baseline."""

    _intent_keywords = {
        Intent.ACCOUNT_TASK: ("수익률", "수수료", "잔액", "계좌 조회"),
        Intent.PERSONAL_ADVICE: ("추천", "맞춤", "갈아타", "나에게"),
        Intent.PRODUCT_LOOKUP: ("상품", "ETF", "펀드", "투자설명서"),
    }
    _pension_types = ("IRP", "DC", "DB", "연금저축")

    def classify(self, query: str) -> Intent:
        """Return the first matching high-signal intent."""
        normalized = query.upper()
        for intent, keywords in self._intent_keywords.items():
            if any(keyword.upper() in normalized for keyword in keywords):
                return intent
        return Intent.SIMPLE_LOOKUP

    def extract_pension_type(self, query: str) -> str | None:
        """Extract a supported pension type without guessing."""
        normalized = query.upper()
        for pension_type in self._pension_types:
            if pension_type.upper() in normalized:
                return pension_type
        return None
