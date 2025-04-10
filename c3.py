import streamlit as st

# Initialize session state for slide tracking
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

# Define slides content
slides = [
    {"title": "Fossil fuels", "content": "This is the first slide!"},
    {"title": "fugitive", "content": "Here is some more information."},
    {"title": "electricity", "content": "Final thoughts go here."},
    {"title": "water", "content": "hi"  },
    {"title": "waste", "content": "hi"  },
    {"title": "travel", "content": "ki" },
    {"title": "offset", "content": "gh" }

]

# Function to go to the next slide
def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

# Function to go to the previous slide
def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

# Display slide
current_slide = slides[st.session_state.slide_index]
st.title(current_slide["title"])
st.write(current_slide["content"])

# Navigation buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.slide_index > 0:
        st.button("Previous", on_click=prev_slide)
with col2:
    if st.session_state.slide_index < len(slides) - 1:
        st.button("Next", on_click=next_slide)

