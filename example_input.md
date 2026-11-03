# Example Input

System description:

We run a customer-support multi-agent setup.  
- Intake Agent receives tickets and classifies urgency.  
- Research Agent pulls relevant knowledge-base articles and past tickets.  
- Draft Agent writes the reply.  
- Review Agent checks tone and policy compliance before the reply is sent.  
- Escalation Agent routes high-risk or complex tickets to human agents.

The system uses an external LLM API and a private knowledge base.  
Human agents handle final approval on all high-urgency tickets and any ticket flagged by the Review Agent.
