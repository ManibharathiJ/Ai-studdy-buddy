# AI Study Buddy 

## 📘 Project Overview
AI Study Buddy is a Streamlit web application that helps students instantly simplify notes, summarize content, and generate quizzes and flashcards for self-revision. By using advanced NLP and AI models, it transforms any length of study material into effective, easy-to-understand study aids for faster learning and recall.

## 🎯 Objectives
•	Help students revise large volumes of notes with ease.
•	Make study content more understandable and accessible for all learners.
•	Generate instant quizzes and flashcards for fast revision and knowledge checks.
•	Support independent learning without the need for manual content creation.

## 🧠 Key Features
•	Accepts unlimited text inputs from students.
•	Simplifies complex notes and generates concise summaries.
•	Automatically creates quiz questions and flashcards.
•	Interactive web interface powered by Streamlit—no install required.
•	Fast, session-only processing for privacy.

## 🛠️ Tools & Technologies
•	Languages: Python
•	Libraries: Streamlit, HuggingFace Transformers, NLTK, PyTorch
•	Models: T5-base (text simplification), HuggingFace summarization pipeline
•	Other: Jupyter Notebook (for development/demo), session-based data handling

## 📂 Dataset
•	Source: Student notes or course content pasted directly by users.
•	Description: Any academic text, no restriction on length; works for all major subjects/topics.
•	Note: No third-party datasets stored; all text processed in-memory per session.

## ⚙️ Project Workflow
1.	User pastes or enters study notes in the app.
2.	The app splits long content into chunks using NLTK tokenization.
3.	Each chunk is processed by AI models (Transformers/T5 via PyTorch) for simplification and summarization.
4.	Quizzes and flashcards are auto-generated from processed content.
5.	All outputs are instantly displayed in the Streamlit interface.

## 📊 Results
•	Notes are simplified and compressed for easier understanding.
•	Generated quizzes and flashcards help reinforce concepts quickly.
•	The app runs instantly regardless of input size; results are delivered in seconds.

## 📈 Visualization
 


## 🧩 Future Work / Improvements
•	Add voice and multilingual support for broader accessibility.
•	Launch a mobile app for revision on-the-go.
•	Incorporate analytics for personalized quiz suggestions.
•	Enable offline access and integration with popular school platforms.

## 👩‍💻 Author / Contributor
Manibharathi
MBA Business Analytics | BTech Biotechnology

## 💬 Acknowledgments
•	Streamlit, HuggingFace, PyTorch, and NLTK documentation.


