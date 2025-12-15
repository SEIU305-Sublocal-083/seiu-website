
document.addEventListener('DOMContentLoaded', () => {
    const articlesGrid = document.getElementById('articles-grid');
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const tagsContainer = document.getElementById('tags-container');
    const featuredArticleSection = document.getElementById('featured-article-section');

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

            const featuredArticle = allArticles.find(article => article.featured);
            if (featuredArticle) {
                renderFeaturedArticle(featuredArticle);
            }

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
            details.className = 'relative group';
            const summary = document.createElement('summary');
            summary.className = 'cursor-pointer bg-brand-purple-light text-brand-purple-dark px-4 py-2 rounded-full text-sm font-semibold transition-colors hover:bg-brand-purple hover:text-white list-none flex items-center gap-1';
            summary.innerHTML = 'Campaigns <svg class="w-4 h-4 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>';

            const div = document.createElement('div');
            div.className = 'absolute z-10 mt-2 w-48 bg-white rounded-lg shadow-xl border border-border-color py-1 overflow-hidden';
            campaignTags.forEach(tag => {
                const link = document.createElement('a');
                link.href = '#';
                link.className = 'block px-4 py-2 text-sm text-text-secondary hover:bg-brand-purple-light hover:text-brand-purple-dark transition-colors';
                link.textContent = tag;
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    activeFilters.activeTag = tag;
                    setActiveTag(null); // Clear others
                    // Optional: indicate selection on dropdown
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
        button.className = 'tag-button px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 border border-transparent';
        button.textContent = tag;
        return button;
    }

    function setActiveTag(activeButton) {
        document.querySelectorAll('.tag-button').forEach(btn => btn.classList.remove('active'));
        if (activeButton) {
            activeButton.classList.add('active');
        }
    }

    function renderFeaturedArticle(article) {
        const altText = article.alt || article.title;
        // Make the featured card look impressive
        featuredArticleSection.innerHTML = `
            <div class="group bg-white rounded-2xl border border-border-color shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden">
                <a href="${article.url}" class="block relative">
                    <div class="grid lg:grid-cols-2 h-full">
                        <div class="relative overflow-hidden h-64 lg:h-auto order-last lg:order-last">
                            <img src="${article.image}" alt="${altText}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                            <div class="absolute inset-0 bg-brand-purple-dark/10 group-hover:bg-brand-purple-dark/0 transition-colors duration-500"></div>
                        </div>
                        <div class="p-8 lg:p-12 flex flex-col justify-center relative bg-white">
                            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-brand-purple to-violet-500 transform origin-left transition-transform duration-500 scale-x-0 group-hover:scale-x-100"></div>
                            <div class="flex items-center gap-3 mb-4">
                                <span class="bg-brand-purple text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider shadow-sm">Featured Story</span>
                                <span class="text-text-secondary text-sm font-medium">${new Date(article.publishedAt).toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'})}</span>
                            </div>
                            <h2 class="text-3xl lg:text-4xl font-bold mb-6 text-brand-dark group-hover:text-brand-purple transition-colors leading-tight font-serif">${article.title}</h2>
                            <p class="text-text-secondary text-lg mb-8 leading-relaxed">${article.description}</p>
                            <div class="flex items-center text-brand-purple font-bold tracking-wide group-hover:translate-x-2 transition-transform duration-300">
                                READ FULL STORY
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        `;
    }

    function renderArticles() {
        let filteredArticles = allArticles.filter(article => !article.featured);

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
            articlesGrid.innerHTML = `
                <div class="col-span-full py-12 text-center bg-white rounded-xl border border-dashed border-gray-300">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
                    <p class="text-xl text-text-secondary font-medium">No articles found.</p>
                    <p class="text-gray-500 mt-2">Try adjusting your search or filters.</p>
                </div>`;
            return;
        }

        articles.forEach(article => {
            const articleCard = document.createElement('div');
            // Added 'h-full' to make cards equal height
            articleCard.className = 'group bg-white rounded-xl border border-border-color shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden flex flex-col h-full hover:-translate-y-1';

            const formattedDate = new Date(article.publishedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
            const altText = article.alt || article.title;
            const primaryTag = article.tags && article.tags.length > 0 ? article.tags[0] : 'News';

            articleCard.innerHTML = `
                <a href="${article.url}" class="block relative overflow-hidden h-52 flex-shrink-0">
                    <img src="${article.image}" alt="${altText}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                    <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-md text-xs font-bold text-brand-purple uppercase tracking-wider shadow-sm">
                        ${primaryTag}
                    </div>
                </a>
                <div class="p-6 flex-grow flex flex-col">
                    <div class="mb-3 flex items-center text-xs text-text-secondary font-medium uppercase tracking-wide">
                        <svg class="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                        ${formattedDate}
                    </div>
                    <h3 class="font-serif font-bold text-xl mb-3 text-brand-dark group-hover:text-brand-purple transition-colors leading-tight line-clamp-2">
                        <a href="${article.url}">${article.title}</a>
                    </h3>
                    <p class="text-text-secondary text-sm line-clamp-3 mb-6 flex-grow">${article.description}</p>

                    <div class="mt-auto pt-4 border-t border-gray-100 flex items-center justify-between">
                        <div class="text-xs text-gray-500 font-medium">
                            ${article.author ? article.author.name : 'SEIU Local 503'}
                        </div>
                        <a href="${article.url}" class="text-brand-purple font-bold text-sm flex items-center group-hover:underline">
                            Read More <svg class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                        </a>
                    </div>
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
