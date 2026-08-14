<!-- NAVER_CLOUD_DEPLOYMENT.md: Defines the minimal, secure Naver Cloud deployment path for the contest endpoint. -->
# Naver Cloud Deployment v1

## Provisioning Order

1. Apply and register the team credit coupon.
2. Confirm credit eligibility for every planned service.
3. Create VPC `10.0.0.0/16`.
4. Create public subnet `10.0.1.0/24` in the selected zone.
5. Start with a Micro Linux server for the stub baseline; upgrade to around 2 vCPU and 4 GB RAM before production-like load tests.
6. Assign one public IP.
7. Configure a dedicated ACG.
8. Install Docker and deploy the API.
9. Add HTTPS and the evaluator-compatible route.

## ACG Baseline

| Direction | Port | Source | Purpose |
|---|---:|---|---|
| Inbound | 22 | Team IP `/32` | SSH only |
| Inbound | 80 | `0.0.0.0/0` | HTTP redirect/validation |
| Inbound | 443 | `0.0.0.0/0` | Public HTTPS API |
| Outbound | 443 | `0.0.0.0/0` | CLOVA Studio and package access |

Never expose SSH or a database port to `0.0.0.0/0`.

## Deferred Services

Load Balancer, API Gateway, managed PostgreSQL, Redis, object storage, autoscaling, and separate agent servers are optional until the single-server baseline passes evaluation tests.

## Deployment Gate

- `/health` returns HTTP 200.
- Chat endpoint validates malformed input with HTTP 422.
- Secrets are runtime variables, not image layers or repository files.
- Logs contain request IDs but no raw account numbers or API keys.
- Unused public IP and server resources are removed to prevent cost leakage.

## Single-Server Runtime

The FastAPI container binds only to `127.0.0.1:8000`. Nginx is the only public entry point and proxies port 80 to the container. Port 8000 must never be added to the ACG.

```bash
PENSION_AI_BRANCH=agent/pension-advisor-skeleton \
  bash scripts/bootstrap_server.sh
curl --fail http://SERVER_PUBLIC_IP/health
```

Enable HTTPS only after a team-owned domain points to the public IP. Store the CLOVA Studio key in a server-side `.env` file and never copy it into an image layer or Git commit.
