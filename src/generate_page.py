from markdown_to_htmlnode import markdown_to_html_node
from markdown_parser import extract_title
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        md_content = md_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', 'href="{basepath}').replace('src="/', 'src="{basepath}')
    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            if item_path.endswith(".md"):
                dest_item_path = dest_item_path.replace(".md", ".html")
                generate_page(item_path, template_path, dest_item_path)
        else:
            generate_pages_recursive(item_path, template_path, dest_item_path)