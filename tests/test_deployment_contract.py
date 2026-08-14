# test_deployment_contract.py: Verifies deployment files preserve the loopback-only application boundary.

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    try:
        return (ROOT / relative_path).read_text(encoding="utf-8")
    except OSError as exc:
        raise AssertionError(f"Could not read deployment file: {relative_path}") from exc


def test_compose_does_not_publish_fastapi_publicly() -> None:
    compose = read_text("docker-compose.yml")
    assert '"127.0.0.1:8000:8000"' in compose
    assert '"8000:8000"' not in compose.replace('"127.0.0.1:8000:8000"', "")


def test_nginx_is_the_public_http_entrypoint() -> None:
    nginx = read_text("deploy/nginx/pension-ai.conf")
    assert "listen 80 default_server;" in nginx
    assert "proxy_pass http://127.0.0.1:8000;" in nginx
