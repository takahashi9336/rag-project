# main/app.py
import query
query_input = "sample_test.cの処理概要を説明して。"
response = query.query(query_input)
print(f"Response to query '{query_input}': {response}")

