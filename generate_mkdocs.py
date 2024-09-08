import os
 
site_name = "Game Design Templates"
theme_name = "material"  # MkDocs theme we want to use
nav = []
 
def scan_markdown_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in sorted(filenames):
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                # Exclude README.md or index.md if necessary
                if filename not in ["README.md", "index.md"]:
                    files.append(filepath)
    return files
 
def format_nav_entry(filepath):
    filename = os.path.basename(filepath)
    name = filename.replace("_", " ").replace(".md", "")
    return f"  - {name.title()}: {filename}"
 
markdown_files = scan_markdown_files(".")
 
for filepath in markdown_files:
    nav.append(format_nav_entry(filepath))

# Create mkdocs.yml content
mkdocs_content = f"""
site_name: {site_name}
theme:
  name: {theme_name}
nav:
"""

mkdocs_content += "\n".join(nav)

with open("mkdocs.yml", "w") as f:
    f.write(mkdocs_content)

print("Generated mkdocs.yml:")
print(mkdocs_content)
