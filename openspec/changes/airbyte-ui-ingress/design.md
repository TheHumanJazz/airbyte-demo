## Context

The repo already boots a kind cluster with ingress-nginx mapped onto host port 80, and the Airbyte deployment lives under `clusters/kind/airbyte-v2/`. The Airbyte chart exposes multiple ingress entry points, but the current deployment keeps them disabled, so the UI is not reachable from a browser.

The user wants a local-only host, `airbyte.localtest.me`, with plain HTTP and no TLS, while preserving internal ClusterIP access.

## Goals / Non-Goals

**Goals:**
- Expose only the Airbyte UI externally on `http://airbyte.localtest.me`.
- Keep internal service access intact for in-cluster workloads.
- Fit the change into the existing Flux-managed kind overlay.

**Non-Goals:**
- Add HTTPS or cert-manager integration.
- Change Airbyte runtime behavior beyond ingress exposure.
- Introduce a new deployment path outside Flux + Helm.

## Decisions

- Use the chart’s webapp ingress rather than publishing the full top-level Airbyte ingress. This keeps the browser-facing surface as small as possible and matches the requirement to expose only the UI. Alternatives considered: enable the top-level ingress as well, or route the UI through a separate reverse proxy; both add unnecessary surface area.
- Use `airbyte.localtest.me` as the host and plain HTTP. This works naturally with local kind because the host resolves to loopback and the cluster already exposes ingress-nginx on host port 80. Alternatives considered: `localhost`, a custom `/etc/hosts` entry, or TLS; each is either less portable or unnecessary for the stated goal.
- Keep Airbyte services as `ClusterIP`. The ingress should be the only external entry point, while internal callers continue using service DNS. Alternatives considered: changing services to `NodePort` or `LoadBalancer`; those would weaken the access boundary and are not needed.

## Risks / Trade-offs

- [Chart ingress semantics may differ between the webapp and top-level blocks] -> Mitigate by verifying the rendered Helm release and checking the created ingress resources after reconciliation.
- [The chosen host may not resolve in every local environment] -> Mitigate by using `localtest.me`, which is designed to resolve to `127.0.0.1`.
- [Exposing only the UI may limit direct browser access to other Airbyte endpoints] -> Mitigate by keeping internal service access available for cluster-native consumers.

## Migration Plan

1. Update the Airbyte HelmRelease values to enable only the webapp ingress for `airbyte.localtest.me`.
2. Reconcile Flux and confirm the ingress resource is created on class `nginx`.
3. Verify the UI opens in a browser at `http://airbyte.localtest.me`.
4. Confirm in-cluster service access still works through ClusterIP DNS names.

## Open Questions

- None.
