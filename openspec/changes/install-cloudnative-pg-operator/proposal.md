## Why

The cluster needs a declarative PostgreSQL operator foundation before any workloads depend on it. Installing CloudNativePG now gives the cluster a managed Postgres control plane that Flux can reconcile consistently.

## What Changes

- Add CloudNativePG operator manifests to the `clusters/kind` Flux overlay.
- Wire the operator into the cluster kustomization so it deploys with the rest of the environment.
- Keep Airbyte and other existing workloads unchanged for this change.

## Capabilities

### New Capabilities
- `cloudnative-pg-operator`: declarative installation of the CloudNativePG operator in the cluster.

### Modified Capabilities
- 

## Impact

- Cluster manifests under `clusters/kind/`.
- New Flux-managed resources for the CloudNativePG operator.
- Future Postgres workloads can depend on the operator being present, but no application configuration changes are required yet.
