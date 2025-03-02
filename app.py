import inspect

# Monkey-patch inspect.getfile to handle built-in objects.
_original_getfile = inspect.getfile

def safe_getfile(object, *args, **kwargs):
    try:
        return _original_getfile(object, *args, **kwargs)
    except TypeError:
        # Return a dummy file path if object is built-in.
        return "<built-in>"

inspect.getfile = safe_getfile

import streamlit as st
import os
import pdfkit  
from bs4 import BeautifulSoup  
from crew import StoryTellingCrew, clean_filename

# Ensure the assets directory exists
os.makedirs("assets", exist_ok=True)

def clean_html_content(html_content):
    """
    Cleans the HTML content by removing any '```html' at the start
    or '```' at the end of the string.
    """
    if not isinstance(html_content, str):
        raise ValueError("HTML content must be a string.")
    
    marker_start = "```html"
    marker_end = "```"
    if html_content.startswith(marker_start):
        html_content = html_content[len(marker_start):]
    if html_content.endswith(marker_end):
        html_content = html_content[:-len(marker_end)]
    return html_content.strip()

def generate_story(input_topic, file_topic=None):
    """
    Runs the CrewAI pipeline to generate a story.
    Uses input_topic for processing and file_topic for file naming.
    """
    if not file_topic:
        file_topic = input_topic
    inputs = {"topic": input_topic}
    try:
        st.info("🔍 Initializing AI Storytelling Crew...")
        # Pass file_topic as the second parameter
        story_crew = StoryTellingCrew(input_topic, file_topic)
        st.info("📝 Generating story... Please wait.")
        story_crew.crew().kickoff(inputs=inputs)
        output_filename = os.path.join("assets", clean_filename(file_topic))
        return output_filename
    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")
        return None

def read_and_clean_file(file_path):
    """
    Reads the content of the file, cleans it, and returns the cleaned content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return clean_html_content(content)
    except Exception as e:
        st.error(f"❌ Error reading or cleaning the file: {e}")
        return None

def remove_loading_elements(html_content):
    """
    Remove elements that may show a loading sign (e.g., spinners, loaders)
    which can blur the rest of the PDF.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for class_name in ["spinner", "loader", "loading", "loading-spinner"]:
        for el in soup.find_all(class_=class_name):
            el.decompose()
        for el in soup.find_all(id=class_name):
            el.decompose()
    return str(soup)

def export_html_to_pdf(html_content, pdf_output_path):
    """
    Converts the provided HTML content into a PDF file at the given path with styling options.
    Updated to remove loading/sign elements before conversion.
    """
    cleaned_html = remove_loading_elements(html_content)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        pdfkit.from_string(cleaned_html, pdf_output_path, options=options, css=css_path)
    else:
        pdfkit.from_string(cleaned_html, pdf_output_path, options=options)
    return pdf_output_path

