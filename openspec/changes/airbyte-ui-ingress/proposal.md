## Why

The current Airbyte kind deployment has ingress plumbing in the cluster, but the Airbyte release itself is not exposed to a browser. We want a simple local URL for the UI so the deployment can be used and verified end-to-end without changing the internal service access pattern.

## What Changes

- Expose the Airbyte web UI on `http://airbyte.localtest.me` through the existing kind ingress controller.
- Keep the top-level Airbyte ingress disabled so only the UI is published externally.
- Keep Airbyte services as `ClusterIP` so in-cluster access remains available.
- Use plain HTTP only for local kind usage.

## Capabilities

### New Capabilities
- `airbyte-ui-ingress`: expose the Airbyte UI through a local kind ingress host while preserving internal service access.

### Modified Capabilities
- None.

## Impact

- `clusters/kind/airbyte-v2/helmrelease.yaml` will need UI ingress values.
- The existing kind ingress-nginx controller will serve the host.
- Verification will rely on Flux reconciliation and browser access to `airbyte.localtest.me`.
