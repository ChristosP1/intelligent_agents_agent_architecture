# Agent Design Document

Possible architectures;

- Reflex agent w/ state
- Goal-based agent
- Utility agent
- BDI agent
- Value/Norm Agent

We have the following scenarios;

- A scenario involving whether a headache is caused by a lack of water (or a collision).
- A scenario involving whether a sickness a customer got was obtained from an allergy (or a venomous animal meat)
- A scenario involving ???
- A scenario involving ???

Thus, we believe it is correct to make a Utility agent.

The utility agent's utility function would involve

# Env

The env initially emits the prompt of a user (can be wrapped into an application), after which
the next perceiving steps perceive additional information available related to the current question.

The agent can interact with these sources to perceive the text contained within, which can be text mined
using NLP for axioms which can be checked using the agent's internal ontology.


# State

The state space should consider all the information that the agent has previously queried.

If an conflict occurs, the agent needs to consider which of the sources some piece of information came from,
and then rate each of the sources based on some metric (TBD).