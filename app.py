import streamlit as st
from agent import Agent, Env, Prompt  
import time
from llm_utils import generate_scenario_explanation


def update_progress(progress_bar, progress_value, delay=0.3):
    """
    Update the progress bar and yield control back to Streamlit.
    :param progress_bar: The progress bar component created with st.progress.
    :param progress_value: The progress value to set.
    :param delay: Time to sleep to simulate yielding control.
    """
    if progress_bar:
        progress_bar.progress(progress_value)  # Use progress() method to update progress bar
        time.sleep(delay)  # Yield control to Streamlit to refresh UI
        

# Title and description
st.title("Statement Validation")

# Dropdown for pre-written statements
statements = [
    "Dehydration has symptom headache and it is true that we should visitdoctor.",
    "Find injury that is caused by football and has symptom headache.",
    "Find injury that has symptom headache and it is true that we should visit doctor.",
    "Find symptoms that are caused by concussion.",
    "There are frogsandtoads that it is false that they are poisonous and are eatenby humans.",
    "Some nutricients are present in frogsandtoads.",
    "There are recipes that have ingredient some frogsandtoads.",
    "There is some location that has animal shark and has sport volleyball.",
    "Is there some vegetarian dish that has an ingredient that is Animal Seafood or Meat and is eaten by sharks.",
    "There are animals that are locatedin Amazon and have diet humans.",
    "Swimming is repetitivenoncontact sport and the caloriesburnedperhour are more than 500.",
]

# Dropdown and text input
# selected_statement = st.selectbox("Select a statement:", options=["Select"] + statements)
# user_statement = st.text_input("Or enter your own statement:")


# Dropdown for pre-written scenarios
scenarios = [
    "Injury or Dehydration.",
    "Frog-based Recipes.",
    "Shark Attack.",
    "Safe Swimming.",
]

# Dropdown and text input
selected_scenario = st.selectbox("Select a scenario:", options=["Select"] + scenarios)

scenario_description = {
    "injury_of_dehydration": "Evie had a busy day yesterday. She went to university, then afterwards she went to her 2-hour football training. During this training, she bumped into another player and hit her head. At night Evie has a bad headache. She reasons that, due to her busy day, she forgot to drink water, which is the reason for the headache. She decides to just sleep it off.",
    "frog_based_recipes": "Rinaldo Salvatore is attempting to cook a new dish involving a new type of meat, originating from frogs. Rinaldo has never tried this before, but a friend said that eating frog meat is perfectly safe, and he even said it is very nutritious. Rinaldo is excited to try it and is already thinking about other frog recipes he could make after this one. ",
    "shark_attack": "Sabrinah will be cooking food at volleyball camp but is fearful that sharks will steal any meat that is part of the dishes, so John tells them to cook vegetarian food.",
    "safe_swimming": "Lex is visiting the Amazon. He wants to go for a swim in the river, but suddenly realizes he does not know what dangers might lie beneath the surface. Lex decides that he thinks it is probably safe enough. He swims in the river for a few minutes, but because of the repetitive movements he quickly gets bored. After getting out of the water Lex feels super hungry because he burned so many calories while swimming."
}

if selected_scenario == scenarios[0]:
    st.markdown("#### Description")
    st.write(scenario_description["injury_of_dehydration"])
    scenario_statements = statements[:4] 
    st.markdown("#### Scenario statements:")
    for i, statement in enumerate(scenario_statements):
        st.write(F"{i+1}. {statement}")
elif selected_scenario == scenarios[1]:
    st.markdown("#### Description")
    st.write(scenario_description["frog_based_recipes"])
    scenario_statements = statements[4:7] 
    st.markdown("#### Scenario statements:")
    for i, statement in enumerate(scenario_statements):
        st.write(F"{i+1}. {statement}")
elif selected_scenario == scenarios[2]:
    st.markdown("#### Description")
    st.write(scenario_description["shark_attack"])
    scenario_statements = statements[7:9]
    st.markdown("#### Scenario statements:")
    for i, statement in enumerate(scenario_statements):
        st.write(F"{i+1}. {statement}")
elif selected_scenario == scenarios[3]:
    st.markdown("#### Description")
    st.write(scenario_description["safe_swimming"])
    scenario_statements = statements[9:]
    st.markdown("#### Scenario statements:")
    for i, statement in enumerate(scenario_statements):
        st.write(F"{i+1}. {statement}") 


# Determine the scenario to process
if selected_scenario != "Select":
    user_scenario = selected_scenario 
    
    
# Button to process the statement(s)
if st.button("Process", type='primary'):
    progress_bar = st.progress(0)
    env = Env()
    agent = Agent(env)
    
    # Initialize a placeholder for the progress bar
    progress_value = 5  # Starting point of the progress bar
    update_progress(progress_bar, progress_value)
    
    if selected_scenario != "Select":
        # Process statements relevant to the selected scenario
        results = agent.process_multiple_prompts(scenario_statements, progress_bar, progress_value)
        
        # Display the results for each statement
        i = 1
        true_count = 0
        false_count = 0
        
        ontology_sources = 0
        reddit_sources = 0
        openai_llm_sources = 0
        
        st.markdown("## Results")
        for prompt, result in results.items():
            truthval = result['truthval']
            source = result['source']
            
            if truthval == "True":
                true_count += 1
            elif truthval == "False":
                false_count += 1
                
            
            if source == "Ontology":
                ontology_sources += 1
            elif source == "Reddit":
                reddit_sources += 1
            else:
                openai_llm_sources += 1
            
            st.markdown(f"#### **Statement {i}:**")
            st.write(prompt)
            st.markdown(f"- **Truth Value:** {truthval}")
            st.markdown(f"- **Source:** {source}")
            st.markdown(f"- **Answer:** {result['answer']}")
            st.write("---")
            i += 1
        
        truth_percentage = true_count / len(scenario_statements)
        if truth_percentage > 0.8:
            overall_truth = "True"
        elif truth_percentage > 0.5:
            overall_truth = "Partially true"
        else:
            overall_truth = "False"
            
        
        # Display the count of True and False statements
        st.markdown("### Truth Value Counts:")
        st.write(f"**True Statements**: {true_count}")
        st.write(f"**False Statements**: {false_count}")
        st.write(f"**Truth percentage**: {truth_percentage}")
        st.write(f"**Not Determined Statements**: {len(results) - true_count - false_count}")
        st.write(f"**Sources**: Ontology ({ontology_sources}) || Reddit ({reddit_sources}) || OpenAI LLM ({openai_llm_sources})")
        
        st.write("--")
        
        # Format statements for the scenario explanation function
        statements_text = "\n".join([f"{i+1}. {statement}: {results[statement]['answer']}" for i, statement in enumerate(scenario_statements)])
        
        # Call the scenario explanation function
        explanation_result = generate_scenario_explanation(agent.llm, statements_text, overall_truth)

        # Display the final scenario explanation
        st.markdown("## Final Scenario Explanation")
        st.write(explanation_result)


        # Complete the progress bar
        update_progress(progress_bar, 100)
        time.sleep(1)
        progress_bar.empty()


