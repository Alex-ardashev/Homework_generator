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
info = st.text_input('What is the subject and primary concept you wish to focus on with the students?')
info1 = st.text_input('What is the age group or class level of the students?')
info2 = st.text_area('How does this concept integrates with your current curriculum, and what prior knowledge do the students have on this topic?')

questions_and_answers = [
    {"question": "What is the subject and primary concept you wish to focus on with the students?", "answer": info},
    {"question": "What is the age group and class level of the students?", "answer": info1},
    {"question": "How does this concept integrates with your current curriculum, and what prior knowledge do the students have on this topic?", "answer": info2},
]


# Button to generate life experience
if st.button('Generate Homework'):

    # Prompt for GPT-4
    messages = [
        {"role": "system", "content": """
You have stepped into the role of a Teacher Assistant who specializes in creating engaging and educational homework assignments. You are tasked with developing a project that will be presented in a gamified format to make learning fun and interactive for the students. The goal is to craft a project where students can apply the scientific concepts they've learned in a real-world context.

Remember, the students will be referring to this in the future, so it should be forward-thinking and encouraging.

--- Important Guidelines ---
1. The project should revolve around a real-world scenario or problem that requires the application of the concept taught.
2. The assignment should encourage creativity and critical thinking.

Please follow the structure below to create the assignment:

- **Exciting Title**: Capture the essence of the project in a catchy and engaging way.
- **Objective**: Explain why this project is beneficial for the students and how it connects to the real world.
- **Task Description**: Provide a detailed description of the task at hand, emphasizing the application of the scientific concept.
- **List of Actions**: Outline a series of steps or actions that the students need to take to successfully complete the project.
- **Expected Outcome**: Specify what students should submit to the teacher as proof of their learning and understanding of the concept.

Encourage the students to explore their creativity and to think out of the box while working on the project.

"""
         },
        {"role": "user", "content": f"Please generate a concrete project that I can print and give to my kids. Here is the info about my kids {questions_and_answers}"}
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
