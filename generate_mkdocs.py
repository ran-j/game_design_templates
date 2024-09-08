import os
import shutil

site_name = "Game Design Templates"
theme_name = "material"
docs_dir = "docs"
nav = []


def ensure_docs_directory():
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"Created directory: {docs_dir}")


def copy_markdown_files_preserve_structure():
    for root, _, filenames in os.walk("."):

        if docs_dir in root:
            continue
        for filename in filenames:
            if filename.endswith(".md"):
                src_path = os.path.join(root, filename)

                relative_path = os.path.relpath(src_path, ".")
                dst_path = os.path.join(docs_dir, relative_path)
                dst_dir = os.path.dirname(dst_path)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copyfile(src_path, dst_path)
                print(f"Copied {src_path} to {dst_path}")


def scan_markdown_files(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in sorted(filenames):
            if filename.endswith(".md") and filename != "README.md":
                relative_dir = os.path.relpath(root, directory)
                if relative_dir not in files:
                    files[relative_dir] = []
                relative_path = os.path.relpath(os.path.join(root, filename), directory)
                files[relative_dir].append(relative_path)
    return files


def format_nav_grouped_by_folder(markdown_files):
    for folder, filepaths in markdown_files.items():
        folder_name = folder.replace("_", " ").title()
        if folder == ".":
            folder_name = "Others"

        nav_entry = {folder_name: []}
        for filepath in filepaths:
            filename = os.path.basename(filepath)
            name = filename.replace("_", " ").replace(".md", "").title()
            nav_entry[folder_name].append({name: filepath})
        nav.append(nav_entry)


def generate_mkdocs_yml():
    markdown_files = scan_markdown_files(docs_dir)
    format_nav_grouped_by_folder(markdown_files)

    mkdocs_content = f"""
site_name: {site_name}
theme:
  name: {theme_name}
nav:
  - Home: README.md
"""
    for entry in nav:
        for folder_name, files in entry.items():
            mkdocs_content += f"  - {folder_name}:\n"
            for file_entry in files:
                for file_name, file_path in file_entry.items():
                    mkdocs_content += f"    - {file_name}: {file_path}\n"

    with open("mkdocs.yml", "w") as f:
        f.write(mkdocs_content)

    print("Generated mkdocs.yml:")
    print(mkdocs_content)


if __name__ == "__main__":
    ensure_docs_directory()
    copy_markdown_files_preserve_structure()
    generate_mkdocs_yml()
