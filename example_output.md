# Example Output (simplified)

## RACI Matrix (excerpt)

| Activity                        | Intake Agent Owner | Research Agent Owner | Draft Agent Owner | Review Agent Owner | System Owner | Human Agents |
|---------------------------------|--------------------|----------------------|-------------------|--------------------|--------------|--------------|
| Design & prompt configuration   | C                  | C                    | R                 | C                  | A            | I            |
| Deployment to production        | I                  | I                    | I                 | I                  | A            | C            |
| Daily monitoring                | R                  | R                    | R                 | R                  | A            | C            |
| Incident response               | C                  | C                    | C                 | C                  | A            | R            |
| Model / knowledge base updates  | I                  | R                    | C                 | C                  | A            | I            |

R = Responsible, A = Accountable, C = Consulted, I = Informed

## Residual Risk Statements (excerpt)

- Residual risk: Incorrect urgency classification by Intake Agent may delay high-severity tickets.  
  Mitigation: Human review of all tickets scored above threshold. Review frequency: daily sample check.

- Residual risk: Research Agent may surface outdated or incorrect knowledge-base content.  
  Mitigation: Knowledge base version control + Review Agent policy check. Human override available.

## Decision Gates

1. System Owner must sign the full accountability package before first production deployment.  
2. Any change to agent prompts or knowledge sources that affects high-urgency routing requires re-sign-off by System Owner and Review Agent Owner.

## Human Oversight Points

- High-urgency tickets: mandatory human approval before reply is sent.  
- Weekly sample review of 20 random completed tickets by a senior human agent.  
- Monthly review of residual-risk register by System Owner.
