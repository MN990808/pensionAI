# verifier.py: Checks evidence coverage, answer presence, and sample-data scope independently of generation.

from app.domain.models import Evidence, Intent, TaskSpec, VerificationResult


class Verifier:
    """Independent MVP verifier for grounded responses."""

    def verify(
        self,
        task: TaskSpec,
        answer: str,
        evidence: list[Evidence],
    ) -> VerificationResult:
        """Return machine-readable postcondition results."""
        checks = {
            "answer_present": bool(answer.strip()),
            "evidence_present": bool(evidence),
            "source_fields_present": self._sources_complete(evidence),
            "sample_scope_allowed": self._sample_scope_allowed(task, evidence),
        }
        passed = all(checks.values())
        code = "PASS" if passed else "VERIFICATION_FAILED"
        return VerificationResult(passed=passed, code=code, checks=checks)

    def _sources_complete(self, evidence: list[Evidence]) -> bool:
        return all(
            item.document_id and item.title and item.source_uri and item.effective_date
            for item in evidence
        )

    def _sample_scope_allowed(self, task: TaskSpec, evidence: list[Evidence]) -> bool:
        has_sample = any(item.is_sample for item in evidence)
        return not has_sample or task.intent == Intent.SIMPLE_LOOKUP
