# utils/generate_projects.py
import os
import json
from PIL import Image, ImageDraw, ImageFont
import random

# Caminhos
PROJECTS_DIR = '../projects'
PREVIEWS_DIR = '../static/images/previews'
DATA_FILE = '../static/data/content.json'

# Garante que a pasta de previews existe
os.makedirs(PREVIEWS_DIR, exist_ok=True)

# Cores de fundo aleatórias para previews
COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

def generate_preview(project_name, tech, output_path):
    """Gera uma imagem de preview com nome e tecnologia"""
    img = Image.new('RGB', (400, 300), random.choice(COLORS))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_tech = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_tech = ImageFont.load_default()

    w, h = draw.textsize(project_name, font=font_title)
    draw.text(((400-w)/2, 100), project_name, fill="white", font=font_title)
    draw.text(((400-w)/2, 160), tech, fill="white", font=font_tech)

    img.save(output_path)

def extract_code_snippet(file_path):
    """Extrai as primeiras 5 linhas de código"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()][:5]
            return '\n'.join(lines)
    except:
        return "// Não foi possível ler o código"

def detect_tech(folder):
    """Detecta tecnologia com base na extensão"""
    tech_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'React',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.java': 'Java',
        '.cs': 'C#',
        '.go': 'Go'
    }
    files = []
    for root, _, fs in os.walk(folder):
        files.extend(fs)
    
    extensions = [os.path.splitext(f)[1] for f in files]
    techs = list(set(tech_map.get(ext, '') for ext in extensions if tech_map.get(ext)))
    return techs[:3] if techs else ['Desconhecido']

def generate_projects_data():
    projects = []

    for project_name in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if not os.path.isdir(project_path):
            continue

        # Detecta tecnologias
        techs = detect_tech(project_path)

        # Procura arquivos principais
        main_files = [f for f in os.listdir(project_path) if f in ['index.html', 'main.js', 'app.js', 'server.js']]
        code_file = os.path.join(project_path, main_files[0]) if main_files else os.path.join(project_path, os.listdir(project_path)[0])

        # Gera preview
        preview_path = f'{PREVIEWS_DIR}/{project_name}.png'
        generate_preview(project_name.replace('-', ' ').title(), ', '.join(techs), preview_path)

        # Extrai código
        code_snippet = extract_code_snippet(code_file)

        projects.append({
            "title": project_name.replace('-', ' ').title(),
            "description": f"Projeto em {', '.join(techs)} com funcionalidades modernas.",
            "image": f"/static/images/previews/{project_name}.png",
            "tags": techs,
            "code": code_snippet,
            "link": f"#"
        })

    # Salva em JSON
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=4)

    print("✅ Projetos gerados com sucesso!")

if __name__ == '__main__':
    generate_projects_data()