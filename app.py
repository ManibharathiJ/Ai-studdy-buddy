import streamlit as st
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

@st.cache_resource
def load_simplifier():
    return pipeline("text2text-generation", model="t5-base")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization")

simplifier = load_simplifier()
summarizer = load_summarizer()

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

def summarize_long_text(text):
    chunks = chunk_text(text, max_words=300)
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

def simplify_text(text):
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

st.title("AI Study Buddy: Your Personal Study Assistant")

user_input = st.text_area("Enter your study text here:", height=200)

if st.button("Generate Study Aids"):
    if not user_input.strip():
        st.warning("Please enter some study text to proceed.")
    else:
        # Word count for input
        input_words = len(word_tokenize(user_input))
        st.info(f"Input text word count: {input_words} words")

        with st.spinner("Processing your input..."):
            simplified = simplify_text(user_input)
            summary = summarize_long_text(user_input)
            quiz = generate_quiz_questions(user_input)
            flashcards = generate_flashcards(summary, num_flashcards=5)

        # Word counts for outputs
        simplified_words = len(word_tokenize(simplified))
        summary_words = len(word_tokenize(summary))

        st.subheader("Simplified Text")
        st.write(simplified)
        st.caption(f"Simplified Text word count: {simplified_words}")

        st.subheader("Summary")
        st.write(summary)
        st.caption(f"Summary word count: {summary_words}")

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
