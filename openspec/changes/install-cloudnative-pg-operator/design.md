## Context

The repository already uses Flux to manage the `clusters/kind` environment, so the cleanest way to add CloudNativePG is to treat it as another Flux-managed cluster dependency. This change is operator-only: it installs the control plane for future PostgreSQL clusters but does not create any database instances yet.

## Goals / Non-Goals

**Goals:**
- Install the CloudNativePG operator in the `clusters/kind` environment through Flux.
- Keep the change isolated to the cluster overlay and consistent with the repo's existing Flux pattern.
- Make the operator easy to verify and easy to remove if rollout fails.

**Non-Goals:**
- Create any `Cluster` or `Backup` resources for application databases.
- Change Airbyte's database configuration.
- Introduce a new deployment system outside Flux.

## Decisions

- Use a Flux `HelmRepository` plus `HelmRelease` for the operator instead of raw manifests. This matches the repo's current cluster management style and gives Flux a clear reconciliation target. Alternatives: vendoring manifests or using a one-off `kubectl apply`; both are less declarative and harder to maintain.
- Install the operator into its own namespace. This keeps controller resources separated from application namespaces and makes lifecycle management simpler. Alternatives: co-locate with workloads or use `flux-system`; both blur ownership boundaries.
- Pin the operator version in the HelmRelease. CloudNativePG is a cluster dependency, so deterministic upgrades matter more than chasing the latest release. Alternatives: track `latest` or an unpinned chart source; both increase rollout risk.
- Keep the overlay limited to operator bootstrap resources. Database cluster definitions belong in follow-up changes once the operator is in place. Alternatives: bundle operator plus database bootstrap in one change; that would make failure analysis and rollback harder.

## Risks / Trade-offs

- [CRDs and webhook resources may take longer to become ready than the Helm release itself] → Mitigate by verifying Flux readiness and allowing a separate reconcile cycle before creating any database clusters.
- [A version mismatch between the operator and future CRDs can block follow-up changes] → Mitigate by pinning the operator version and treating upgrades as explicit changes.
- [The operator may require cluster-wide permissions that are easy to misconfigure] → Mitigate by keeping the install minimal and validating the rendered HelmRelease against Flux events.

## Migration Plan

1. Add the CloudNativePG Helm repository and HelmRelease to the `clusters/kind` overlay.
2. Reconcile Flux until the operator deployment reports ready.
3. Verify the operator namespace, deployment, and CRDs are present.
4. If reconciliation fails, remove the new Flux resources and re-reconcile the overlay.

## Open Questions

- Which CloudNativePG chart version should be pinned for the initial install?
- Do we want the operator namespace to follow the upstream `cnpg-system` convention or a repo-specific name?
