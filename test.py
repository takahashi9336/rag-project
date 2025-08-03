import parser.c_parser as c_parser

def print_chunks(chunks):
    for chunk in chunks:
        print(f"ファイル: {chunk['filename']}")
        print(f"タイプ: {chunk['type']}")
        print(f"名前: {chunk['name']}")
        print(f"開始行: {chunk['start_line'] + 1}, 終了行: {chunk['end_line'] + 1}")
        print(f"バイト数: {chunk['bytes']}")
        print("コードスニペット:")
        print(chunk['code'])
        print("=" * 80)

if __name__ == "__main__":
    chunks = c_parser.get_chunks_from_directory("./batch_source")
    merged_chunks = c_parser.merge_chunks(chunks)
    print_chunks(merged_chunks)

#chunks = c_parser.get_chunks('./batch_source/sample_test.c')
# chunks = c_parser.get_chunks_from_directory('./batch_source')

# def print_chunks(chunks):
#     for chunk in chunks:
#         print(f"file_name: {chunk['file_name']}")
#         print(f"function_name: {chunk['function_name']}")
#         print(f"start_line: {chunk['start_line'] + 1}, end_line: {chunk['end_line'] + 1}")
#         print(f"line: {chunk['end_line'] - chunk['start_line'] + 1}, bytes: {chunk['bytes']}")
#         print("code:")
#         print(chunk['code'])
#         print("=" * 80)
