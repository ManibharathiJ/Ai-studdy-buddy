import streamlit as st
import nltk
# This conditional block SOLVES stubborn punkt errors on Streamlit Cloud or Docker
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import pipeline


st.title("AI Study Buddy: Summarize & Simplify")

# --- Helper Functions ---
def chunk_text(text, max_words=300):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    count = 0
    for sentence in sentences:
        word_count = len(sentence.split())
        if count + word_count > max_words:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            count = word_count
        else:
            current_chunk += " " + sentence
            count += word_count
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def summarize_long_text(text, summarizer):
    chunks = chunk_text(text, max_words=300)
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

def simplify_text(text, simplifier):
    input_text = "simplify: " + text
    result = simplifier(input_text, max_length=512, clean_up_tokenization_spaces=True)
    return result[0]['generated_text']

def generate_quiz_questions(text):
    sentences = sent_tokenize(text)
    questions = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 3:
            question = ' '.join(words[:-1]) + " ______"
            answer = words[-1]
            questions.append((question, answer))
    return questions

def generate_flashcards(summary, num_flashcards=5):
    sentences = sent_tokenize(summary)
    flashcards = []
    used = set()
    for sentence in sentences:
        words = word_tokenize(sentence)
        if len(words) > 4:
            for i in reversed(range(len(words))):
                if words[i].istitle() or words[i].isalpha():
                    question = sentence.replace(words[i], "__________", 1)
                    if question not in used and words[i] not in used:
                        flashcards.append({"question": question, "answer": words[i]})
                        used.add(question)
                        used.add(words[i])
                    break
        if len(flashcards) >= num_flashcards:
            break
    return flashcards

# --- Load Models ---
@st.cache_resource
def load_simplifier():
    return pipeline("text2text-generation", model="t5-base")
@st.cache_resource
def load_summarizer():
    return pipeline("summarization")

simplifier = load_simplifier()
summarizer = load_summarizer()

# --- Streamlit UI ---
user_input = st.text_area("Paste your study notes here:", height=300)

if st.button("Generate Study Aids"):
    if not user_input.strip():
        st.warning("Please enter some study text to proceed.")
    else:
        input_words = len(word_tokenize(user_input))

        # Automatic chunking for unlimited length
        simplified = " ".join([simplify_text(chunk, simplifier) for chunk in chunk_text(user_input, max_words=300)])
        summary = summarize_long_text(user_input, summarizer)
        quiz = generate_quiz_questions(user_input)
        flashcards = generate_flashcards(summary, num_flashcards=5)
        simplified_words = len(word_tokenize(simplified))
        summary_words = len(word_tokenize(summary))

        st.success(f"Input length: {input_words} words")
        
        st.subheader("Simplified Text")
        st.write(simplified)
        st.caption(f"Words: {simplified_words}")

        st.subheader("Summary")
        st.write(summary)
        st.caption(f"Words: {summary_words}")

        st.subheader("Quiz Questions")
        for i, (q, a) in enumerate(quiz, 1):
            st.markdown(f"**Q{i}:** {q}")
            with st.expander("Show Answer"):
                st.write(a)

        st.subheader("Flashcards")
        for idx, card in enumerate(flashcards, 1):
            st.markdown(f"**Flashcard {idx}:**")
            st.markdown(f"Q: {card['question']}")
            with st.expander("Show Answer"):
                st.write(card['answer'])


