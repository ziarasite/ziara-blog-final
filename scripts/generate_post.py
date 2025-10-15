
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from slugify import slugify
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

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

# Paletas de cores (agora fixas para preto e branco, mas mantendo a estrutura para futuras expansões)
PALETTES = {
    "primary":"#000000",
    "secondary":"#333333",
    "accent":"#666666",
    "bg":"#ffffff",
    "light_gray":"#f5f5f5"
}

def apply_seasonal_css():
    # Usar paleta fixa para preto e branco
    pal = PALETTES
    css_content = f"""/* style.css gerado automaticamente */\n\n:root {{\n    --primary-color: {pal["primary"]};\n    --secondary-color: {pal["secondary"]};\n    --accent-color: {pal["accent"]};\n    --text-color: #1a1a1a;\n    --bg-color: {pal["bg"]};\n    --light-gray: {pal["light_gray"]};\n    --border-color: #e0e0e0;\n    --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);\n    --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.12);\n}}\n\n* {{\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}}\n\nbody {{\n    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n    line-height: 1.6;\n    color: var(--text-color);\n    background-color: var(--bg-color);\n}}\n\n.container {{\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 0 20px;\n}}\n\n/* Header */\n.header {{\n    background: var(--primary-color);\n    color: var(--bg-color);\n    padding: 2.5rem 0;\n    border-bottom: 1px solid var(--border-color);\n}}\n\n.logo-area {{\n    text-align: center;\n    margin-bottom: 1rem;\n}}\n\n.logo {{\n    font-size: 2.8rem;\n    font-weight: 700;\n    color: var(--bg-color);\n    text-transform: uppercase;\n    letter-spacing: 4px;\n    margin-bottom: 0.5rem;\n}}\n\n.subtitle {{\n    font-size: 0.95rem;\n    color: #cccccc;\n    font-style: italic;\n    font-weight: 300;\n}}\n\n.tagline {{\n    text-align: center;\n    font-size: 1rem;\n    color: #e0e0e0;\n    margin-top: 0.5rem;\n    font-weight: 300;\n}}\n\n/* Main Content */\nmain {{\n    padding: 3rem 0;\n}}\n\n.intro {{\n    background: var(--light-gray);\n    padding: 2.5rem;\n    border-radius: 2px;\n    margin-bottom: 3rem;\n    border-left: 3px solid var(--primary-color);\n}}\n\n.intro h2 {{\n    color: var(--primary-color);\n    margin-bottom: 1rem;\n    font-size: 1.8rem;\n    font-weight: 600;\n}}\n\n.intro p {{\n    font-size: 1.05rem;\n    line-height: 1.8;\n    color: var(--secondary-color);\n}}\n\n/* Posts Section */\n.posts-section {{\n    margin-bottom: 3rem;\n}}\n\n.section-title {{\n    font-size: 2rem;\n    color: var(--primary-color);\n    margin-bottom: 2.5rem;\n    padding-bottom: 0.75rem;\n    border-bottom: 2px solid var(--primary-color);\n    font-weight: 600;\n}}\n\n.posts-grid {{\n    display: grid;\n    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));\n    gap: 2rem;\n}}\n\n.post-card {{\n    background: var(--bg-color);\n    border-radius: 2px;\n    overflow: hidden;\n    box-shadow: var(--shadow);\n    transition: transform 0.3s ease, box-shadow 0.3s ease;\n    border: 1px solid var(--border-color);\n}}\n\n.post-card:hover {{\n    transform: translateY(-5px);\n    box-shadow: var(--shadow-hover);\n}}\n\n.post-image {{\n    width: 100%;\n    height: 200px;\n    object-fit: cover;\n    background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);\n}}\n\n.post-content {{\n    padding: 1.5rem;\n}}\n\n.post-meta {{\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    margin-bottom: 1rem;\n    font-size: 0.85rem;\n    color: var(--accent-color);\n}}\n\n.post-date {{\n    display: flex;\n    align-items: center;\n    gap: 0.3rem;\n}}\n\n.post-category {{\n    background: var(--primary-color);\n    color: var(--bg-color);\n    padding: 0.3rem 0.8rem;\n    border-radius: 2px;\n    font-size: 0.75rem;\n    font-weight: 600;\n    text-transform: uppercase;\n    letter-spacing: 0.5px;\n}}\n\n.post-title {{\n    font-size: 1.4rem;\n    color: var(--primary-color);\n    margin-bottom: 0.8rem;\n    line-height: 1.3;\n    font-weight: 600;\n}}\n\n.post-title a {{\n    color: inherit;\n    text-decoration: none;\n    transition: color 0.3s ease;\n}}\n\n.post-title a:hover {{\n    color: var(--accent-color);\n}}\n\n.post-excerpt {{\n    color: var(--secondary-color);\n    line-height: 1.6;\n    margin-bottom: 1rem;\n}}\n\n.post-link {{\n    display: inline-block;\n    color: var(--primary-color);\n    text-decoration: none;\n    font-weight: 600;\n    transition: color 0.3s ease;\n    text-transform: uppercase;\n    font-size: 0.85rem;\n    letter-spacing: 0.5px;\n}}\n\n.post-link:hover {{\n    color: var(--accent-color);\n}}\n\n.loading {{\n    text-align: center;\n    color: var(--accent-color);\n    font-style: italic;\n    padding: 2rem;\n}}\n\n/* Footer */\n.footer {{\n    background: var(--primary-color);\n    color: var(--bg-color);\n    padding: 2rem 0;\n    text-align: center;\n    margin-top: 4rem;\n    border-top: 1px solid var(--border-color);\n}}\n\n.footer p {{\n    margin-bottom: 0.5rem;\n}}\n\n.footer-note {{\n    font-size: 0.85rem;\n    color: #cccccc;\n    font-weight: 300;\n}}\n\n/* Responsive */\n@media (max-width: 768px) {{\n    .logo {{\n        font-size: 2rem;\n    }}\n    \n    .posts-grid {{\n        grid-template-columns: 1fr;\n    }}\n    \n    .intro h2 {{\n        font-size: 1.5rem;\n    }}\n    \n    .section-title {{\n        font-size: 1.6rem;\n    }}\n}}\n\n/* Post Detail Page */\n.post-detail {{\n    background: var(--bg-color);\n    padding: 3rem;\n    border-radius: 2px;\n    box-shadow: var(--shadow);\n    margin-bottom: 2rem;\n    border: 1px solid var(--border-color);\n}}\n\n.post-detail .post-header {{\n    margin-bottom: 2rem;\n    padding-bottom: 1.5rem;\n    border-bottom: 2px solid var(--border-color);\n}}\n\n.post-detail .post-title {{\n    font-size: 2.5rem;\n    margin-bottom: 1rem;\n}}\n\n.post-detail .post-image {{\n    width: 100%;\n    height: auto;\n    max-height: 400px;\n    margin-bottom: 2rem;\n    border-radius: 2px;\n}}\n\n.post-detail .post-body {{\n    font-size: 1.1rem;\n    line-height: 1.8;\n    color: var(--text-color);\n}}\n\n.post-detail .post-body p {{\n    margin-bottom: 1.5rem;\n}}\n\n.post-detail .post-body h3 {{\n    color: var(--primary-color);\n    margin-top: 2rem;\n    margin-bottom: 1rem;\n    font-weight: 600;\n}}\n\n.post-detail .post-body table {{
    width: 100%;\n    border-collapse: collapse;\n    margin: 2rem 0;\n}}\n\n.post-detail .post-body table th,\n.post-detail .post-body table td {{\n    border: 1px solid var(--border-color);\n    padding: 0.75rem;\n    text-align: left;\n}}\n\n.post-detail .post-body table th {{\n    background: var(--light-gray);\n    font-weight: 600;\n    color: var(--primary-color);\n}}\n\n.post-detail .post-body img {{\n    max-width: 100%;\n    height: auto;\n    margin: 1.5rem 0;\n    border-radius: 2px;\n}}\n\n.back-link {{\n    display: inline-block;\n    margin-bottom: 2rem;\n    color: var(--primary-color);\n    text-decoration: none;\n    font-weight: 600;\n    transition: color 0.3s ease;\n    text-transform: uppercase;\n    font-size: 0.9rem;\n    letter-spacing: 0.5px;\n}}\n\n.back-link:hover {{\n    color: var(--accent-color);\n}}\n"""
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
    pal = PALETTES
    draw.rectangle([0,0,img_w,220], fill=pal["primary"])
    
    # Centralizar o texto do título
    text_width, text_height = draw.textbbox((0,0), title, font=font_title)[2:]
    text_x = (img_w - text_width) / 2
    text_y = (220 - text_height) / 2 # Centralizar verticalmente na faixa de 220px
    draw.text((text_x, text_y), title, fill=(255,255,255), font=font_title) # Texto branco no fundo preto
    
    path = os.path.join(IMAGES_DIR, filename)
    img.save(path, format="PNG")
    return os.path.join("assets", "images", filename).replace("\\", "/") # Caminho relativo para o HTML

