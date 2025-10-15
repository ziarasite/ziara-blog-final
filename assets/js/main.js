// ZIARA TESTE - Sistema de Carregamento de Posts

async function loadAllPosts() {
    try {
        const response = await fetch('./posts-index.json');
        const data = await response.json();
        
        const postsContainer = document.getElementById('posts-container');
        
        if (!data.posts || data.posts.length === 0) {
            postsContainer.innerHTML = '<p class="loading">Nenhuma publicação disponível ainda.</p>';
            return;
        }
        
        // Ordenar posts por data (mais recente primeiro)
        const sortedPosts = data.posts.sort((a, b) => {
            return new Date(b.timestamp) - new Date(a.timestamp);
        });
        
        // Limpar container
        postsContainer.innerHTML = '';
        
        // Renderizar cada post
        sortedPosts.forEach(post => {
            const postCard = createPostCard(post);
            postsContainer.appendChild(postCard);
        });
        
    } catch (error) {
        console.error('Erro ao carregar posts:', error);
        document.getElementById('posts-container').innerHTML = 
            '<p class="loading">Erro ao carregar publicações. Por favor, tente novamente mais tarde.</p>';
    }
}

function createPostCard(post) {
    const card = document.createElement('div');
    card.className = 'post-card';
    
    const imageUrl = post.image || 'assets/images/default-post.png';
    const excerpt = post.excerpt || post.summary || 'Clique para ler mais...';
    const category = post.category || 'Notícias';
    
    card.innerHTML = `
        ${post.image ? `<img src="${imageUrl}" alt="${post.title}" class="post-image">` : '<div class="post-image"></div>'}
        <div class="post-content">
            <div class="post-meta">
                <span class="post-date">📅 ${formatDate(post.date)}</span>
                <span class="post-category">${category}</span>
            </div>
            <h3 class="post-title">
                <a href="posts/${post.filename}">${post.title}</a>
            </h3>
            <p class="post-excerpt">${excerpt}</p>
            <a href="posts/${post.filename}" class="post-link">Ler mais →</a>
        </div>
    `;
    
    return card;
}

function formatDate(dateString) {
    // Espera formato DD/MM/YYYY ou ISO
    if (dateString.includes('/')) {
        return dateString;
    }
    
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${day}/${month}/${year}`;
}

// Carregar posts quando a página carregar
document.addEventListener('DOMContentLoaded', loadAllPosts);

