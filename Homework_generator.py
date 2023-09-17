import openai
import os
import base64
import streamlit as st
import pygsheets
import pandas as pd





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
    st.info('''This is a demo version of a platform that saves teacher's time and make students excited about the study process by generating engaging projects that might be a homework or in-class activity.''')
    st.title('Feedback:')
    st.info('Please send purchase requests and feedback to oribo.official@gmail.com')

# English and German content dictionaries
content = {
    "English": {
        "title": "Project Maker",
        "subheader": "Please give us some info about the project you want to make:",
        "input1": "What topic and main idea do you want to explore with the students?",
        "input2": "How old are the students or what grade are they in?",
        "input3": "How does this topic fit with what you are currently teaching, and what do the students already know about it?",
        "input4": "Should extra materials be used?",
        "input5": "Should it be a group or solo project?",
        "input6": "How much time should children spend on project?",
        "button": "Create Project",

    },
    "German": {
        "title": "Projektersteller",
        "subheader": "Bitte geben Sie uns einige Infos zum Projekt, das Sie erstellen möchten:",
        "input1": "Welches Thema und welche Hauptidee möchten Sie mit den Schülern erkunden?",
        "input2": "Wie alt sind die Schüler oder in welcher Klasse sind sie?",
        "input3": "Wie passt dieses Thema zu dem, was Sie derzeit unterrichten, und was wissen die Schüler bereits darüber?",
        "input4": "Sollten zusätzliche Materialien verwendet werden?",
        "input5": "Soll es ein Gruppen- oder Einzelprojekt sein?",
        "input6": "Wie viel Zeit sollte das Projekt in Anspruch nehmen?",
        "button": "Projekt erstellen",
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
#info4 = st.selectbox(selected_content["input4"], ["No", "Yes"])
#info5 = st.selectbox(selected_content["input5"], ["Solo", "Group"])  # Adjusted to dropdown menu
info6 = st.text_input(selected_content["input6"])  # Adjusted to text input





questions_and_answers = [
    {"question": selected_content["input1"], "answer": info1},
    {"question": selected_content["input2"], "answer": info2},
    {"question": selected_content["input3"], "answer": info3},
    # {"question": selected_content["input4"], "answer": info4},
    # {"question": selected_content["input5"], "answer": info5},
    {"question": selected_content["input6"], "answer": info6},
]

# Button to generate life experience
if st.button(selected_content["button"]):
    with st.spinner('Generating the project...'):
        # Prompt for GPT-4
        messages = [
            {"role": "system", "content":
                f"""
                **--- Your Role ---**
                Rapidly changing world requires a new education paradigm.
                Your life mission is to bring a project-oriented learning into education to craft assignments for 
                students based on the input from user.
                Focus the project on what really matters to the development of students: their disposition towards learning and complexity, their ability to work effectively in teams, and their capacity to make ethical decisions.
                Don't break your role under any conditions. 
                Don't reply for requests you think don't suit to your role. 
                

                
                Follow the guidelines below to develop a project for the students:
        
                **--- Important Guidelines ---**
        
                1. **Problem Definition**:
                   - Project must be centered around concrete problem and make sense. Students should feel that they solve a real problem.
                   - Phrase the task in a way that students must find some pieces of information themselves using deduction. (Note: Do not explicitly mention this in the task).
                   - It shouldn't be just a boring task. The outcome should be a complete product that students can add to their protfolio.
                   - Provide all necessary information or data for calculations. If some data can be obtained from the internet search, suggest students to find it themselves.
                   - Provide a clear description what the outcome should be.
                
                2. **Teacher's Guide**:
                   - Advice the teacher to tell students that if some information pieces are missing, they can use their research skill to them find out. 
                   - Provide a detailed and clear instruction on what teacher should do to perform the project.
                   - Provide an example of the solution for the teacher.

                """
             },
            {"role": "user", "content": f"""I am a teacher. Here is information about my students: <{questions_and_answers}>. 
            Please generate a project in {language_selection} that I can give to my students."""}
        ]

        # Make API call to GPT-4
        model_engine = "gpt-4"  # Use the appropriate GPT-4 model engine
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages,
            temperature=0.8
        )


        # Extract and display the generated text
        generated_experience = response['choices'][0]['message']['content'].strip()
        if generated_experience:
            st.markdown(generated_experience)

            # authorization
            gc = pygsheets.authorize(service_account_file='service_account.json')

            # Create empty dataframe
            df = pd.DataFrame()

            # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
            sh = gc.open('oribo')

            # Select the first sheet
            wks = sh[0]

            # Get all values in the sheet
            all_values = wks.get_all_values()

            # Count the number of non-empty rows
            num_rows = sum(1 for row in all_values if any(cell for cell in row))

            df = pd.DataFrame()
            df['questions_and_answers'] = [f'''{questions_and_answers}''']
            df['gpt-reply'] = [f'''{generated_experience}''']

            # If the sheet is empty, set the dataframe from cell B2 (which corresponds to (1,1) in zero-indexed notation)
            if num_rows == 0:
                wks.set_dataframe(df, (1, 1))
            else:
                # Otherwise, add the data in the next available rows
                wks.set_dataframe(df, (num_rows + 1, 1))


        else:
            st.error('The generated content is empty. Please try again.')
