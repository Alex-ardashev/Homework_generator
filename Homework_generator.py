import streamlit as st
import openai
import os
import base64


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: center;
background-repeat: repeat;
background-attachment: local;
}}
body {{
    background-color: pink;
}}
.stTextInput input {{
    border-radius: 15px;
    border: 1px solid #ff99cc;
    background-color: #ffebf7;
}}
.stTextArea textarea {{
    border-radius: 15px;
    border: 1px solid #ff99cc;
    background-color: #ffebf7;
}}
.stButton>button {{
    border-radius: 20px;
    background-color: #ff99cc;
    border: none;
    color: white;
    font-size: 1em;
}}
h1 {{
    color: #ff66b2;
}}
.markdown-text-container {{
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #ff3399;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# [data-testid="stSidebar"] > div:first-child {{
# background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
# background-position: center;
# background-repeat: no-repeat;
# background-attachment: fixed;
# }}
# [data-testid="stHeader"] {{
# background: rgba(0,0,0,0);
# }}
#
# [data-testid="stToolbar"] {{
# right: 2rem;
# }}



# Initialize the GPT-4 API client
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Title of the Streamlit app
st.title('Homework Creator')

st.subheader('Kindly furnish us with details regarding the assignment you wish to create:')
info = st.text_input('What is the primary topic or concept you wish to focus on with the students?')
info1 = st.text_input('What is the age group or class level of the students?')
info2 = st.text_input('Approximately how much time should students dedicate to this assignment?')
info3 = st.text_input('Do students need to purchase or bring any supplementary materials for the project?')
info4 = st.text_area('How does this topic or concept integrate with your current curriculum, and what prior knowledge do the students have on this topic?')

questions_and_answers = [
    {"question": "What is the primary topic or concept you wish to focus on with the students?", "answer": info},
    {"question": "What is the age group or class level of the students?", "answer": info1},
    {"question": "Approximately how much time should students dedicate to this assignment?", "answer": info2},
    {"question": "Do students need to purchase or bring any supplementary materials for the project?", "answer": info3},
    {"question": "How does this topic or concept integrate with your current curriculum, and what prior knowledge do the students have on this topic?", "answer": info4},
]


# Button to generate life experience
if st.button('Generate Homework'):

    # Prompt for GPT-4
    messages = [
        {"role": "system", "content": """
        You are a teacher assistant. The teacher enters the concept he wants to teach kids and then a homework is being created. Always provide response in markdown.
         The homework should be in form of a practical real-world project where the concept teacher explained should be used as a tool to solve the real-world problem."""
         },
        {"role": "user", "content": f"Please generate a concrete project that I can print and give to my kids. Here is the info about my kids {questions_and_answers}. Make the project title interesting"}
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
        st.write('Please copy the details below, paste them into your document, and proceed to print.')
        st.markdown(generated_experience)
    else:
        st.error('The generated content is empty. Please try again.')
