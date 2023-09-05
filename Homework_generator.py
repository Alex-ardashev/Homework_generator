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

# Initialize the GPT-4 API client
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Language selection
language_selection = st.sidebar.selectbox('Select Language', ['English', 'German'])

# English and German content dictionaries
content = {
    "English": {
        "title": "Homework Creator",
        "subheader": "Kindly furnish us with details regarding the assignment you wish to create:",
        "input1": "What is the subject and primary concept you wish to focus on with the students?",
        "input2": "What is the age group or class level of the students?",
        "input3": "How does this concept integrate with your current curriculum, and what prior knowledge do the students have on this topic?",
        "input4": "Additional Details",
        "help4": "Feel free to describe any specific aspects or requirements for the project here. You might include details such as whether it is a group or individual project, the particular theme or focus of the project, or any custom expectations regarding the outcome or deliverables of the project",
        "button": "Generate Homework"
    },
    "German": {
        "title": "Hausaufgaben Ersteller",
        "subheader": "Bitte geben Sie uns Einzelheiten zur Aufgabe, die Sie erstellen möchten:",
        "input1": "Welches ist das Thema und der primäre Schwerpunkt, den Sie mit den Schülern bearbeiten möchten?",
        "input2": "Welche Altersgruppe oder Klassenstufe haben die Schüler?",
        "input3": "Wie integriert sich dieses Konzept in Ihren aktuellen Lehrplan und welche Vorkenntnisse haben die Schüler zu diesem Thema?",
        "input4": "Zusätzliche Details",
        "help4": "Beschreiben Sie hier gerne spezifische Aspekte oder Anforderungen des Projekts. Sie könnten Details angeben wie, ob es sich um ein Gruppen- oder Einzelprojekt handelt, das spezielle Thema oder den Schwerpunkt des Projekts, oder jegliche individuelle Erwartungen bezüglich des Ergebnisses oder der Projektergebnisse",
        "button": "Hausaufgaben generieren"
    }
}

# Set the language content based on the selection
selected_content = content[language_selection]

# Display the content
st.title(selected_content["title"])
st.subheader(selected_content["subheader"])
info = st.text_input(selected_content["input1"])
info1 = st.text_input(selected_content["input2"])
info2 = st.text_area(selected_content["input3"])
info3 = st.text_input(selected_content["input4"], help=selected_content["help4"])



questions_and_answers = [
    {"question": selected_content["input1"], "answer": info},
    {"question": selected_content["input2"], "answer": info1},
    {"question": selected_content["input3"], "answer": info2},
    {"question": selected_content["input4"], "answer": info3},
]

# Button to generate life experience
if st.button(selected_content["button"]):
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
- **List of prequisites**: (if there are)Provide a detailed description of the things that students have to prepare in order to make the project. 
- **List of Actions**: Outline a series of steps or actions that the students need to take to successfully complete the project.
- **Expected Outcome**: Specify what students should submit to the teacher as proof of their learning and understanding of the concept.

Encourage the students to explore their creativity and to think out of the box while working on the project.

"""
         },
        {"role": "user", "content": f"Please generate a concrete project in {language_selection} that I can print and give to my kids. Here is the info about my kids {questions_and_answers}"}
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

