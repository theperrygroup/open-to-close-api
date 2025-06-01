/* Open To Close API Documentation JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    
    // Add copy functionality to code blocks
    function addCopyButtons() {
        const codeBlocks = document.querySelectorAll('pre > code');
        
        codeBlocks.forEach(function(codeBlock) {
            const pre = codeBlock.parentNode;
            
            // Skip if copy button already exists
            if (pre.querySelector('.copy-button')) {
                return;
            }
            
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-button';
            copyButton.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/>
                </svg>
                Copy
            `;
            copyButton.title = 'Copy to clipboard';
            
            copyButton.addEventListener('click', function() {
                navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                    copyButton.innerHTML = `
                        <svg viewBox="0 0 24 24" width="16" height="16">
                            <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
                        </svg>
                        Copied!
                    `;
                    copyButton.classList.add('copied');
                    
                    setTimeout(function() {
                        copyButton.innerHTML = `
                            <svg viewBox="0 0 24 24" width="16" height="16">
                                <path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"/>
                            </svg>
                            Copy
                        `;
                        copyButton.classList.remove('copied');
                    }, 2000);
                });
            });
            
            pre.style.position = 'relative';
            pre.appendChild(copyButton);
        });
    }
    
    // Add API endpoint badges
    function addEndpointBadges() {
        const headers = document.querySelectorAll('h3, h4');
        
        headers.forEach(function(header) {
            const text = header.textContent.toLowerCase();
            let method = null;
            
            if (text.includes('get ') || text.includes('list ') || text.includes('retrieve ')) {
                method = 'get';
            } else if (text.includes('post ') || text.includes('create ')) {
                method = 'post';
            } else if (text.includes('put ') || text.includes('update ')) {
                method = 'put';
            } else if (text.includes('delete ') || text.includes('remove ')) {
                method = 'delete';
            }
            
            if (method) {
                const badge = document.createElement('span');
                badge.className = `endpoint-method ${method}`;
                badge.textContent = method.toUpperCase();
                header.insertBefore(badge, header.firstChild);
            }
        });
    }
    
    // Add smooth scrolling for anchor links
    function addSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Add status badges for API methods
    function addStatusBadges() {
        const codeSpans = document.querySelectorAll('code');
        
        codeSpans.forEach(function(span) {
            const text = span.textContent;
            
            // Add status badges for common API statuses
            if (text.match(/\b(available|stable|ready)\b/i)) {
                span.classList.add('status-badge', 'available');
            } else if (text.match(/\b(deprecated|legacy)\b/i)) {
                span.classList.add('status-badge', 'deprecated');
            } else if (text.match(/\b(beta|experimental|preview)\b/i)) {
                span.classList.add('status-badge', 'beta');
            }
        });
    }
    
    // Enhanced search functionality
    function enhanceSearch() {
        const searchInput = document.querySelector('.md-search__input');
        
        if (searchInput) {
            // Add search suggestions for API endpoints
            const commonSearches = [
                'contacts', 'properties', 'agents', 'teams', 'tags', 
                'users', 'documents', 'emails', 'notes', 'tasks',
                'authentication', 'error handling', 'rate limits'
            ];
            
            searchInput.addEventListener('focus', function() {
                // Could implement autocomplete here
                console.log('Search focused - implement autocomplete for:', commonSearches);
            });
        }
    }
    
    // Add real estate property examples highlighting
    function highlightPropertyExamples() {
        const codeBlocks = document.querySelectorAll('pre code');
        
        codeBlocks.forEach(function(block) {
            const content = block.textContent;
            
            // Highlight property-related JSON structures
            if (content.includes('"address"') || content.includes('"property_type"') || content.includes('"listing_price"')) {
                block.parentNode.classList.add('property-example-code');
            }
        });
    }
    
    // Add table of contents highlighting
    function addTocHighlighting() {
        const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        const tocLinks = document.querySelectorAll('.md-nav__link');
        
        function updateActiveHeader() {
            let activeHeader = null;
            
            headers.forEach(function(header) {
                const rect = header.getBoundingClientRect();
                if (rect.top <= 100 && rect.bottom >= 0) {
                    activeHeader = header;
                }
            });
            
            tocLinks.forEach(function(link) {
                link.classList.remove('active-section');
                if (activeHeader && link.getAttribute('href') === '#' + activeHeader.id) {
                    link.classList.add('active-section');
                }
            });
        }
        
        window.addEventListener('scroll', updateActiveHeader);
        updateActiveHeader();
    }
    
    // Initialize all enhancements
    addCopyButtons();
    addEndpointBadges();
    addSmoothScrolling();
    addStatusBadges();
    enhanceSearch();
    highlightPropertyExamples();
    addTocHighlighting();
    
    // Add observer for dynamic content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                addCopyButtons();
                addEndpointBadges();
                addStatusBadges();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('Open To Close API Documentation enhancements loaded');
});

// Add CSS for copy buttons and other enhancements
const style = document.createElement('style');
style.textContent = `
    .copy-button {
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        opacity: 0;
        transition: opacity 0.2s;
        z-index: 10;
    }
    
    pre:hover .copy-button {
        opacity: 1;
    }
    
    .copy-button:hover {
        background: rgba(0, 0, 0, 0.9);
    }
    
    .copy-button.copied {
        background: #2e7d32;
    }
    
    .copy-button svg {
        width: 14px;
        height: 14px;
    }
    
    .property-example-code {
        border-left: 4px solid #4caf50 !important;
        background: #f1f8e9 !important;
    }
    
    .active-section {
        color: #2e7d32 !important;
        font-weight: 600;
    }
`;
document.head.appendChild(style); 