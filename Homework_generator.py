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
    background-color: white; /* Changed to white to resemble A4 paper */
}}
.stTextInput input {{
    border-radius: 15px;
    border: 1px solid #ccc; /* Changed to a neutral border color */
    background-color: #f9f9f9; /* Changed to a light gray background color */
}}
.stTextArea textarea {{
    border-radius: 15px;
    border: 1px solid #ccc; /* Changed to a neutral border color */
    background-color: #f9f9f9; /* Changed to a light gray background color */
}}
.stButton>button {{
    border-radius: 20px;
    background-color: #007bff; /* Changed to a neutral button color */
    border: none;
    color: white;
    font-size: 1em;
}}
h1 {{
    color: #000; /* Changed to black color for better readability */
}}
.markdown-text-container {{
    font-family: 'Arial', sans-serif; /* Changed to Arial for a more professional look */
    color: #000; /* Changed to black color for better readability */
}}
</style>

"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize the GPT-4 API client
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Language selection
language_selection = st.sidebar.selectbox('Select Language', ['English', 'German'])
with st.sidebar:
    st.title('Feedback:')
    st.info('Please send your feedback to oribo.official@gmail.com')

# English and German content dictionaries
content = {
    "English": {
        "title": "Homework Creator",
        "subheader": "Kindly furnish us with details regarding the assignment you wish to create:",
        "input1": "What is the subject and primary concept you wish to focus on with the students?",
        "input2": "What is the age group or class level of the students?",
        "input3": "How does this concept integrate with your current curriculum, and what prior knowledge do the students have on this topic?",
        "input4": "Additional Details",
        "placeholder4": "Execution time, group/individual project etc",
        "button": "Generate Homework"
    },
    "German": {
        "title": "Hausaufgaben Ersteller",
        "subheader": "Bitte geben Sie uns Details zur Aufgabe, die Sie erstellen möchten:",
        "input1": "Um welches Thema und welchen zentralen Aspekt möchten Sie sich mit den Schülern konzentrieren?",
        "input2": "Wie alt sind die Schüler oder in welcher Klassenstufe befinden sie sich?",
        "input3": "Wie fügt sich dieses Konzept in Ihren aktuellen Lehrplan ein und welche Vorkenntnisse haben die Schüler zu diesem Thema?",
        "input4": "Zusätzliche Details",
        "placeholder4": "Ausführungszeit, Gruppen-/Einzelprojekt usw.",
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
info3 = st.text_area(selected_content["input4"], placeholder=selected_content["placeholder4"])



questions_and_answers = [
    {"question": selected_content["input1"], "answer": info},
    {"question": selected_content["input2"], "answer": info1},
    {"question": selected_content["input3"], "answer": info2},
    {"question": selected_content["input4"], "answer": info3},
]

# Button to generate life experience
if st.button(selected_content["button"]):
    with st.spinner('Generating homework...'):
        # Prompt for GPT-4
        messages = [
            {"role": "system", "content":
                """

                You are a Teacher Assistant with expertise in integrating gamification elements into education to craft world-class homework assignments. Follow the guidelines below to develop a project for the students:
        
                **--- Important Guidelines ---**
        
                1. **Problem Definition**:
                   - Develop a project centered around a clear, concrete problem.
                   - Ensure the problem necessitates the application of the recently discussed concept (Note: Do not explicitly mention this concept in the task).
                   - Provide all necessary data or numerical information for calculations.
                   - Feel free to integrate other concepts that should've been learned via k-12 program before (Note: Do not explicitly mention this concept in the task).
        
                2. **Project Task for Students**:
                   - Describe the task and expected outcome in detail.
        
                3. **Teacher's Guide**:
                   - Outline guidelines and a potential solution with calculations for the teacher.
        
                4. **Formatting**:
                   - Ensure the document is formatted for easy readability and printing.
        
                > Your task is to craft a project following the guidelines above. After detailing the project task for students, provide a separate section below it, containing guidelines and a potential solution with numbers for the teacher to refer to during assessment.
                """
             },
            {"role": "user", "content": f"I am a teacher. Please generate a concrete project in {language_selection} that I can give to students. Here is the info about my students {questions_and_answers}"}
        ]

        # Make API call to GPT-4
        model_engine = "gpt-4"  # Use the appropriate GPT-4 model engine
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages
        )


        # Extract and display the generated text
        generated_experience = response['choices'][0]['message']['content'].strip()
        if generated_experience:
            st.write('Please copy the details below, paste them into your document, and proceed to print.')
            st.markdown(generated_experience)
        else:
            st.error('The generated content is empty. Please try again.')

