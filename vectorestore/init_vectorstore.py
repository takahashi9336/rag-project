import parser.c_parser as c_parser
import vectorestore.chroma_connector as chroma_connector

# chunks = c_parser.get_chunks('./batch_source/sample_test.c')
chunks = c_parser.get_chunks_from_directory('./batch_source')
merged_chunks = c_parser.merge_chunks(chunks)

db = chroma_connector.get_vector_db()
for chunk in merged_chunks:
    db.add_texts(
        texts=[chunk['code']],
        metadatas=[{
            'function_name': chunk['function_name'],
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'bytes': chunk['bytes']
        }]
    )

print(f"Added {len(merged_chunks)} function definitions to the vector database.")
