import os
import re
import shutil

# 配置
root_dir = "."              # 你的 Markdown 根目录
target_folder = "pictures"  # 统一放图片的目录

# 创建 target_folder
os.makedirs(target_folder, exist_ok=True)

# 匹配 ![](path)
img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

def is_image(file):
    return file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"))

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".md"):
            md_path = os.path.join(subdir, file)

            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            updated_content = content
            matches = img_pattern.findall(content)

            for img_path in matches:
                if not os.path.isfile(os.path.join(subdir, img_path)):
                    continue  # 非本地图片，跳过

                abs_img_path = os.path.join(subdir, img_path)
                img_name = os.path.basename(img_path)
                new_img_path = os.path.join(target_folder, img_name)

                # 如果存在同名图片，自动重命名
                if os.path.exists(new_img_path):
                    base, ext = os.path.splitext(img_name)
                    i = 1
                    while os.path.exists(new_img_path):
                        new_img_path = os.path.join(target_folder, f"{base}_{i}{ext}")
                        i += 1

                shutil.move(abs_img_path, new_img_path)

                # 替换 markdown 中的路径
                updated_content = updated_content.replace(img_path, os.path.relpath(new_img_path, subdir))

            # 写回 md 文件
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

print("所有 Markdown 图片已整理到 pictures/ 文件夹，并更新引用路径！")
