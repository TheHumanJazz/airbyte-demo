## 1. Configure the Airbyte UI ingress

- [x] 1.1 Inspect the existing `clusters/kind/airbyte-v2/` HelmRelease values and confirm which ingress block drives the web UI.
- [x] 1.2 Update the Airbyte values to enable only the webapp ingress for `airbyte.localtest.me` over HTTP with the nginx ingress class.
- [x] 1.3 Keep the top-level Airbyte ingress disabled and preserve ClusterIP service exposure.

## 2. Verify access paths

- [x] 2.1 Reconcile Flux and confirm the Airbyte ingress resource is created successfully.
- [x] 2.2 Open `http://airbyte.localtest.me` in a browser and verify the UI loads.
- [x] 2.3 Confirm in-cluster callers can still reach Airbyte through service DNS.
