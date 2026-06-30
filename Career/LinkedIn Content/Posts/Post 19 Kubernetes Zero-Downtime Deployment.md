---
type: linkedin-post
post_number: 19
scheduled_week: 10
scheduled_day: Tuesday
status: drafted
---
How Kubernetes achieves zero-downtime deployments — step by step.

[ATTACH: Rolling update animation or step diagram]

The Rolling Update sequence for 3 pods (maxSurge: 1, maxUnavailable: 0):

Step 1: Kubernetes creates Pod 4 (new version). Now 4 pods running.
Step 2: Kubernetes waits for Pod 4 readinessProbe to return healthy.
Step 3: Kubernetes removes Pod 1 (old version). Back to 3 pods.
Step 4: Repeat for Pod 2, then Pod 3.

The critical detail: Pod 1 is only removed AFTER Pod 4 is READY.
"Ready" = readinessProbe returns 200.

If your readinessProbe checks database connectivity and the new pod
cannot connect: it never becomes Ready, Kubernetes never removes the old pod,
and your deployment rolls back automatically.

Zero-downtime is not magic. It's readiness probes + rolling update config.

One mistake I made: forgetting to add a preStop hook to drain in-flight
requests before the pod is terminated. Without it, users mid-request
get a connection reset.

#Kubernetes #DevOps #BackendEngineering
