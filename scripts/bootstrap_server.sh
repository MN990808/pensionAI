#!/usr/bin/env bash
# bootstrap_server.sh: Installs the single-server runtime and deploys Pension Advisor behind Nginx.
set -Eeuo pipefail

trap 'echo "Server bootstrap failed at line ${LINENO}." >&2' ERR

readonly REPOSITORY_URL="${PENSION_AI_REPOSITORY_URL:-https://github.com/MN990808/pensionAI.git}"
readonly DEPLOY_BRANCH="${PENSION_AI_BRANCH:-agent/pension-advisor-skeleton}"
readonly APP_DIR="${PENSION_AI_APP_DIR:-/opt/pension-ai}"

sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 git nginx
sudo systemctl enable --now docker nginx

if [[ ! -d "${APP_DIR}/.git" ]]; then
  sudo git clone --branch "${DEPLOY_BRANCH}" "${REPOSITORY_URL}" "${APP_DIR}"
fi

sudo git -C "${APP_DIR}" fetch origin "${DEPLOY_BRANCH}"
sudo git -C "${APP_DIR}" checkout "${DEPLOY_BRANCH}"
sudo git -C "${APP_DIR}" pull --ff-only origin "${DEPLOY_BRANCH}"
sudo install -m 0644 "${APP_DIR}/deploy/nginx/pension-ai.conf" /etc/nginx/sites-available/pension-ai
sudo ln -sfn /etc/nginx/sites-available/pension-ai /etc/nginx/sites-enabled/pension-ai
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
sudo docker compose -f "${APP_DIR}/docker-compose.yml" up -d --build
curl --fail --silent --show-error http://127.0.0.1/health