def display_story():
    st.write("### Story Display Options:")

    # Icon control panel: expand and minimize
    with st.container():
        cols = st.columns(2)
        if cols[0].button("⛶", key="expand_story", help="Expand story area to full page"):
            st.session_state.iframe_height = 1200
        if cols[1].button("🗕", key="minimize_story", help="Minimize story view area"):
            st.session_state.iframe_height = 400

    # Fine-tune the height with the slider below the icon buttons.
    new_height = st.slider(
        "Adjust story display height:",
        400, 1200,
        st.session_state.iframe_height,
        step=50,
        key="slider_height"
    )
    st.session_state.iframe_height = new_height

    st.write("### 📖 Your Story:")
    st.components.v1.html(
        st.session_state.story_html,
        height=st.session_state.iframe_height,
        scrolling=True
    )

    # Download button for the story file.
    try:
        with open(st.session_state.story_filename, "r", encoding="utf-8") as file:
            file_data = file.read()
        st.download_button(
            label="📥 Download HTML Story",
            data=file_data,
            file_name=os.path.basename(st.session_state.story_filename),
            mime="text/html"
        )
    except Exception as e:
        st.error(f"❌ Error loading file for download: {e}")

    # New PDF Export section
    if st.button("Export to PDF"):
        try:
            pdf_filename = st.session_state.story_filename.replace(".html", ".pdf")
            export_html_to_pdf(st.session_state.story_html, pdf_filename)
            with open(pdf_filename, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            st.download_button(
                label="📥 Download PDF Story",
                data=pdf_data,
                file_name=os.path.basename(pdf_filename),
                mime="application/pdf"
            )
            st.success("✅ PDF exported successfully!")
        except Exception as e:
            st.error(f"❌ Error exporting to PDF: {e}")

def generate_story_ui():
    st.write("💡 **Enter a topic, and I'll generate a captivating story for you!**")

    suggested_topics = [
        "The Enchanted Kingdom of Eldoria",
        "Beyond the Stars",
        "Love Amidst the Autumn Leaves",
        "The Haunting of Blackwood Manor",
        "Shadows in the Fog",
        "The Rebellion's Rise",
        "The Quest for the Lost Treasure",
        "Neon Dreams and Digital Nightmares",
        "Legends of the Forgotten Gods",
        "The Misadventures of a Clumsy Magician"
    ]

    option = st.selectbox(
        "Choose a suggested topic or select 'Custom Topic' to enter your own:",
        ["Custom Topic"] + suggested_topics,
        key="topic_selector"
    )
    if option == "Custom Topic":
        topic = st.text_input(
            "🎭 Enter your custom topic:",
            key="custom_topic",
            placeholder="E.g., A New Dawn for AI-Driven Art"
        )
    else:
        topic = option

    # New background input for additional context
    background = st.text_input(
        "📝 (Optional) Enter background information:",
        key="background_info",
        placeholder="Add extra context to enrich the story..."
    )

    if topic and topic.strip():
        if st.button("🚀 Generate Story", key="generate_story"):
            combined_topic = f"{topic} {background}" if background.strip() else topic
            with st.spinner("⏳ AI is crafting your story... Please wait."):
                # Pass combined_topic for processing and original topic for filename.
                output_filename = generate_story(combined_topic, topic)
            if output_filename:
                cleaned_content = read_and_clean_file(output_filename)
                if cleaned_content is not None:
                    with open(output_filename, "w", encoding="utf-8") as file:
                        file.write(cleaned_content)
                if cleaned_content and cleaned_content.strip().startswith("<"):
                    st.success("✅ Story generated successfully!")
                    st.write(f"📂 Story saved at: `{output_filename}`")
                    st.session_state.story_html = cleaned_content
                    st.session_state.story_filename = output_filename
                else:
                    st.error("❌ Invalid HTML content returned. Please try again.")
    else:
        st.warning("⚠️ Please select or enter a topic to generate a story.")

    if "story_html" in st.session_state and st.session_state.story_html:
        if "iframe_height" not in st.session_state:
            st.session_state.iframe_height = 600
        display_story()

def load_existing_story_ui():
    st.write("📂 **Load an Existing Story**")
    asset_files = os.listdir("assets")
    if not asset_files:
        st.warning("No stories available to load. Please generate a story first!")
        return

    selected_file = st.selectbox("Select a story to read:", asset_files, key="existing_story_selector")
    if st.button("📖 Load Story", key="load_story"):
        full_file_path = os.path.join("assets", selected_file)
        cleaned_content = read_and_clean_file(full_file_path)
        if cleaned_content:
            # Write the cleaned content back to disk to ensure a clean file.
            with open(full_file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_content)
            st.success("✅ Story loaded successfully and cleaned!")
            st.session_state.story_html = cleaned_content
            st.session_state.story_filename = full_file_path
        else:
            st.error("❌ Error loading the story.")
    
    if "story_html" in st.session_state and st.session_state.story_html:
        if "iframe_height" not in st.session_state:
            st.session_state.iframe_height = 600
        display_story()

def main():
    st.set_page_config(
        page_title="AI Story Creator",
        page_icon="📚",
        layout="wide"
    )
    st.title("📚 AI-Powered Story Creator")

    # Initialize session state variables if they don't exist.
    if "iframe_height" not in st.session_state:
        st.session_state.iframe_height = 600
    if "story_html" not in st.session_state:
        st.session_state.story_html = None
    if "story_filename" not in st.session_state:
        st.session_state.story_filename = None

    mode = st.sidebar.radio("Select Mode:", ["Generate Story", "Read Existing Story"], key="mode_selector")
    if mode == "Generate Story":
        generate_story_ui()
    elif mode == "Read Existing Story":
        load_existing_story_ui()

if __name__ == "__main__":
    main()