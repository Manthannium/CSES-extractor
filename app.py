import streamlit as st
import extractor

st.title("CSES Extractor")

username = st.text_input("Enter username:")
password = st.text_input("Enter password:", type="password")
permission = st.checkbox("I permit to extract my solutions")

st.balloons()

def extract():
    if username and password and permission:
        with st.spinner(text="Extracting..."):
            extractor.run(username, password)
            st.success("Done")
            st.snow()
        
        with open("compressed.zip", "rb") as fp:
            btn = st.download_button(
                label = "Download ZIP",
                data = fp,
                file_name = "compressed.zip",
                mime = "application/zip"
            )
        feedback = st.feedback("thumbs")
    else:
        if not username:
            st.warning("Please enter username")
        elif not password:
            st.warning("Please enter password")
        elif not permission:
            st.warning("Please allow permission to extract")

if st.button("Extract"):
    extract()
