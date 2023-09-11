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
        "title": "Project Maker",
        "subheader": "Please give us some info about the project you want to make:",
        "input1": "What topic and main idea do you want to explore with the students?",
        "input2": "How old are the students or what grade are they in?",
        "input3": "How does this topic fit with what you are currently teaching, and what do the students already know about it?",
        "input4": "Should students use extra materials or resources?",
        "input5": "Should it be a group or solo project?",  # Adjusted
        "input6": "Estimated time for project",  # Adjusted
        "button": "Create Project"
    },
    "German": {
        "title": "Projektersteller",
        "subheader": "Bitte geben Sie uns einige Infos zum Projekt, das Sie erstellen möchten:",
        "input1": "Welches Thema und welche Hauptidee möchten Sie mit den Schülern erkunden?",
        "input2": "Wie alt sind die Schüler oder in welcher Klasse sind sie?",
        "input3": "Wie passt dieses Thema zu dem, was Sie derzeit unterrichten, und was wissen die Schüler bereits darüber?",
        "input4": "Sollten die Schüler zusätzliche Materialien oder Ressourcen verwenden?",
        "input5": "Soll es ein Gruppen- oder Einzelprojekt sein?",  # Adjusted
        "input6": "Geschätzte Zeit für das Projekt",  # Adjusted
        "button": "Projekt erstellen"
    }
}

# Set the language content based on the selection
selected_content = content[language_selection]

# Display the content
st.title(selected_content["title"])
st.subheader(selected_content["subheader"])
info1 = st.text_input(selected_content["input1"])
info2 = st.text_input(selected_content["input2"])
info3 = st.text_area(selected_content["input3"])
info4 = st.selectbox(selected_content["input4"], ["yes", "no"])
info5 = st.selectbox(selected_content["input5"], ["yes", "no"])  # Adjusted to dropdown menu
info6 = st.text_input(selected_content["input6"])  # Adjusted to text input





questions_and_answers = [
    {"question": selected_content["input1"], "answer": info1},
    {"question": selected_content["input2"], "answer": info2},
    {"question": selected_content["input3"], "answer": info3},
    {"question": selected_content["input4"], "answer": info4},
    {"question": selected_content["input5"], "answer": info5},
    {"question": selected_content["input6"], "answer": info6},
]

# Button to generate life experience
if st.button(selected_content["button"]):
    with st.spinner('Generating the project...'):
        # Prompt for GPT-4
        messages = [
            {"role": "system", "content":
                f"""

                You are a Teacher Assistant with expertise in integrating gamification elements into education to craft world-class project assignments. 
                
                Here is the info about students {questions_and_answers}
                
                Follow the guidelines below to develop a project for the students:
        
                **--- Important Guidelines ---**
        
                1. **Problem Definition**:
                   - Develop a project centered around a clear, concrete problem. It should be more complicated and interesting than just a quiz from study books.
                   - Ensure the problem necessitates the application of the recently discussed concept (Note: Do not explicitly mention this concept in the task).
                   - Provide all necessary data or numerical information for calculations.
                   - Feel free to integrate other concepts that should have been learned via study program before (Note: Do not explicitly mention this concept in the task).
                
                2. **Desired outcome**:
                    - Provide information for students on what outcome should be.     
        
                3. **Hints for Students. Optional to provide**:
                   - Describe the task and expected outcome in detail.
        
                4. **Teacher's Guide**:
                   - Outline guidelines and a potential solution with calculations for the teacher.
        
                > Your task is to craft a project following the guidelines above. After detailing the project task for students, provide a separate section below it, containing guidelines and a potential solution with numbers for the teacher to refer to during assessment.
                """
             },
            {"role": "user", "content": f"I am a teacher. Please generate a concrete project in {language_selection} that I can give to students."}
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




#add whether kids should use additional materials