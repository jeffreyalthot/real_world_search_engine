# Contrats API (prototype)

## gRPC: HypothesisService

- `GenerateHypotheses(GenerateHypothesesRequest) returns (GenerateHypothesesResponse)`
- `ValidateHypothesis(ValidateHypothesisRequest) returns (ValidationResponse)`

## gRPC: SimulationBroker

- `SubmitSimulation(SimulationSpec) returns (SimulationTicket)`
- `GetSimulationResult(SimulationTicket) returns (SimulationResult)`

## Event Bus

Topics recommandés:
- `knowledge.claims.ingested`
- `hypothesis.generated`
- `simulation.completed`
- `portfolio.updated`
