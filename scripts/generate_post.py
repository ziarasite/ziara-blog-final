
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from slugify import slugify
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

# Configurações de diretório
ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
POSTS_DIR = os.path.join(ROOT, "posts")
ASSETS_CSS_DIR = os.path.join(ROOT, "assets", "css")
IMAGES_DIR = os.path.join(ROOT, "assets", "images")
POSTS_INDEX_FILE = os.path.join(ROOT, "posts-index.json")

# Garante que os diretórios existam
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Inicializa o cliente OpenAI
client = OpenAI()

# Paletas de cores sazonais (exemplo)
PALETTES = {
    1: {"primary":"#c49a6c","bg":"#fff9f2"}, 2: {"primary":"#e89fb2","bg":"#fff6fb"},
    3: {"primary":"#f2c17d","bg":"#fff9f2"}, 4: {"primary":"#b0d7c6","bg":"#f7fffb"},
    5: {"primary":"#9aa8ff","bg":"#f6f8ff"}, 6: {"primary":"#f6d6a6","bg":"#fffaf6"},
    7: {"primary":"#ffd7e0","bg":"#fff6f8"}, 8: {"primary":"#c7f0d8","bg":"#f8fffb"},
    9: {"primary":"#e6c9ff","bg":"#fbf8ff"}, 10: {"primary":"#f3b57d","bg":"#fff8f2"},
    11: {"primary":"#c8c8c8","bg":"#fbfbfb"}, 12: {"primary":"#ffd9a6","bg":"#fffaf6"},
}

