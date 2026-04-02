## ADDED Requirements

### Requirement: CloudNativePG operator is installed by Flux
The cluster MUST deploy the CloudNativePG operator through Flux so the operator is present after the `clusters/kind` overlay reconciles.

#### Scenario: Flux reconciliation installs the operator
- **WHEN** Flux applies the `clusters/kind` overlay
- **THEN** the CloudNativePG operator resources are created and become ready in the cluster
