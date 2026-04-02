## Why

Airbyte needs to be deployed to the cluster in a way Flux can reconcile reliably, and the current attempt has failed. This change makes the deployment declarative and repeatable so the cluster can converge on a working Airbyte Helm chart v2 install.

## What Changes

- Add a Flux-managed Airbyte deployment based on Helm chart v2.
- Align cluster resources so Airbyte is installed into the target namespace and reconciled through Flux.
- Replace the failed deployment attempt with a working configuration that can be validated with `flux` and `kubectl`.

## Capabilities

### New Capabilities
- `airbyte-flux-deployment`: declarative Airbyte deployment on the cluster using Flux and Helm chart v2.

### Modified Capabilities

- 

## Impact

- Cluster manifests under `clusters/kind/airbyte-v2/`.
- Flux resources such as `HelmRepository` and `HelmRelease`.
- Airbyte namespace, chart values, and any related secrets or config inputs.
