import streamlit as st
import requests
from bs4 import BeautifulSoup

def google_drive_search(query):
    search_url = f"https://www.google.com/search?q=site:drive.google.com+{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for g in soup.find_all('div', class_='g'):
            link = g.find('a', href=True)
            title = g.find('h3')
            if link and title:
                href = link['href']
                if "drive.google.com" in href:
                    url = href.split("&")[0].split("?q=")[-1]
                    results.append((title.text, url))
        
        return results
    else:
        return []

st.title("Drive Search Engine")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            results = google_drive_search(query)
        
        if results:
            st.success(f"Found {len(results)} results:")
            for title, link in results:
                st.markdown(f"[{title}]({link})")
        else:
            st.warning("No results found.")
    else:
        st.warning("Please enter a query.")

# Add footer with the creator's name
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: black;
    }
    </style>
    <div class="footer">
    Created by Deviprasad Shetty
    </div>
    """,
    unsafe_allow_html=True
)
