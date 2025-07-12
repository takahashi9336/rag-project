# main/app.py
import source_loader_c as source_loader_c
import vector_db_getter
import query

print("==" * 10 + " starting get_chunks" + "==" * 10)

chunks = source_loader_c.get_chunks('./source/sample_test.c')
# chunks = c_source_loader.get_chunks_from_directory('./source')

print("==" * 10 + " starting to add chunks to vector database " + "==" * 10)

db = vector_db_getter.get_vector_db()
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


