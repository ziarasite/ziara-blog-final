# Plano de Implementação: Blog Preto e Branco com Feed de Artigos

## Objetivo
Transformar o blog existente em um design predominantemente preto e branco, com exceção das imagens que devem permanecer coloridas, e reorganizar a exibição das publicações em um formato de feed/artigo, mantendo o minimalismo.

## Análise Inicial
O blog utiliza `index.html` para a estrutura principal, `assets/css/style.css` para a estilização e `assets/js/main.js` para o carregamento dinâmico das publicações a partir de `posts-index.json` e arquivos HTML individuais em `posts/`.

## Fases de Implementação

### 1. Estilização Preto e Branco (assets/css/style.css)

#### 1.1. Definição de Variáveis CSS
Alterar as variáveis de cor no `:root` para uma paleta de tons de cinza, preto e branco. Isso garantirá consistência e facilidade de manutenção.

```css
:root {
    --primary-color: #1a1a1a; /* Preto quase absoluto para textos e elementos principais */
    --secondary-color: #4a4a4a; /* Cinza escuro para textos secundários */
    --accent-color: #7a7a7a; /* Cinza médio para detalhes e links */
    --text-color: #1a1a1a;
    --bg-color: #ffffff; /* Fundo branco */
    --light-gray: #f0f0f0; /* Cinza muito claro para seções de fundo */
    --border-color: #d0d0d0; /* Cinza claro para bordas */
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Sombra sutil */
    --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.15); /* Sombra mais pronunciada ao hover */
}
```

#### 1.2. Aplicação de Filtros CSS

*   Aplicar um filtro `grayscale(100%)` ao `body` para converter todo o conteúdo para preto e branco.
*   Remover o filtro `grayscale(100%)` das imagens (`img`) para que elas permaneçam coloridas. Isso pode ser feito com `filter: grayscale(0%);` ou `filter: none;` nas tags `img` ou em classes específicas para imagens.

#### 1.3. Ajustes Específicos de Cores
Revisar e ajustar manualmente quaisquer cores que não sejam cobertas pelas variáveis ou pelos filtros, como cores de links, fundos de botões, etc., para garantir que se encaixem na paleta preto e branco.

### 2. Layout de Feed/Artigo (index.html e assets/css/style.css)

#### 2.1. Estrutura do `index.html`
O `index.html` já possui uma seção `posts-section` com um `posts-grid`. A estrutura atual com `post-card` é adequada para um layout de feed. Será necessário garantir que os elementos dentro de `post-card` exibam as informações relevantes (título, imagem, excerto, data, categoria).

#### 2.2. Ajustes CSS para o Layout (assets/css/style.css)

*   **`posts-grid`**: Manter o `display: grid` para organizar os posts. Ajustar `grid-template-columns` para um layout de coluna única em telas menores e múltiplas colunas em telas maiores, se necessário, para otimizar a visualização como feed.
*   **`post-card`**: Garantir que cada cartão de postagem seja visualmente distinto e contenha os elementos necessários.
*   **`post-image`**: A imagem representativa deve ser proeminente. Manter `object-fit: cover` para garantir que as imagens preencham o espaço sem distorção.
*   **`post-content`**: Organizar o conteúdo (título, meta, excerto, link) de forma clara e legível dentro do cartão.

### 3. Inclusão de Imagens Representativas (assets/js/main.js e posts-index.json)

#### 3.1. `posts-index.json`
Verificar se o `posts-index.json` contém o caminho para a imagem representativa de cada post. Se não, será necessário adicionar um campo `image` a cada entrada.

Exemplo:
```json
[
    {
        "id": "post-1",
        "title": "Título do Post 1",
        "date": "2025-10-15",
        "category": "Notícias",
        "excerpt": "Um breve resumo do conteúdo do post 1.",
        "image": "assets/images/post_image_1.png",
        "url": "posts/post-1.html"
    }
]
```

#### 3.2. `assets/js/main.js`
Modificar a função que carrega e exibe os posts para incluir a imagem representativa. O código JavaScript deve criar um elemento `<img>` e atribuir o `src` com base no campo `image` do `posts-index.json`.

Exemplo de modificação na criação do `post-card`:

```javascript
// Dentro da função que cria o post-card
const postImage = document.createElement('img');
postImage.src = post.image; // Assumindo que 'post.image' contém o caminho da imagem
postImage.alt = post.title; // Alt text para acessibilidade
postImage.classList.add('post-image');
postCard.appendChild(postImage);

// ... restante do código para título, excerto, etc.
```

### 4. Manutenção do Minimalismo

*   **Tipografia**: Manter fontes limpas e legíveis. O `font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;` já é uma boa escolha.
*   **Espaçamento**: Utilizar espaçamento adequado entre os elementos para evitar sobrecarga visual.
*   **Elementos Decorativos**: Evitar elementos gráficos desnecessários. O foco deve ser no conteúdo.

### 5. Testes

*   **Visualização**: Abrir `index.html` no navegador para verificar se o tema preto e branco foi aplicado corretamente e se as imagens estão coloridas.
*   **Responsividade**: Testar em diferentes tamanhos de tela para garantir que o layout de feed se adapte bem.
*   **Funcionalidade**: Verificar se os links dos posts funcionam e se o carregamento dinâmico está correto.

## Próximos Passos

1.  Implementar as alterações no `style.css`.
2.  Atualizar `posts-index.json` com os caminhos das imagens (se necessário).
3.  Modificar `main.js` para exibir as imagens.
4.  Realizar testes e ajustes finos.

