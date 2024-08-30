import streamlit as st
import time
import cohere
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from annoy import AnnoyIndex
import numpy as np
import pytesseract
from pdf2image import convert_from_bytes
from multiprocessing import Pool, cpu_count
co = cohere.Client(api_key='NyUP8YHHfdp30nLRI9gsLLJMvgzZoQJJvUJaIMcB')

# Define process_image function outside of pdf_to_text
def process_image(image):
    return pytesseract.image_to_string(image)

def pdf_to_text(pdf):
    # Convert PDF pages to images
    images = convert_from_bytes(pdf.read())
    
    # Perform OCR on each image
    texts = []

    # Create a progress bar
    progress_bar = st.progress(0)
    total_pages = len(images)
    
    # Use multiprocessing for OCR
    with Pool(processes=cpu_count()) as pool:
        for i, text in enumerate(pool.imap(process_image, images)):
            texts.append(text)
            progress = (i + 1) / total_pages
            progress_bar.progress(progress)

    progress_bar.empty()
    
    # Join all texts and split into paragraphs
    full_text = '\n\n'.join(texts)
    
    # Write to file (if needed)
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Split into paragraphs and clean up
    paragraphs = [t.strip() for t in full_text.split('\n\n') if t.strip()]
    
    st.subheader("Text extracted")
    return np.array(paragraphs)

def search(query):
    # Get the query's embedding
    query_embed = co.embed(texts=[query]).embeddings
    
    # Retrieve the nearest neighbors
    similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,include_distances=True)

    search_results = texts[similar_item_ids[0]]
    
    return search_results


# ## Generating Answers

def ask(question, num_generations=1):
    
    # Search the text archive
    results = search(question)
    # Get the top result
    context = results[0]
    # Prepare the prompt
    prompt = f"""
    context: 
    {context}
    Question: {question}
    
    Extract the answer of the question from the text provided. 
    If the text doesn't contain the answer, 
    reply that the answer is not available."""

    prediction = co.generate(
        prompt=prompt,
        max_tokens=70,
        model="command-nightly",
        temperature=0.5,
        num_generations=num_generations
    )

    return prediction.generations


#UI

st.title("ChatPDF")

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'search_index' not in st.session_state:
    st.session_state.search_index = None
if 'texts' not in st.session_state:
    st.session_state.texts = None

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and not st.session_state.pdf_processed:
    texts = pdf_to_text(uploaded_file)
    st.write("PDF uploaded and processed successfully.")
    
    response = co.embed(texts=texts.tolist()).embeddings

    # Build a search index
    embeds = np.array(response)
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    
    # Add all the vectors to the search index

    # Display loading spinner while embedding and indexing
    with st.spinner("Embedding and indexing in progress..."):
        # Add all the vectors to the search index
        for i in range(len(embeds)):
            search_index.add_item(i, embeds[i])
    search_index.build(10)  # 10 trees
    st.success("Embedding and indexing completed.")

    # Store processed data in session state
    st.session_state.pdf_processed = True
    st.session_state.search_index = search_index
    st.session_state.texts = texts

elif st.session_state.pdf_processed:
    st.success("PDF already processed. Ready for queries.")
else:
    st.warning("Please upload a PDF file to proceed.")
    st.stop()

# Get user input
user_query = st.chat_input("Ask a question:", key="user_query")

if user_query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
    
    # Get chatbot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Use stored search_index and texts
        search_index = st.session_state.search_index
        texts = st.session_state.texts
        
        # Simulate stream of response with milliseconds delay
        responses = ask(user_query, num_generations=1)
        response = str(responses[0]).split("'")[3]
        print(response)
        message_placeholder.markdown(response)
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []

# Add a button to reset PDF processing
if st.button("Reset PDF Processing"):
    st.session_state.pdf_processed = False
    st.session_state.search_index = None
    st.session_state.texts = None
