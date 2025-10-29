
document.addEventListener('DOMContentLoaded', () => {
    const articlesGrid = document.getElementById('articles-grid');
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const tagsContainer = document.getElementById('tags-container');

    let allArticles = [];
    let activeFilters = {
        searchTerm: '',
        sortOrder: 'newest',
        activeTag: null
    };

    async function loadNews() {
        try {
            const response = await fetch('news/news.json');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            allArticles = await response.json();

            // Sort by publishedAt date descending by default
            allArticles.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

            populateTags(allArticles);
            renderArticles();
        } catch (error) {
            console.error("Could not fetch news:", error);
            articlesGrid.innerHTML = '<p class="text-text-secondary col-span-full text-center">Could not load news articles at this time.</p>';
        }
    }

    function populateTags(articles) {
        const allTags = new Set();
        articles.forEach(article => {
            article.tags.forEach(tag => allTags.add(tag));
        });

        const campaigns = new Set(['2026 Bargaining', '2026 Elections']);
        const regularTags = [...allTags].filter(tag => !campaigns.has(tag));

        // "All" button
        const allButton = createTagButton('All');
        allButton.classList.add('active');
        allButton.addEventListener('click', () => {
            activeFilters.activeTag = null;
            setActiveTag(allButton);
            renderArticles();
        });
        tagsContainer.appendChild(allButton);

        // Regular tags
        regularTags.forEach(tag => {
            const button = createTagButton(tag);
            button.addEventListener('click', () => {
                activeFilters.activeTag = tag;
                setActiveTag(button);
                renderArticles();
            });
            tagsContainer.appendChild(button);
        });

        // Campaigns dropdown
        const campaignTags = [...allTags].filter(tag => campaigns.has(tag));
        if (campaignTags.length > 0) {
            const details = document.createElement('details');
            details.className = 'relative';
            const summary = document.createElement('summary');
            summary.className = 'cursor-pointer bg-brand-purple-light text-brand-purple-dark px-4 py-2 rounded-full text-sm font-semibold transition-colors hover:bg-brand-purple hover:text-white';
            summary.textContent = 'Campaigns';
            const div = document.createElement('div');
            div.className = 'absolute z-10 mt-2 w-48 bg-white rounded-md shadow-lg border border-border-color';
            campaignTags.forEach(tag => {
                const link = document.createElement('a');
                link.href = '#';
                link.className = 'block px-4 py-2 text-sm text-text-secondary hover:bg-gray-100';
                link.textContent = tag;
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    activeFilters.activeTag = tag;
                    setActiveTag(null);
                    summary.textContent = tag;
                    details.removeAttribute('open');
                    renderArticles();
                });
                div.appendChild(link);
            });

            details.appendChild(summary);
            details.appendChild(div);
            tagsContainer.appendChild(details);
        }
    }

    function createTagButton(tag) {
        const button = document.createElement('button');
        button.className = 'tag-button bg-brand-purple-light text-brand-purple-dark px-4 py-2 rounded-full text-sm font-semibold transition-colors hover:bg-brand-purple hover:text-white';
        button.textContent = tag;
        return button;
    }

    function setActiveTag(activeButton) {
        document.querySelectorAll('.tag-button').forEach(btn => btn.classList.remove('active'));
        if (activeButton) {
            activeButton.classList.add('active');
        }
    }

    function renderArticles() {
        let filteredArticles = [...allArticles];

        // Filter by search term
        if (activeFilters.searchTerm) {
            const term = activeFilters.searchTerm.toLowerCase();
            filteredArticles = filteredArticles.filter(article =>
                article.title.toLowerCase().includes(term) ||
                article.description.toLowerCase().includes(term)
            );
        }

        // Filter by tag
        if (activeFilters.activeTag) {
            filteredArticles = filteredArticles.filter(article => article.tags.includes(activeFilters.activeTag));
        }

        // Sort
        if (activeFilters.sortOrder === 'newest') {
            filteredArticles.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
        } else {
            filteredArticles.sort((a, b) => new Date(a.publishedAt) - new Date(b.publishedAt));
        }

        displayArticles(filteredArticles);
    }

    function displayArticles(articles) {
        articlesGrid.innerHTML = '';

        if (articles.length === 0) {
            articlesGrid.innerHTML = '<p class="text-text-secondary col-span-full text-center">No news articles match your criteria.</p>';
            return;
        }

        articles.forEach(article => {
            const articleCard = document.createElement('div');
            articleCard.className = 'bg-white rounded-xl border border-border-color overflow-hidden flex flex-col';

            const formattedDate = new Date(article.updatedAt + 'T00:00:00').toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const dateTooltip = `Created: ${article.createdAt}\nPublished: ${article.publishedAt}\nUpdated: ${article.updatedAt}`;

            articleCard.innerHTML = `
                <a href="${article.url}" class="block group">
                    <img src="${article.image}" alt="${article.title}" class="w-full h-48 object-cover">
                    <div class="p-6 flex-grow">
                        <div class="flex items-center justify-between mb-2">
                            <p class="text-text-secondary text-sm" title="${dateTooltip}">Last updated: ${formattedDate}</p>
                        </div>
                        <h3 class="font-bold text-xl mb-3 group-hover:text-brand-purple transition-colors">${article.title}</h3>
                        <p class="text-text-secondary">${article.description}</p>
                        <div class="mt-4 flex flex-wrap gap-2">
                            ${article.tags.map(tag => `<span class="bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs">${tag}</span>`).join('')}
                        </div>
                    </div>
                </a>
                <div class="bg-gray-50 border-t border-border-color p-4">
                     <p class="text-sm text-text-secondary">${article.author.name} - ${article.author.title}</p>
                </div>
            `;
            articlesGrid.appendChild(articleCard);
        });
    }

    searchInput.addEventListener('input', (e) => {
        activeFilters.searchTerm = e.target.value;
        renderArticles();
    });

    sortSelect.addEventListener('change', (e) => {
        activeFilters.sortOrder = e.target.value;
        renderArticles();
    });

    loadNews();
});
