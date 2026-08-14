#!/usr/bin/env bash
# smoke_test.sh: Verifies the deployed health, validation, and evaluator contracts over HTTP.
set -Eeuo pipefail

trap 'echo "Deployment smoke test failed at line ${LINENO}." >&2' ERR

readonly BASE_URL="${BASE_URL:-http://127.0.0.1}"
READY="false"

for attempt in {1..15}; do
  if curl --fail --silent --output /dev/null "${BASE_URL}/health"; then
    READY="true"
    break
  fi
  sleep 2
done

[[ "${READY}" == "true" ]]
readonly HEALTH_RESPONSE="$(curl --fail --silent --show-error "${BASE_URL}/health")"
readonly VALIDATION_STATUS="$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
  -X POST "${BASE_URL}/v1/chat" -H 'Content-Type: application/json' -d '{"message":""}')"

grep -q '"status":"ok"' <<<"${HEALTH_RESPONSE}"
[[ "${VALIDATION_STATUS}" == "422" ]]
curl --fail --silent --show-error --get "${BASE_URL}/v1/evaluate" \
  --data-urlencode 'question=이 프로젝트는 무엇인가요?' >/dev/null
printf 'Deployment smoke test passed for %s\n' "${BASE_URL}"