def generate_chart_image(data, filename):
    df = pd.DataFrame(data)
    
    plt.style.use('seaborn-v0_8-whitegrid') # Estilo mais limpo
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Exemplo de gráfico de barras simples
    if 'label' in df.columns and 'value' in df.columns:
        ax.bar(df['label'], df['value'], color=PALETTES["primary"])
        ax.set_title('Dados do Mercado de Joias', color=PALETTES["primary"])
        ax.set_xlabel('Categoria', color=PALETTES["secondary"])
        ax.set_ylabel('Valor', color=PALETTES["secondary"])
        ax.tick_params(axis='x', colors=PALETTES["secondary"])
        ax.tick_params(axis='y', colors=PALETTES["secondary"])
    else:
        # Fallback para um gráfico vazio ou erro
        ax.text(0.5, 0.5, 'Dados insuficientes para gráfico', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, color=PALETTES["accent"])

    # Ajustes para esquema de cores P&B
    fig.patch.set_facecolor(PALETTES["bg"])
    ax.set_facecolor(PALETTES["bg"])
    ax.spines['top'].set_color(PALETTES["border_color"])
    ax.spines['right'].set_color(PALETTES["border_color"])
    ax.spines['bottom'].set_color(PALETTES["border_color"])
    ax.spines['left'].set_color(PALETTES["border_color"])
    ax.xaxis.label.set_color(PALETTES["secondary"])
    ax.yaxis.label.set_color(PALETTES["secondary"])
    ax.title.set_color(PALETTES["primary"])
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    
    path = os.path.join(IMAGES_DIR, filename)
    with open(path, 'wb') as f:
        f.write(buf.getvalue())
    return os.path.join("assets", "images", filename).replace("\\", "/")