def apply_seasonal_css():
    month = datetime.now().month
    pal = PALETTES.get(month, {"primary":"#b8860b","bg":"#fffaf6"})
    css_content = f"""/* style.css gerado automaticamente - paleta da estação */\n\n:root {{\n    --primary-color: {pal['primary']};\n    --secondary-color: #2c3e50;\n    --accent-color: #e67e22;\n    --text-color: #333;\n    --bg-color: {pal['bg']};\n    --white: #ffffff;\n    --border-color: #e0e0e0;\n    --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);\n    --shadow-hover: 0 4px 20px rgba(0, 0, 0, 0.15);\n}}\n\n/* Restante do CSS permanece o mesmo */\n\n* {{\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}}\n\nbody {{\n    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n    line-height: 1.6;\n    color: var(--text-color);\n    background-color: var(--bg-color);\n}}\n\n.container {{\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 0 20px;\n}}\n\n/* Header */\n.header {{\n    background: linear-gradient(135deg, var(--secondary-color) 0%, #34495e 100%);\n    color: var(--white);\n    padding: 2rem 0;\n    box-shadow: var(--shadow);\n}}\n\n.logo-area {{\n    text-align: center;\n    margin-bottom: 1rem;\n}}\n\n.logo {{\n    font-size: 2.5rem;\n    font-weight: bold;\n    color: var(--primary-color);\n    text-transform: uppercase;\n    letter-spacing: 3px;\n    margin-bottom: 0.5rem;\n}}\n\n.subtitle {{\n    font-size: 1rem;\n    color: #bdc3c7;\n    font-style: italic;\n}}\n\n.tagline {{\n    text-align: center;\n    font-size: 1.1rem;\n    color: #ecf0f1;\n    margin-top: 0.5rem;\n}}\n\n/* Main Content */\nmain {{\n    padding: 3rem 0;\n}}\n\n.intro {{\n    background: var(--white);\n    padding: 2rem;\n    border-radius: 8px;\n    box-shadow: var(--shadow);\n    margin-bottom: 3rem;\n    border-left: 4px solid var(--primary-color);\n}}\n\n.intro h2 {{\n    color: var(--secondary-color);\n    margin-bottom: 1rem;\n    font-size: 1.8rem;\n}}\n\n.intro p {{\n    font-size: 1.1rem;\n    line-height: 1.8;\n    color: #555;\n}}\n\n/* Posts Section */\n.posts-section {{\n    margin-bottom: 3rem;\n}}\n\n.section-title {{\n    font-size: 2rem;\n    color: var(--secondary-color);\n    margin-bottom: 2rem;\n    padding-bottom: 0.5rem;\n    border-bottom: 3px solid var(--primary-color);\n}}\n\n.posts-grid {{\n    display: grid;\n    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));\n    gap: 2rem;\n}}\n\n.post-card {{\n    background: var(--white);\n    border-radius: 8px;\n    overflow: hidden;\n    box-shadow: var(--shadow);\n    transition: transform 0.3s ease, box-shadow 0.3s ease;\n    border: 1px solid var(--border-color);\n}}\n\n.post-card:hover {{\n    transform: translateY(-5px);\n    box-shadow: var(--shadow-hover);\n}}\n\n.post-image {{\n    width: 100%;\n    height: 200px;\n    object-fit: cover;\n    background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);\n}}\n\n.post-content {{\n    padding: 1.5rem;\n}}\n\n.post-meta {{\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    margin-bottom: 1rem;\n    font-size: 0.85rem;\n    color: #777;\n}}\n\n.post-date {{\n    display: flex;\n    align-items: center;\n    gap: 0.3rem;\n}}\n\n.post-category {{\n    background: var(--primary-color);\n    color: var(--white);\n    padding: 0.3rem 0.8rem;\n    border-radius: 20px;\n    font-size: 0.75rem;\n    font-weight: bold;\n}}\n\n.post-title {{\n    font-size: 1.4rem;\n    color: var(--secondary-color);\n    margin-bottom: 0.8rem;\n    line-height: 1.3;\n}}\n\n.post-title a {{\n    color: inherit;\n    text-decoration: none;\n    transition: color 0.3s ease;\n}}\n\n.post-title a:hover {{\n    color: var(--primary-color);\n}}\n\n.post-excerpt {{\n    color: #666;\n    line-height: 1.6;\n    margin-bottom: 1rem;\n}}\n\n.post-link {{\n    display: inline-block;\n    color: var(--accent-color);\n    text-decoration: none;\n    font-weight: bold;\n    transition: color 0.3s ease;\n}}\n\n.post-link:hover {{\n    color: var(--primary-color);\n}}\n\n.loading {{\n    text-align: center;\n    color: #999;\n    font-style: italic;\n    padding: 2rem;\n}}\n\n/* Footer */\n.footer {{\n    background: var(--secondary-color);\n    color: var(--white);\n    padding: 2rem 0;\n    text-align: center;\n    margin-top: 4rem;\n}}\n\n.footer p {{\n    margin-bottom: 0.5rem;\n}}\n\n.footer-note {{\n    font-size: 0.9rem;\n    color: #bdc3c7;\n}}\n\n/* Responsive */\n@media (max-width: 768px) {{\n    .logo {{\n        font-size: 2rem;\n    }}\n    \n    .posts-grid {{\n        grid-template-columns: 1fr;\n    }}\n    \n    .intro h2 {{\n        font-size: 1.5rem;\n    }}\n    \n    .section-title {{\n        font-size: 1.6rem;\n    }}\n}}\n\n/* Post Detail Page */\n.post-detail {{\n    background: var(--white);\n    padding: 3rem;\n    border-radius: 8px;\n    box-shadow: var(--shadow);\n    margin-bottom: 2rem;\n}}\n\n.post-detail .post-header {{\n    margin-bottom: 2rem;\n    padding-bottom: 1.5rem;\n    border-bottom: 2px solid var(--border-color);\n}}\n\n.post-detail .post-title {{\n    font-size: 2.5rem;\n    margin-bottom: 1rem;\n}}\n\n.post-detail .post-image {{\n    width: 100%;\n    height: auto;\n    max-height: 400px;\n    margin-bottom: 2rem;\n    border-radius: 8px;\n}}\n\n.post-detail .post-body {{\n    font-size: 1.1rem;\n    line-height: 1.8;\n    color: #444;\n}}\n\n.post-detail .post-body p {{\n    margin-bottom: 1.5rem;\n}}\n\n.post-detail .post-body h3 {{\n    color: var(--secondary-color);\n    margin-top: 2rem;\n    margin-bottom: 1rem;\n}}\n\n.back-link {{\n    display: inline-block;\n    margin-bottom: 2rem;\n    color: var(--accent-color);\n    text-decoration: none;\n    font-weight: bold;\n    transition: color 0.3s ease;\n}}\n\n.back-link:hover {{\n    color: var(--primary-color);\n}}\n"""
    with open(os.path.join(ASSETS_CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

def make_featured_image(title, filename):
    img_w, img_h = 1200, 600
    img = Image.new("RGB", (img_w, img_h), color=(255,255,255))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font_title = ImageFont.load_default()
    
    # Usar uma cor de destaque da paleta para o cabeçalho da imagem
    month = datetime.now().month
    pal = PALETTES.get(month, {"primary":"#b8860b","bg":"#fffaf6"})
    draw.rectangle([0,0,img_w,220], fill=pal['primary'])
    
    # Centralizar o texto do título
    text_width, text_height = draw.textbbox((0,0), title, font=font_title)[2:]
    text_x = (img_w - text_width) / 2
    text_y = (220 - text_height) / 2 # Centralizar verticalmente na faixa de 220px
    draw.text((text_x, text_y), title, fill=(40,40,40), font=font_title)
    
    path = os.path.join(IMAGES_DIR, filename)
    img.save(path, format="PNG")
    return os.path.join("assets", "images", filename).replace("\\", "/") # Caminho relativo para o HTML

def generate_content_with_llm():
    prompt = (
        "Gere um título e um corpo de texto para uma notícia diária sobre o mundo de joias e semijoias, "
        "focada em atacadistas e comerciantes. O conteúdo deve abordar tendências, altas do setor, "
        "dicas de mercado ou informações relevantes para o negócio. O texto deve ser profissional, "
        "informativo e ter aproximadamente 300-500 palavras, dividido em parágrafos. "
        "Inclua um parágrafo de introdução (lead) e alguns parágrafos no corpo. "
        "Formate a saída como um JSON com as chaves 'title', 'lead', 'body' (HTML formatado com tags <p> e talvez <h3> para subtítulos) e 'category'. "
        "Exemplo de categoria: 'Tendências de Mercado', 'Dicas para Atacadistas', 'Novidades do Setor'."
    )
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash", # Usando o modelo flash para rapidez
        messages=[
            {"role": "system", "content": "Você é um especialista em mercado de joias e semijoias, focado em atacadistas e comerciantes."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    response_content = response.choices[0].message.content.strip()
    # Remover markdown code block delimiters se presentes
    if response_content.startswith("```json") and response_content.endswith("```"):
        response_content = response_content[len("```json"):-len("```")].strip()
    elif response_content.startswith("```") and response_content.endswith("```"):
        response_content = response_content[len("```"):-len("```")].strip()

    # Tentar encontrar o JSON dentro da string, caso haja texto extra
    json_start = response_content.find("{")
    json_end = response_content.rfind("}")
    if json_start != -1 and json_end != -1 and json_end > json_start:
        response_content = response_content[json_start : json_end + 1]
    print(f"Resposta bruta da API: {response_content}") # Para depuração
    try:
        content = json.loads(response_content)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da API: {e}")
        print(f"Conteúdo recebido: {response_content}")
        # Retornar um conteúdo padrão ou levantar uma exceção
        return {"title": "Erro na Geração de Conteúdo", "lead": "Houve um problema ao gerar o conteúdo. Tente novamente.", "body": "<p>Não foi possível obter o conteúdo do LLM.</p>", "category": "Erro"}
    return content
    return content

def generate_post():
    today = datetime.now()
    
    # Gerar conteúdo com LLM
    llm_content = generate_content_with_llm()
    title = llm_content.get("title", f"Atualização do Mercado {today.strftime('%d/%m/%Y')}")
    lead = llm_content.get("lead", "Confira as últimas novidades do setor.")
    body = llm_content.get("body", "<p>Nenhuma informação detalhada disponível.</p>")
    category = llm_content.get("category", "Notícias do Setor")
    
    slug = slugify(f"{title}-{today.strftime('%Y%m%d%H%M%S')}") # Adiciona H M S para unicidade
    filename = f"{slug}.html"
    image_name = f"post_{today.strftime('%Y%m%d%H%M%S')}.png"
    
    # Gerar imagem destacada
    image_path_for_html = make_featured_image(title, image_name)
    
    # Renderizar com Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("base.html")
    rendered_html = template.render(
        title=title,
        date=today.strftime("%d/%m/%Y"),
        category=category,
        lead=lead,
        body=body,
        image=image_path_for_html,
        summary=lead # Usar o lead como summary para o index
    )
    
    # Salvar o post HTML
    post_filepath = os.path.join(POSTS_DIR, filename)
    with open(post_filepath, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    print(f"Post '{title}' salvo em {post_filepath}")
    
    # Atualizar posts-index.json
    update_posts_index({
        "title": title,
        "date": today.strftime("%d/%m/%Y"),
        "timestamp": today.isoformat(),
        "category": category,
        "excerpt": lead, # Usar o lead como excerpt
        "filename": filename,
        "image": image_path_for_html
    })

def update_posts_index(new_post_data):
    posts_data = {"posts": [], "last_updated": datetime.now().isoformat()}
    
    if os.path.exists(POSTS_INDEX_FILE):
        with open(POSTS_INDEX_FILE, "r", encoding="utf-8") as f:
            try:
                posts_data = json.load(f)
            except json.JSONDecodeError:
                print("Erro ao decodificar posts-index.json. Criando um novo.")
                
    posts_data["posts"].append(new_post_data)
    posts_data["last_updated"] = datetime.now().isoformat()
    
    with open(POSTS_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)
    print(f"posts-index.json atualizado com '{new_post_data['title']}'.")

if __name__ == '__main__':
    apply_seasonal_css()
    generate_post()

