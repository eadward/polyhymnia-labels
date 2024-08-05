import streamlit as st
import pandas as pd

audio_css = " audio::-webkit-media-controls-time-remaining-display, \
                audio::-webkit-media-controls-current-time-display { \
                    max-width: 50%; \
                    max-height: 20px; \
                } "

st.set_page_config(layout="wide")

st.title("Polyhymnia Labels")


items = pd.read_csv("./data/items.csv")
tuples = pd.read_csv("./data/tuples.csv")


# song1 = items.loc[items.id==tuples['song1'][0]]
# st.audio(song1['url'], format="audio/wav")

col1, col2, col3, col4,_ = st.columns([1,1,1,1,4])

# st.markdown("<style>" + audio_css + "</style>", unsafe_allow_html=True)

with col1:
    st.subheader("Song 1")
    st.audio("./data/tracks/"+str(tuples['song1'][0])+".mp3", format="audio/wav")
with col2:
    st.subheader("Song 2")
    st.audio("./data/tracks/"+str(tuples['song2'][0])+".mp3", format="audio/wav")
with col3:
    st.subheader("Song 3")
    st.audio("./data/tracks/"+str(tuples['song3'][0])+".mp3", format="audio/wav")
with col4:
    st.subheader("Song 4")
    st.audio("./data/tracks/"+str(tuples['song4'][0])+".mp3", format="audio/wav")

st.header("Please listen to the four songs above and indicate …")

hA = st.radio(
    "Which track do you think that expresses the highest level of arousal?",
    ["Song 1", "Song 2", "Song 3", "Song 4"],
    horizontal=True,
    index=None,
)

lA = st.radio(
    "Which track do you think that expresses the lowest level of arousal?",
    ["Song 1", "Song 2", "Song 3", "Song 4"],
    horizontal=True,
    index=None,
)

hV = st.radio(
    "Which track do you think that expresses the highest level of valence?",
    ["Song 1", "Song 2", "Song 3", "Song 4"],
    horizontal=True,
    index=None,
)

lV = st.radio(
    "Which track do you think that expresses the lowest level of valence?",
    ["Song 1", "Song 2", "Song 3", "Song 4"],
    horizontal=True,
    index=None,
)

with st.expander("Help ..."):
    st.write('''
        .....
    ''')
    st.image("https://static.streamlit.io/examples/dice.jpg")