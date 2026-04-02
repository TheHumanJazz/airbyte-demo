## ADDED Requirements

### Requirement: Airbyte UI is exposed on a local kind host
The system SHALL expose the Airbyte web UI on `http://airbyte.localtest.me` through the kind ingress controller.

#### Scenario: Flux creates the UI ingress
- **WHEN** Flux reconciles the Airbyte release
- **THEN** it SHALL create an ingress for the Airbyte web UI with host `airbyte.localtest.me`
- **AND** the ingress SHALL use the nginx ingress class
- **AND** the ingress SHALL be reachable over plain HTTP

### Requirement: Only the UI is published externally
The system SHALL keep the top-level Airbyte ingress disabled so that only the UI is exposed to external traffic.

#### Scenario: The release reconciles without a public API ingress
- **WHEN** the Airbyte release is applied
- **THEN** no top-level Airbyte ingress resource SHALL be created for external access
- **AND** the browser-facing ingress SHALL be limited to the web UI

### Requirement: Internal service access remains available
The system SHALL keep the Airbyte service endpoints accessible inside the cluster for internal consumers.

#### Scenario: In-cluster workloads reach Airbyte directly
- **WHEN** a pod in the cluster accesses Airbyte by service DNS
- **THEN** the request SHALL resolve to ClusterIP services inside the cluster
- **AND** internal access SHALL remain available without using the public ingress host
