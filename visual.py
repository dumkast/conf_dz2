import os
import subprocess
import argparse
import tempfile
import webbrowser

def get_commits(repo_path):
    os.chdir(repo_path)
    try:
        result = subprocess.run(['git', 'rev-list', '--all', '--reverse'], capture_output=True, text=True, check=True)
        commits = result.stdout.splitlines()
        return commits
    except subprocess.CalledProcessError as e:
        return []

def check_file_exists_in_commit(commit_hash, filename):
    try:
        result = subprocess.run(['git', 'ls-tree', '-r', commit_hash, '--name-only'], capture_output=True, text=True,
                                check=True)
        files = result.stdout.splitlines()
        return filename in files
    except subprocess.CalledProcessError:
        return False

def build_dependency_graph(repo_path, commits, filename):
    graph = {}
    irrelevant_commits = [c for c in commits if check_file_exists_in_commit(c, filename)]

    for commit in commits:
        try:
            result = subprocess.run(['git', 'show', '--pretty=%P', '--no-patch', commit], capture_output=True,
                                    text=True, check=True)
            parents = result.stdout.strip().split()
            graph[commit] = parents
        except subprocess.CalledProcessError as e:
            print(f"Ошибка Git при обработке коммита {commit}: {e}")

    return graph, irrelevant_commits

def generate_mermaid_code(repo_path,graph, irrelevant_commits):
    code = "graph TD\n"

    commits = get_commits(repo_path)
    commit_order = {commit: index + 1 for index, commit in enumerate(commits)}

    for commit in irrelevant_commits:
        node_id = commit[:7]
        order_number = commit_order[commit]

        code += f"    {node_id}({order_number}: {node_id})\n"

    for commit in irrelevant_commits:
        node_id = commit[:7]
        parents = graph.get(commit, [])
        for parent in parents:
            if parent in irrelevant_commits:
                parent_id = parent[:7]
                code += f"    {parent_id} --> {node_id}\n"

    return code

def render_mermaid_graph(mermaid_path, mermaid_graph, script_dir):
    with tempfile.NamedTemporaryFile(suffix=".mmd", delete=False, mode='w') as temp_file:
        temp_file.write(mermaid_graph)
        temp_file_path = temp_file.name

    output_image_path = os.path.join(script_dir, "graph.png")

    try:
        subprocess.run([mermaid_path, '-i', temp_file_path, '-o', output_image_path], check=True)
        print(f"Граф сохранен как: {output_image_path}")


        webbrowser.open(output_image_path)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка Mermaid: {e}")
    finally:
        os.remove(temp_file_path)

def main():
    parser = argparse.ArgumentParser(description='Visualize Git commit dependencies.')
    parser.add_argument('mermaid_path', help='Path to the mermaid-cli executable')
    parser.add_argument('repo_path', help='Path to the git repository')
    parser.add_argument('filename', help='File name to track dependencies')

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    commits = get_commits(args.repo_path)

    if not commits:
        print("No commits found.")
        return
    dependency_graph, irrelevant_commits = build_dependency_graph(args.repo_path, commits, args.filename)


    mermaid_code = generate_mermaid_code(args.repo_path,dependency_graph, irrelevant_commits)

    print(mermaid_code)
    render_mermaid_graph(args.mermaid_path, mermaid_code, script_dir)


if __name__ == "__main__":
    main()
