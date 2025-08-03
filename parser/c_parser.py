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

def collect_function_definitions(node, code, file_name=None):
    functions = []
    code_bytes = code.encode("utf-8")

    def walk(n):
        if n.type == "function_definition":
            snippet = code_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="ignore")
            functions.append({
                "file_name": file_name,
                "function_name": extract_function_name(n),
                "code": snippet,
                "start_line": n.start_point[0],
                "end_line": n.end_point[0],
                "bytes": n.end_byte - n.start_byte
            })
        for child in n.children:
            walk(child)

    walk(node)
    return functions

def collect_top_level_chunks(node, code, filename=None):
    chunks = []
    code_bytes = code.encode("utf-8")

    def walk(n):
        # 対象とするノードタイプ一覧
        target_types = [
            "function_definition",
            "preproc_include",
            "preproc_def",
            "preproc_function_def",
            "declaration"
        ]

        if n.type in target_types:
            snippet = code_bytes[n.start_byte:n.end_byte].decode("utf-8", errors="ignore")

            chunks.append({
                "type": n.type,
                "name": extract_function_name(n) if n.type == "function_definition" else "<non-function>",
                "code": snippet,
                "start_line": n.start_point[0],
                "end_line": n.end_point[0],
                "bytes": n.end_byte - n.start_byte,
                "filename": filename
            })

        # トップレベルのみ対象（子は再帰しない）
        # ただし関数定義内の入れ子を無視したいため
        for child in n.children:
            # if n.type == "translation_unit":  # ファイルのルートのみ再帰する
            #     walk(child)
            walk(child)

    walk(node)
    return chunks

def get_chunks(source_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    file_name =os.path.basename(source_path)
    # chunks = collect_function_definitions(root_node, code,file_name)
    chunks = collect_top_level_chunks(root_node, code, file_name)
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
            if filename.endswith(".c") or filename.endswith(".h"):
                full_path = os.path.join(dirpath, filename)
                print(f"[INFO] Parsing {full_path}...")
                try:
                    chunks = get_chunks(full_path)
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"[ERROR] Failed to parse {full_path}: {e}")
    return all_chunks


def merge_chunks(chunks):
    if not chunks:
        return []

    # ファイル名、type、開始行でソート
    chunks = sorted(chunks, key=lambda c: (c['filename'], c['type'], c['start_line']))

    merged = []
    current = chunks[0].copy()

    for chunk in chunks[1:]:
        is_same_file = chunk['filename'] == current['filename']
        is_same_type = chunk['type'] == current['type']
        is_continuous = chunk['start_line'] <= current['end_line'] + 1

        if is_same_file and is_same_type and is_continuous:
            # マージ対象：コードや行・バイト数を更新
            current['code'] += '\n' + chunk['code']
            current['end_line'] = chunk['end_line']
            current['bytes'] += chunk['bytes']
        else:
            # ひとまとまりとして保存
            merged.append(current)
            current = chunk.copy()

    merged.append(current)
    return merged


