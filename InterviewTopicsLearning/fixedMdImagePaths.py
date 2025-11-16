import os
import re

def fix_md_paths(root_dir):
    # Markdown 图片语法： ![alt](path)
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    for folder, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".md"):
                md_path = os.path.join(folder, file)
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()

                def replace_slash(match):
                    alt = match.group(1)
                    path = match.group(2)
                    fixed_path = path.replace("\\", "/")
                    return f"![{alt}]({fixed_path})"

                new_content = pattern.sub(replace_slash, content)

                if new_content != content:
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed: {md_path}")

if __name__ == "__main__":
    # 使用当前目录，也可以改成具体路径
    fix_md_paths(".")
