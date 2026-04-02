## 1. Prepare the Flux overlay

- [ ] 1.1 Inspect the existing `clusters/kind` Flux structure and identify where the CloudNativePG operator resources should live.
- [ ] 1.2 Add the namespace and Flux source/release manifests needed to install the operator.
- [ ] 1.3 Include the new manifests in the `clusters/kind` kustomization so Flux applies them.

## 2. Verify the operator install

- [ ] 2.1 Reconcile Flux until the CloudNativePG operator reports ready.
- [ ] 2.2 Confirm the operator namespace, deployment, and CRDs exist with `kubectl`.
- [ ] 2.3 Record any follow-up issues if reconciliation fails or resources do not become ready.
