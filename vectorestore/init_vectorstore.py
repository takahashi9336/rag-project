import sys
import os

# このファイルから見て1つ上の階層（main）を import パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import my_parser.c_parser as c_parser
import vectorestore.chroma_connector as chroma_connector

# chunks = c_parser.get_chunks('./batch_source/sample_test.c')
chunks = c_parser.get_chunks_from_directory('./batch_source')
merged_chunks = c_parser.merge_chunks(chunks)

db = chroma_connector.get_vector_db('rag-collection')
for chunk in merged_chunks:
    db.add_texts(
        texts=[chunk['code']],
        metadatas=[{
            'filename': chunk['filename'],
            'type': chunk['type'],
            'name': chunk['name'],
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'bytes': chunk['bytes']
        }]
    )

print(f"Added {len(merged_chunks)} code snippets to the vector database.")
