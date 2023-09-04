import streamlit as st
import openai


# Initialize the GPT-4 API client
openai.api_key = "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"

# Title of the Streamlit app
st.title('Life Experience & Opportunity Awareness Generator')

# Collecting user information
st.header('Experience generator')

st.subheader('Write some information about yourself:')
st.write("Some questions to answer:")
st.markdown("- Where are you based?")
st.markdown("- Where do you study or What do you do for work?")
st.markdown("- What are your hobbies and interests?")
st.markdown("- What subjects can you talk about for hours?")
st.markdown("- What are some goals you have?")
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)

info = st.text_area('Write the description of yourself here')

# Button to generate life experience
if st.button('Generate Life Experience'):

    st.header('Suggested Life Experience to Increase Awareness')

    # Prompt for GPT-4
    messages = [
        {"role": "system", "content": "Your goal is to make the person aware of opportunities that can improve their life but the person is not aware of them yet. It also might be outside of the persons' professional area."},
        {"role": "user", "content": f"Here is info about me: {info}. Hi, can you please generate a life experience for every day that would increase my awareness of opportunities around me?"}
    ]

    # Make API call to GPT-4
    model_engine = "gpt-4"  # Use the appropriate GPT-4 model engine
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )

    # Extract and display the generated text
    generated_experience = response['choices'][0]['message']['content'].strip()
    st.write(generated_experience)
