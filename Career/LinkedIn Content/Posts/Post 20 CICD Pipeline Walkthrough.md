---
type: linkedin-post
post_number: 20
scheduled_week: 10
scheduled_day: Friday
status: drafted
---
My full CI/CD pipeline from push to production. Built with GitHub Actions.

[ATTACH: Pipeline flowchart diagram]

4 stages on every push to main:

1. TEST
   → mvn test (JUnit 5 + TestContainers)
   → jacoco:check (fails if coverage < 80%)
   → Takes: ~45 seconds

2. BUILD
   → Multi-stage Dockerfile (Maven builder + JRE Alpine runtime)
   → docker/build-push-action to GHCR
   → Image tagged with git SHA for traceability
   → Takes: ~90 seconds

3. DEPLOY (Dev)
   → kubectl set image deployment/order-api [new-image-sha]
   → kubectl rollout status (waits for rolling update to complete)
   → Takes: ~30 seconds

4. DEPLOY (Prod)
   → Requires manual approval in GitHub Environment settings
   → Same kubectl commands, different namespace

Total time from push to production: ~3 minutes (+ manual approval).

The GitHub Actions YAML is in the repo: [link]

#DevOps #Kubernetes #BackendEngineering
