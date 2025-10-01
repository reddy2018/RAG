# Kubernetes Runbook

## CrashLoopBackOff
1. Check pod logs: `kubectl logs <pod> -n <ns>`
2. Check container readiness/liveness probes.
3. Check OOMKilled: `kubectl describe pod <pod>` and look for OOMKilled reason.
4. If config issue, update ConfigMap/Secret and rollout restart deployment.
