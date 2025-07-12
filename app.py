# main/app.py
import parser.c_parser as c_parser
import vectorestore.chroma_connector as chroma_connector
import query

print("==" * 10 + " starting get_chunks" + "==" * 10)

chunks = c_parser.get_chunks('./batch-source/sample_test.c')
# chunks = c_source_loader.get_chunks_from_directory('./source')

print("==" * 10 + " starting to add chunks to vector database " + "==" * 10)

db = chroma_connector.get_vector_db()
for chunk in chunks:
    db.add_texts(
        texts=[chunk['code']],
        metadatas=[{
            'name': chunk['name'],
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'bytes': chunk['bytes']
        }]
    )

print(f"Added {len(chunks)} function definitions to the vector database.")

print("==" * 10 + " starting query" + "==" * 10)

query_input = "sample_test.cの処理概要を説明して。"
response = query.query(query_input)
print(f"Response to query '{query_input}': {response}")


