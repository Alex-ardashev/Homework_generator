import streamlit as st
import openai
import os

# Initialize the GPT-4 API client
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Title of the Streamlit app
st.title('Homework generator')

# Collecting user information
st.header('Homework generator')
st.subheader('Write homework criteria:')
info = st.text_input('Key topic or concept that you have learned with kids?')
info1 = st.text_input('Class age?')
info2 = st.text_input('Time kids should spend?')
info3 = st.text_input('Should kids buy/bring anything additional for the project?')
info4 = st.text_input('How does this particular concept or topic fit into your curriculum and what do students already know about the topic?')

questions_ands = [
    {"question": "Key topic or concept that you have learned with kids?", "answer": info},
    {"question": "Class age?", "answer": info1},
    {"question": "Time kids should spend?", "answer": info2},
    {"question": "Should kids buy/bring anything additional for the project?", "answer": info3},
    {"question": "How does this particular concept or topic fit into your curriculum and what do students already know about the topic?", "answer": info4},
]

# Button to generate life experience
if st.button('Generate Homeworks'):

    # Prompt for GPT-4
    messages = [
        {"role": "system", "content": """
        You are a teacher assistant. The teacher enters the concept he wants to teach kids and then a homework is being created.
         The homework should be in form of a practical real-world project where the concept teacher explained should be used as a tool to solve the real-world problem."""
         },
        {"role": "user", "content": f"Please generate a concrete project that I can print and give to my kids. Here is the info about my kids {questions_ands}. Make the project title interesting"}
    ]

    # Make API call to GPT-4
    model_engine = "gpt-4"  # Use the appropriate GPT-4 model engine
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )

    #st.write(questions_ands)

    # Extract and display the generated text
    generated_experience = response['choices'][0]['message']['content'].strip()
    if generated_experience:
        st.markdown(generated_experience)
    else:
        st.error('The generated content is empty. Please try again.')
