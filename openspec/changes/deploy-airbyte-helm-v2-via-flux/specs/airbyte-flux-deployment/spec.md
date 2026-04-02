## ADDED Requirements

### Requirement: Flux-managed Airbyte deployment
The system SHALL define a Flux-managed Airbyte deployment that installs the Helm chart v2 release into the cluster target namespace and keeps it reconciled through Flux.

#### Scenario: Flux reconciles the Airbyte release
- **WHEN** Flux reconciles the change
- **THEN** it SHALL create or update the Airbyte HelmRelease from the Airbyte HelmRepository using chart v2
- **AND** the release SHALL be targeted at the Airbyte namespace in the cluster

#### Scenario: Deployment can be verified in-cluster
- **WHEN** the deployment has reconciled successfully
- **THEN** `flux` and `kubectl` SHALL report the Airbyte resources as present in the cluster
