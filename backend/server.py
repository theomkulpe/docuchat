import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import *

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# This stores the vector store for the uploaded file
vector_store = None

@app.route('/upload', methods=['POST'])
def upload():
    global vector_store
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract and process the PDF
    docs = extract_pdf_text(filepath)
    docs = split_text(docs)
    vector_store = create_vector_store()
    add_documents_to_vector_store(vector_store, docs)

    return jsonify({'message': 'File processed successfully'})

@app.route('/upload_webpage', methods=['POST'])
def upload_webpage():
    global vector_store
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Extract and process the webpage
    docs = extract_webpage_text(url)
    docs = split_text(docs)
    vector_store = create_vector_store()
    add_documents_to_vector_store(vector_store, docs)

    return jsonify({'message': 'Webpage processed successfully'})

@app.route('/query', methods=['POST'])
def query():
    global vector_store
    if vector_store is None:
        return jsonify({'error': 'No file uploaded yet'}), 400
    
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Process the query
    response = chat(vector_store, query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
