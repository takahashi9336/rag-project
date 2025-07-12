import os
from tree_sitter import Language, Parser

# 言語設定
Language.build_library(
    'build/my-languages.so',
    ['../shared/tree-sitter-c']
)

C_LANGUAGE = Language('build/my-languages.so', 'c')
parser = Parser()
parser.set_language(C_LANGUAGE)

def extract_function_name(node):
    for child in node.children:
        if child.type == "function_declarator":
            for sub in child.children:
                if sub.type == "identifier":
                    return sub.text.decode("utf-8")
    return "<anonymous>"

def collect_function_definitions(node, code):
    functions = []
    code_bytes = code.encode("utf-8")

    def walk(n):
        if n.type == "function_definition":
            snippet = code_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="ignore")
            functions.append({
                "name": extract_function_name(n),
                "code": snippet,
                "start_line": n.start_point[0],
                "end_line": n.end_point[0],
                "bytes": n.end_byte - n.start_byte
            })
        for child in n.children:
            walk(child)

    walk(node)
    return functions

def get_chunks(source_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    chunks = collect_function_definitions(root_node, code)
    # for f in chunks:
    #     print(f"Function: {f['name']}  |  Lines: {f['end_line'] - f['start_line'] + 1}  |  Bytes: {len(f['code'])}")
    #     print(f"Lines {f['start_line']}–{f['end_line']}")
    #     print(f"bytes: {f['bytes']}")
    #     print(f['code'])
    #     print("-" * 40)

    return chunks

# ★ サブディレクトリを含めた `.c` ファイルすべてを対象に解析
def get_chunks_from_directory(root_dir):
    all_chunks = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".c"):
                full_path = os.path.join(dirpath, filename)
                try:
                    chunks = get_chunks(full_path)
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"[ERROR] Failed to parse {full_path}: {e}")
    return all_chunks