### **📚 AI Story Creator**  

### 🖋️ **Generate and Read AI-Powered Stories!**  

This **AI-powered storytelling application** uses **CrewAI** and **Streamlit** to generate immersive, culturally rich stories based on a user-provided topic. The AI-generated story is formatted into a **beautiful HTML page**, ready for reading and downloading.  

---

## **🎯 Features**  
✅ **Multi-Agent AI Workflow** – Uses CrewAI to handle research, planning, writing, and formatting.  
✅ **Cultural & Historical Accuracy** – Ensures stories are rich and authentic.  
✅ **Interactive Streamlit UI** – User-friendly interface for generating and downloading stories.  
✅ **Custom & Suggested Topics** – Choose from predefined topics or enter your own.  
✅ **Auto-Saving & Downloading** – Save stories as HTML files.  
✅ **Read previously generated stories** – Easily reload and view previously generated stories.  

---

## **🛠️ Installation Guide**  

You can set up this project using **Conda** or **virtual environments (venv)**.  

### 🔹 1️⃣ Clone the Repository  
```bash
git clone https://github.com/veerupandey/AI_story_teller.git
cd AI_story_teller
```

### 🔹 2️⃣ Choose a Setup Method  

#### **➡️ Using Conda (Recommended)**
```bash
conda create --name ai-story python=3.11
conda activate ai-story
pip install "crewai[tools]" streamlit beautifulsoup4 google-generativeai python-dotenv pdfkit
```

#### **➡️ Using Virtual Environment (venv)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install crewai[tools] streamlit beautifulsoup4 google-generativeai python-dotenv pdfkit
```

---

## **🔑 Set Up API Keys**  

This project requires two API keys:  
1️⃣ **Google Gemini API Key** – for AI-powered storytelling.  
2️⃣ **Serper API Key** – for AI-powered web searches.  

### **🔹 Get Google Gemini API Key**
1. Visit **[Google AI Studio](https://aistudio.google.com/)**.  
2. Sign in with your **Google Account**.  
3. Navigate to **API Keys** and generate a key.  

### **🔹 Get Serper API Key**
1. Go to **[Serper.dev](https://serper.dev/)**.  
2. Sign up for a free account.  
3. Copy your API key from the **Dashboard**.  

### **🔹 Store API Keys in a `.env` File**
Create a `.env` file in the project root and add the following:  
```ini
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

---

## **🚀 Running the AI Story Creator**  

### 🔹 1️⃣ Start the Streamlit App  
```bash
streamlit run app.py
```
This will launch the **AI Story Creator UI** in your browser.  

### 🔹 2️⃣ Generate a Story  
1️⃣ **Select or enter a story topic** (e.g., _"The Legend of Atlantis"_).  
2️⃣ **Click "Generate Story"** – AI will research, plan, and write the story.  
3️⃣ **Read the story in HTML format** inside the app.  
4️⃣ **Download** the story as an HTML file.  

### 🔹 3️⃣ Read a Previously Generated Story  
- Select **"Read Existing Story"** from the sidebar.  
- Choose a **previously saved story** from the dropdown.  
- Click **"Load Story"** to display it.  

---

## 📂 **Project Structure**  
```
📦 ai-story-creator
│── 📁 config
│   ├── agents.yaml        # CrewAI agent definitions
│   ├── tasks.yaml         # CrewAI task definitions
│── 📁 assets              # Folder where generated stories are saved
│── 📜 crew.py             # CrewAI pipeline for AI storytelling
│── 📜 app.py              # Streamlit web app for user interaction
│── 📜 .env                 # API keys (not included in repo)
│── 📜 README.md            # Project documentation
```

---

## 🤖 **How CrewAI Works in This Project**  
CrewAI enables **multiple AI agents** to collaborate like a real editorial team:  

| 🎭 **Agent**            | 🎯 **Role** |
|----------------------|------------------------------------------------|
| **Story Manager**    | Oversees workflow, ensures quality |
| **Background Researcher** | Gathers historical & cultural context |
| **Cultural Expert**  | Ensures authenticity & prevents stereotypes |
| **Story Planner**    | Develops story structure, characters, themes |
| **Story Writer**     | Writes the complete, engaging story |
| **Consistency Checker** | Ensures logical & narrative coherence |
| **Web Designer**     | Formats the story into a beautiful HTML page |

---

## 🔥 **Future Enhancements**  
✅ **AI-Generated Illustrations** – Add AI-generated images to enhance storytelling.  
✅ **Speech Narration (TTS)** – Convert the generated story into an **audio narration**.  
 

---

## 📄 **License**  
This project is open-source and available under the **MIT License**.  

---

## 📧 **Contact**  
💬 **Follow my work and stay updated!**  

📩 **Substack:** [First Ratio](https://firstratio.substack.com/)  
🔗 **LinkedIn:** [Rakesh Pandey](https://www.linkedin.com/in/rakeshpandey820/)  
🔗 **LinkedIn:** [Valli Akella](https://www.linkedin.com/in/vallials/) 

🚀 **Happy Storytelling! 📖✨**

---

### 🔑 Dependencies Notice

- **pdfkit:** This package is required for PDF conversion.  
- **wkhtmltopdf:** Please install wkhtmltopdf separately as pdfkit depends on it.
  - On Ubuntu/Debian:
    ```bash
    sudo apt-get update
    sudo apt-get install wkhtmltopdf
    ```
  - On macOS (using Homebrew):
    ```bash
    brew install wkhtmltopdf
    ```
  - On Windows:
    Download the installer from https://wkhtmltopdf.org/downloads.html and follow the installation instructions.