def generate_content_with_llm():
    prompt = (
        "Gere um título, um lead, um corpo de texto detalhado (em HTML com tags <p> e <h3> para subtítulos), "
        "e uma categoria para uma notícia diária sobre o mundo de joias e semijoias, "
        "focada em atacadistas e comerciantes. O conteúdo deve ser profissional, informativo e ter entre 400-700 palavras. "
        "Inclua:
        "- **Dicas de moda e tendências:** Baseadas nas altas mais pesquisadas na internet para o setor.
        "- **Sugestão de imagem:** Uma breve descrição para uma imagem que complemente o texto.
        "- **Dados para uma tabela ou gráfico:** Forneça dados fictícios relevantes para o setor (ex: vendas por tipo de joia, variação de preço de matéria-prima, popularidade de tendências) em formato JSON, com chaves como `table_data` (para tabela) ou `chart_data` (para gráfico). Se for tabela, inclua `headers` e `rows`. Se for gráfico, inclua `labels` e `values`.
        "- **Tópicos de interesse:** Aborde aspectos como materiais inovadores, design, marketing digital para joias, sustentabilidade ou eventos do setor."
        "Formate a saída como um JSON com as chaves 'title', 'lead', 'body', 'category', 'image_description', 'table_data' (opcional) e 'chart_data' (opcional)."
    )
    
    response = client.chat.completions.create(
        model="gemini-2.5-flash", # Usando o modelo flash para rapidez
        messages=[
            {"role": "system", "content": "Você é um especialista em mercado de joias e semijoias, focado em atacadistas e comerciantes. Seu conteúdo é minimalista, profissional e focado em preto e branco."},
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
        return {"title": "Erro na Geração de Conteúdo", "lead": "Houve um problema ao gerar o conteúdo. Tente novamente.", "body": "<p>Não foi possível obter o conteúdo do LLM.</p>", "category": "Erro"}
    return content

def generate_post():
    today = datetime.now()
    
    # Gerar conteúdo com LLM
    llm_content = generate_content_with_llm()
    title = llm_content.get("title", f"Atualização do Mercado {today.strftime('%d/%m/%Y')}")
    lead = llm_content.get("lead", "Confira as últimas novidades do setor.")
    body = llm_content.get("body", "<p>Nenhuma informação detalhada disponível.</p>")
    category = llm_content.get("category", "Notícias do Setor")
    image_description = llm_content.get("image_description", title)
    table_data = llm_content.get("table_data")
    chart_data = llm_content.get("chart_data")
    
    slug = slugify(f"{title}-{today.strftime('%Y%m%d%H%M%S')}") # Adiciona H M S para unicidade
    filename = f"{slug}.html"
    
    # Gerar imagem destacada (título)
    image_name = f"post_{today.strftime('%Y%m%d%H%M%S')}.png"
    image_path_for_html = make_featured_image(image_description, image_name)
    
    # Processar tabela
    table_html = ""
    if table_data and "headers" in table_data and "rows" in table_data:
        table_html = "<table><thead><tr>"
        for header in table_data["headers"]:
            table_html += f"<th>{header}</th>"
        table_html += "</tr></thead><tbody>"
        for row in table_data["rows"]:
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"
        body = body.replace("[TABLE_PLACEHOLDER]", table_html) # Substituir placeholder no corpo
    
    # Processar gráfico
    chart_image_html = ""
    if chart_data and "labels" in chart_data and "values" in chart_data:
        chart_image_name = f"chart_{today.strftime('%Y%m%d%H%M%S')}.png"
        chart_path_for_html = generate_chart_image(pd.DataFrame(chart_data), chart_image_name)
        chart_image_html = f"<img src=\"../{chart_path_for_html}\" alt=\"Gráfico de {title}\" style=\"max-width: 100%; height: auto; margin: 1.5rem 0; border-radius: 2px;\">"
        body = body.replace("[CHART_PLACEHOLDER]", chart_image_html) # Substituir placeholder no corpo

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

