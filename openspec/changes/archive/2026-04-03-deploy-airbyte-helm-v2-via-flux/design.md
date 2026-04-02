## Context

The repo already contains a Flux-managed `clusters/kind/airbyte-v2/` overlay with a `HelmRepository`, `HelmRelease`, and namespace manifest. The current attempt failed, so the main problem is not introducing a new deployment model but making the existing Flux + Helm chart v2 path converge cleanly in-cluster.

## Goals / Non-Goals

**Goals:**
- Make Airbyte deployable through Flux using Helm chart v2.
- Keep the deployment scoped to the existing `airbyte-v2` cluster overlay.
- Ensure the final state is easy to verify with `flux` and `kubectl`.

**Non-Goals:**
- Redesign Airbyte runtime architecture.
- Introduce a new deployment toolchain outside Flux/Helm.
- Optimize Airbyte runtime configuration beyond what is needed for a successful reconcile.

## Decisions

- Use the existing `clusters/kind/airbyte-v2/` overlay instead of creating a second deployment path. This minimizes drift and keeps the fix local to the failed attempt. Alternatives: create a new overlay or replace Flux with manual Helm installs; both add unnecessary surface area.
- Keep the Helm chart pinned to v2 and managed through `HelmRelease` plus `HelmRepository`. This preserves Flux reconciliation semantics and avoids vendoring chart contents. Alternatives: raw manifests or a custom controller; both would be harder to maintain.
- Treat the deployment as configuration-first: repair chart values, namespace wiring, and secret references until Flux reports the release healthy. This targets the actual failure mode rather than changing the app itself.

## Risks / Trade-offs

- [Chart values may be incomplete] -> Mitigate by validating the rendered release with Flux events and tightening values only where needed.
- [Missing secrets or external dependencies can block reconciliation] -> Mitigate by verifying referenced Secrets/ConfigMaps exist before rollout and by keeping rollback to a commit revert.
- [Chart v2 may have behavior differences from the prior attempt] -> Mitigate by pinning the chart version and verifying the exact release state after each change.

## Migration Plan

1. Update the `airbyte-v2` overlay to match the chart v2 expectations.
2. Reconcile the Flux source and HelmRelease.
3. Verify the namespace and Airbyte resources with `kubectl`.
4. If reconciliation fails, revert the change and re-run Flux reconciliation.

## Open Questions

- What cluster-specific secrets and credentials must be present before the release can go healthy?
- Should the deployment use internal storage/database defaults or integrate with existing external services?
- Is ingress/host configuration required for the initial rollout, or is internal-only access sufficient?
