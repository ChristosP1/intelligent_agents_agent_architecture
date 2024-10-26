import streamlit as st
from agent import Agent, Env, Prompt  

st.title("Statement Validation")
st.write("Enter a statement for the agent to evaluate it.")

# Text input for user statement
user_statement = st.text_input("Enter your statement:")

# Button to process the statement
if st.button("Process", type='primary'):
    if user_statement:
        # Initialize environment and agent
        env = Env()
        env.set_prompt(Prompt(user_statement))
        agent = Agent(env)
        
        # Run the agent's reasoning process
        agent.perceive()
        agent.reason()
        agent.perceive()
        agent.reason()
        
        st.write(f"Query: {agent.sparql_queries}")
        # display the querying output (Temporary)
        st.write(f"Querying output: {agent.outcome}")
        
        # Display the results
        if agent.truthval is not None:
            st.write("Truth Value:", agent.truthval)
        else:
            st.write("Truth Value: Not determined")
        
        if agent.answer:
            st.write("Answer:", agent.answer)
        
        if agent.explanation:
            st.write("Explanation:", agent.explanation)
    else:
        st.warning("Please enter a statement to process.")
