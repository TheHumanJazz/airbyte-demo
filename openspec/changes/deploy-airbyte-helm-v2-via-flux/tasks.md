## 1. Fix the Flux-managed Airbyte overlay

- [ ] 1.1 Inspect the existing `clusters/kind/airbyte-v2/` manifests and identify the settings preventing a healthy Flux reconcile.
- [ ] 1.2 Update the HelmRelease, HelmRepository, namespace, and any required values so the Airbyte Helm chart v2 release can install cleanly.
- [ ] 1.3 Add or correct any required Secret or ConfigMap references needed by the chart values.

## 2. Verify the rollout

- [ ] 2.1 Reconcile the Flux source and HelmRelease until the Airbyte release reports ready.
- [ ] 2.2 Confirm the namespace and Airbyte workloads are present with `kubectl`.
- [ ] 2.3 Record any remaining follow-up fixes if Flux or Kubernetes reports a failure.
