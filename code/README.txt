ChatPDF with RAG (Retrieval-Augmented Generation)
Description
ChatPDF with RAG is an interactive application built using Streamlit that enables users to extract and search information from PDF files, leveraging OCR (Optical Character Recognition) for image-based PDFs. The tool uses Cohere's language model for natural language query processing and Annoy for fast vector similarity search. Additionally, it generates flowcharts for step-based responses and retrieves images relevant to user queries from the PDF.
Features
1.	PDF Upload and Processing:
o	Upload a PDF file, which will be converted into text using OCR (via Tesseract).
o	The text is split into paragraphs, embedded, and indexed for efficient searching.
2.	Text-Based Search:
o	Use natural language queries to search the PDF content.
o	The search utilizes an Annoy index for fast retrieval of relevant paragraphs from the document.
3.	Image Extraction and Search:
o	Images from the PDF are extracted and processed using OCR.
o	You can search for relevant images by providing a keyword, and the tool will display images from the PDF related to the keyword.
4.	Flowchart Generation:
o	For queries that return step-by-step instructions, the application automatically generates a flowchart to visualize the steps.
5.	Interactive Chat:
o	The tool maintains chat history for back-and-forth interaction with the user, allowing users to ask questions and get responses.
o	Provides clarification or simplified answers if the user requests them.
6.	Embeddings and RAG:
o	Uses Cohere's embedding API to create vector representations of the text, which are then indexed with Annoy.
o	Supports Retrieval-Augmented Generation (RAG) to answer questions based on retrieved information.
Dependencies
To install the necessary dependencies, run:
bash
Copy code
pip install -r requirements.txt
Key Dependencies:
•	Streamlit: For building the interactive user interface.
•	Cohere: For text embeddings and language model generation.
•	Tesseract OCR: For extracting text from images in the PDF.
•	Annoy: For efficient nearest-neighbor search.
•	pdf2image: To convert PDF pages into images for OCR processing.
•	PIL (Pillow): To handle image manipulation.
•	Graphviz: For generating flowcharts.
•	Multiprocessing: For parallel OCR processing.
File Structure
•	app.py: The main application file containing the Streamlit interface, PDF processing, search functionality, and image extraction.
•	README.md: This file, providing information about the project.
•	requirements.txt: A list of dependencies required for the project.
Usage
1.	Run the Application: To run the application, use the following command:
bash
Copy code
streamlit run app.py
2.	Upload a PDF:
o	Once the app is running, upload a PDF file in the sidebar.
o	If the PDF contains text and images, it will be processed, and the text will be indexed for searching.
3.	Ask Questions:
o	Type a natural language question in the chat input to search for relevant text within the PDF.
o	The application will retrieve the relevant paragraphs and display them.
4.	View Flowcharts:
o	If the answer to your query includes steps or instructions, a flowchart will be displayed for better visualization.
5.	Image Search:
o	After PDF processing, relevant images are extracted using OCR.
o	You can search for images by querying specific keywords related to the content.
6.	Clear History and Reset:
o	You can clear the chat history and reset the PDF processing at any time.
Example Queries
•	"What are the steps for data analysis?"
•	"Show me images related to 'neural network'."
•	"Can you simplify the explanation of 'machine learning'?"
Customization
•	Flowchart Font Size: You can modify the flowchart font size by editing the generate_flowchart() function in the app.
•	Cohere API Key: Replace the placeholder API key in the code (api_key='xmHg8viTBgZ6vnb7YIxMe5VFouuFCiDM4MkE3x2v') with your actual Cohere API Key.
License
This project is open source and available under the MIT License.

Contributing
Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.

