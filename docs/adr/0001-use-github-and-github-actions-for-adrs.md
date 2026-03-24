# 1. Use GitHub and GitHub Actions for ADRs

Date: 2026-03-24

## Status

Accepted

## Context

We need a systematic way to manage Architectural Decision Records (ADRs). Currently, decisions and architecture diagrams are scattered and hard to maintain. Furthermore, diagrams often become outdated or reference informal systems that drift from reality. We want to align our process loosely with the C4 model for architecture diagrams, relying on "Software Systems" and "Containers". 

Mermaid provides a C4-compatible templating DSL, but there is no native validation to ensure diagrams accurately reference the allowed systems. 

## Decision

We will use **GitHub** to store our ADRs in markdown format. 

For architecture diagrams within ADRs, we will strictly use **Mermaid JS**, specifically its C4 diagram capabilities. Furthermore, we will establish a `software_systems.yaml` definitions file within the repository as the baseline for all available software systems.

We will write a python script that automatically parses markdown ADRs, looking for Mermaid C4 definitions, and validates that every container referenced belongs to a known software system from `software_systems.yaml`. 

Finally, we will use **GitHub Actions** to automate this validation on pull requests, rejecting any diagrams that do not conform to the system boundaries. We will also introduce an automated step to compile mermaid markdown blocks into image files (like PNG) to be embedded directly into the ADRs for better viewing support outside of environments that render mermaid natively.

## Consequences

- **Positive:** All architectural diagrams will follow standard C4 terminology and explicitly reference a single set of truth for software systems, improving clarity.
- **Positive:** Automated validation will enforce consistency before any Pull Request is merged.
- **Positive:** Generated images ensure compatibility and persistence for historical documentation.
- **Negative:** Diagram authors must ensure they are using the correct Mermaid C4 syntax and referencing valid systems, adding a slight overhead to composing new ADRs.
- **Negative:** We need to maintain custom validation scripts.
