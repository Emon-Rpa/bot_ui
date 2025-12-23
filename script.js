// API endpoints
const API_PLATFORMS = '/api/platforms';
const API_GROUPS = '/api/groups';
const API_MESSAGES = '/api/messages';

// Icons
const ICON_FB = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.248h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>';
const ICON_MESSENGER = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 0C5.373 0 0 4.974 0 11.111c0 3.498 1.744 6.614 4.469 8.654V24l4.088-2.242c1.092.303 2.25.464 3.443.464 6.627 0 12-4.974 12-11.111C24 4.974 18.627 0 12 0zm1.291 14.194l-3.239-3.454-6.325 3.454 6.956-7.394 3.239 3.454 6.325-3.454-6.956 7.394z"/></svg>';
const ICON_WHATSAPP = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';

// DOM elements
const titleElement = document.getElementById('title');
const subtitleElement = document.getElementById('subtitle');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const messagesContainer = document.getElementById('messagesContainer');
const groupsList = document.getElementById('groupsList');
const groupCount = document.getElementById('groupCount');
const sidebarTitle = document.getElementById('sidebarTitle');
const messengerTab = document.getElementById('messengerTab');
const whatsappTab = document.getElementById('whatsappTab');
const messengerCount = document.getElementById('messengerCount');
const whatsappCount = document.getElementById('whatsappCount');
const headerActions = document.getElementById('headerActions');
const btnSource1 = document.getElementById('btnSource1');
const btnSource2 = document.getElementById('btnSource2');
const btnText1 = document.getElementById('btnText1');
const btnText2 = document.getElementById('btnText2');
const btnIcon1 = document.getElementById('btnIcon1');
const btnIcon2 = document.getElementById('btnIcon2');

// State
let currentPlatform = 'messenger';
let currentItem = null;
let allItems = [];

// Initialize app
async function init() {
    await loadPlatforms();
    setupPlatformTabs();
}

// Load platform counts
async function loadPlatforms() {
    try {
        const response = await fetch(API_PLATFORMS);
        if (!response.ok) throw new Error('Failed to fetch platforms');

        const data = await response.json();
        const platforms = data.platforms || [];

        // Update counts
        platforms.forEach(platform => {
            if (platform.name === 'messenger') {
                messengerCount.textContent = platform.count;
            } else if (platform.name === 'whatsapp') {
                whatsappCount.textContent = platform.count;
            }
        });

        // Load default platform
        await switchPlatform(currentPlatform);

    } catch (error) {
        console.error('Error loading platforms:', error);
    }
}

// Setup platform tab click handlers
function setupPlatformTabs() {
    messengerTab.addEventListener('click', () => switchPlatform('messenger'));
    whatsappTab.addEventListener('click', () => switchPlatform('whatsapp'));
}

// Switch between platforms
async function switchPlatform(platform) {
    currentPlatform = platform;
    currentItem = null;

    // Update active tab
    document.querySelectorAll('.platform-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    if (platform === 'messenger') {
        messengerTab.classList.add('active');
        sidebarTitle.textContent = 'Message Groups';
    } else {
        whatsappTab.classList.add('active');
        sidebarTitle.textContent = 'WhatsApp Authors';
    }

    // Load items for this platform
    await loadItems();
}

// Load groups/channels for current platform
async function loadItems() {
    try {
        const response = await fetch(`${API_GROUPS}?platform=${currentPlatform}`);
        if (!response.ok) throw new Error('Failed to fetch items');

        const data = await response.json();

        if (currentPlatform === 'messenger') {
            // Flatten the nested structure: authors with channels -> just channels
            const authors = data.authors || [];
            allItems = [];
            authors.forEach(author => {
                if (author.channels) {
                    author.channels.forEach(channel => {
                        // Store author info in the channel for reference
                        allItems.push({
                            ...channel,
                            author_id: author.author_id,
                            author_name: author.author_name
                        });
                    });
                }
            });
            groupCount.textContent = `${allItems.length} channel${allItems.length !== 1 ? 's' : ''}`;
        } else {
            allItems = data.channels || [];
            groupCount.textContent = `${allItems.length} channel${allItems.length !== 1 ? 's' : ''}`;
        }

        renderItemsList();

        // Load first item by default
        if (allItems.length > 0) {
            if (currentPlatform === 'messenger') {
                const firstChannel = allItems[0];
                loadItem(firstChannel.author_id, firstChannel.source);
            } else {
                loadItem(null, allItems[0].Source_name);
            }
        } else {
            loadingElement.style.display = 'none';
            messagesContainer.innerHTML = '<div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">No data available</div>';
        }

    } catch (error) {
        console.error('Error loading items:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
    }
}

// Render items list in sidebar
function renderItemsList() {
    groupsList.innerHTML = '';

    if (allItems.length === 0) {
        groupsList.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-secondary);">No items yet</div>';
        return;
    }

    if (currentPlatform === 'messenger') {
        // Render flattened channels
        allItems.forEach(channel => {
            const channelElement = createChannelElement(channel, channel.author_id);
            groupsList.appendChild(channelElement);
        });
    } else {
        // Render WhatsApp channels
        allItems.forEach(item => {
            const itemElement = createItemElement(item);
            groupsList.appendChild(itemElement);
        });
    }
}

// Create channel element (for Messenger channels)
function createChannelElement(channel, authorId) {
    const element = document.createElement('div');
    element.className = 'channel-item flat-item';

    if (currentItem === `${authorId}:${channel.source}`) {
        element.classList.add('active');
    }

    const channelContent = document.createElement('div');
    channelContent.className = 'channel-content';

    const title = document.createElement('div');
    title.className = 'channel-title';
    title.textContent = channel.Title || 'Untitled';

    const subtitle = document.createElement('div');
    subtitle.className = 'channel-subtitle';
    subtitle.textContent = channel.Sub_Title || 'No description';

    const meta = document.createElement('div');
    meta.className = 'channel-meta';
    meta.innerHTML = `
        <span>${channel.message_count || 0} messages</span>
        <span>${channel.last_updated ? formatDate(channel.last_updated) : ''}</span>
    `;

    channelContent.appendChild(title);
    channelContent.appendChild(subtitle);
    channelContent.appendChild(meta);

    const channelIcon = document.createElement('img');
    channelIcon.className = 'channel-icon-sidebar';
    channelIcon.src = channel.icon || 'https://via.placeholder.com/32';
    channelIcon.alt = channel.Title;
    channelIcon.loading = 'lazy';

    element.appendChild(channelIcon);
    element.appendChild(channelContent);

    element.addEventListener('click', (e) => {
        loadItem(authorId, channel.source);
    });

    return element;
}

// Create item element for sidebar (WhatsApp only)
function createItemElement(item) {
    const element = document.createElement('div');
    element.className = 'group-item';

    const identifier = item.Source_name;
    if (currentItem === identifier) {
        element.classList.add('active');
    }

    const title = document.createElement('div');
    title.className = 'group-title';
    title.textContent = identifier || 'Untitled';

    const subtitle = document.createElement('div');
    subtitle.className = 'group-subtitle';
    subtitle.textContent = `${item.Followers || '0'} followers`;

    const meta = document.createElement('div');
    meta.className = 'group-meta';

    meta.innerHTML = `
        <span>${item.post_count || 0} posts</span>
        <span>${item.last_updated ? formatDate(item.last_updated) : ''}</span>
    `;

    element.appendChild(title);
    element.appendChild(subtitle);
    element.appendChild(meta);

    element.addEventListener('click', () => loadItem(null, identifier));

    return element;
}

// Load specific item (group or channel)
async function loadItem(authorId, source) {
    try {
        if (currentPlatform === 'messenger') {
            currentItem = `${authorId}:${source}`;
        } else {
            currentItem = source;
        }

        // Update active state
        document.querySelectorAll('.channel-item, .group-item').forEach(item => {
            item.classList.remove('active');
        });

        loadingElement.style.display = 'block';
        messagesContainer.innerHTML = '';
        errorElement.style.display = 'none';

        let response;
        if (currentPlatform === 'messenger') {
            response = await fetch(`${API_MESSAGES}?platform=${currentPlatform}&author_id=${encodeURIComponent(authorId)}&source=${encodeURIComponent(source)}`);
        } else {
            response = await fetch(`${API_MESSAGES}?platform=${currentPlatform}&source=${encodeURIComponent(source)}`);
        }

        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();

        // Update header
        if (currentPlatform === 'messenger') {
            const headerContent = document.querySelector('.header-content');
            // Check if icon exists, if not create it
            let iconElement = document.getElementById('header-icon');
            if (!iconElement) {
                iconElement = document.createElement('img');
                iconElement.id = 'header-icon';
                iconElement.className = 'header-icon';
                headerContent.prepend(iconElement);
            }
            iconElement.src = data.icon || 'https://via.placeholder.com/48';
            iconElement.style.display = 'block';

            titleElement.textContent = data.Title || 'Messages';
            subtitleElement.textContent = data.Sub_Title || '';

            // Setup buttons
            headerActions.style.display = 'flex';

            // Button 1: View Author
            if (data.author_url) {
                btnSource1.style.display = 'flex';
                btnSource1.href = data.author_url;
                btnText1.textContent = 'View Author';
                btnIcon1.innerHTML = ICON_FB;
            } else {
                btnSource1.style.display = 'none';
            }

            // Button 2: View Group
            btnSource2.style.display = 'flex';
            btnSource2.href = data.source;
            btnText2.textContent = 'View Group';
            btnIcon2.innerHTML = ICON_MESSENGER;

            renderMessages(data.messages || []);
        } else {
            const iconElement = document.getElementById('header-icon');
            if (iconElement) iconElement.style.display = 'none';

            titleElement.textContent = data.Source_name || 'Channel';
            subtitleElement.textContent = `${data.Followers || '0'} followers`;

            // Setup buttons
            headerActions.style.display = 'flex';

            // Button 1: View Channel (WhatsApp)
            btnSource1.style.display = 'flex';
            btnSource1.href = data.Source_link || '#';
            btnText1.textContent = 'View Channel';
            btnIcon1.innerHTML = ICON_WHATSAPP;

            // Hide Button 2 for WhatsApp
            btnSource2.style.display = 'none';

            renderPosts(data.posts || []);
        }

        loadingElement.style.display = 'none';
        renderItemsList();

    } catch (error) {
        console.error('Error loading item:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
    }
}

// Render Messenger messages
function renderMessages(messages) {
    messagesContainer.innerHTML = '';

    if (messages.length === 0) {
        messagesContainer.innerHTML = '<div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">No messages</div>';
        return;
    }

    // Sort messages by timestamp descending (newest first)
    // Using string comparison works because format is YYYY-MM-DD HH:MM:SS
    const sortedMessages = messages.slice().sort((a, b) => {
        const timeA = a.timestamp || '';
        const timeB = b.timestamp || '';
        if (timeA === timeB) return 0;
        return timeA < timeB ? 1 : -1;
    });

    sortedMessages.forEach((message, index) => {
        const card = createMessageCard(message, index);
        messagesContainer.appendChild(card);
    });
}

// Render WhatsApp posts
function renderPosts(posts) {
    messagesContainer.innerHTML = '';

    if (posts.length === 0) {
        messagesContainer.innerHTML = '<div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">No posts</div>';
        return;
    }

    // Sort posts by scraping time descending (newest first)
    const sortedPosts = posts.slice().sort((a, b) => {
        const timeA = a.Post_scraping_time || '';
        const timeB = b.Post_scraping_time || '';
        if (timeA === timeB) return 0;
        return timeA < timeB ? 1 : -1;
    });

    sortedPosts.forEach((post, index) => {
        const card = createPostCard(post, index);
        messagesContainer.appendChild(card);
    });
}

// Helper function to convert URLs in text to clickable links
function linkifyText(text) {
    if (!text) return '';

    // Regular expression to match URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g;

    // Escape HTML to prevent XSS attacks
    const escapeHtml = (str) => {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    };

    // Replace URLs with anchor tags
    return escapeHtml(text).replace(urlRegex, (url) => {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="message-link">${url}</a>`;
    });
}

// Create Messenger message card
function createMessageCard(message, index) {
    const card = document.createElement('div');
    card.className = 'message-card';
    card.style.animationDelay = `${index * 0.05}s`;

    // User info
    const userInfo = document.createElement('div');
    userInfo.className = 'user-info';

    const avatar = document.createElement('img');
    avatar.className = 'user-avatar';
    avatar.src = message.user_profile_pic || 'https://via.placeholder.com/50';
    avatar.alt = message.user_name;
    avatar.loading = 'lazy';

    const userDetails = document.createElement('div');
    userDetails.className = 'user-details';

    const userName = document.createElement('div');
    userName.className = 'user-name';
    userName.textContent = message.user_name || 'Unknown User';

    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = formatTimestamp(message.timestamp);

    userDetails.appendChild(userName);
    userDetails.appendChild(timestamp);
    userInfo.appendChild(avatar);
    userInfo.appendChild(userDetails);
    card.appendChild(userInfo);

    // Message text with clickable links
    if (message.text && message.text.trim()) {
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = linkifyText(message.text);
        card.appendChild(messageText);
    }

    // Media
    if (message.media && message.media.length > 0) {
        const mediaGallery = createMediaGallery(message.media);
        if (mediaGallery.children.length > 0) {
            card.appendChild(mediaGallery);
        }
    }

    // Reactions
    if (message.reactions && Object.keys(message.reactions).length > 0) {
        const reactions = createReactions(message.reactions);
        card.appendChild(reactions);
    }

    return card;
}

// Create WhatsApp post card
function createPostCard(post, index) {
    const card = document.createElement('div');
    card.className = 'message-card';
    card.style.animationDelay = `${index * 0.05}s`;

    // Post header (time and reaction count)
    const header = document.createElement('div');
    header.className = 'user-info';
    header.style.marginBottom = '12px';

    const timeDiv = document.createElement('div');
    timeDiv.className = 'user-details';
    timeDiv.style.flex = '1';

    const time = document.createElement('div');
    time.className = 'timestamp';
    time.textContent = post.Post_time || '';
    timeDiv.appendChild(time);

    const reactionDiv = document.createElement('div');
    reactionDiv.style.display = 'flex';
    reactionDiv.style.alignItems = 'center';
    reactionDiv.style.gap = '6px';

    if (post.Post_reaction) {
        const reactionIcon = document.createElement('span');
        reactionIcon.textContent = '❤️';
        reactionIcon.style.fontSize = '1.1rem';

        const reactionCount = document.createElement('span');
        reactionCount.className = 'reaction-count';
        reactionCount.textContent = post.Post_reaction;

        reactionDiv.appendChild(reactionIcon);
        reactionDiv.appendChild(reactionCount);
    }

    header.appendChild(timeDiv);
    header.appendChild(reactionDiv);
    card.appendChild(header);

    // Post text with clickable links
    if (post.Post_text && post.Post_text.trim()) {
        const postText = document.createElement('div');
        postText.className = 'message-text';
        postText.innerHTML = linkifyText(post.Post_text);
        card.appendChild(postText);
    }

    // Post image (with error handling)
    if (post.Post_image) {
        const mediaGallery = document.createElement('div');
        mediaGallery.className = 'media-gallery';

        const img = document.createElement('img');
        img.className = 'media-item';
        img.alt = 'Post image';
        img.loading = 'lazy';

        // Handle image load error
        img.onerror = function () {
            // Replace with placeholder or hide
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'media-item';
            placeholder.style.display = 'flex';
            placeholder.style.alignItems = 'center';
            placeholder.style.justifyContent = 'center';
            placeholder.style.background = 'rgba(124, 77, 255, 0.1)';
            placeholder.style.color = 'var(--text-secondary)';
            placeholder.style.fontSize = '0.9rem';
            placeholder.textContent = '📷 Image not available';
            mediaGallery.appendChild(placeholder);
        };

        // Set image source
        img.src = post.Post_image;

        // Click to open (only if image loads successfully)
        img.addEventListener('click', () => {
            if (img.complete && img.naturalHeight !== 0) {
                window.open(post.Post_image, '_blank');
            }
        });

        mediaGallery.appendChild(img);
        card.appendChild(mediaGallery);
    }

    return card;
}

// Create media gallery
function createMediaGallery(mediaUrls) {
    const gallery = document.createElement('div');
    gallery.className = 'media-gallery';

    const actualMedia = mediaUrls.filter(url =>
        !url.includes('emoji.php') &&
        (url.includes('.jpg') || url.includes('.png') || url.includes('.jpeg') || url.includes('.gif'))
    );

    actualMedia.forEach(url => {
        const img = document.createElement('img');
        img.className = 'media-item';
        img.src = url;
        img.alt = 'Media';
        img.loading = 'lazy';
        img.addEventListener('click', () => window.open(url, '_blank'));
        gallery.appendChild(img);
    });

    return gallery;
}

// Create reactions
function createReactions(reactions) {
    const container = document.createElement('div');
    container.className = 'reactions';

    Object.entries(reactions).forEach(([emoji, count]) => {
        const badge = document.createElement('div');
        badge.className = 'reaction-badge';

        const emojiSpan = document.createElement('span');
        emojiSpan.className = 'reaction-emoji';
        emojiSpan.textContent = emoji;

        const countSpan = document.createElement('span');
        countSpan.className = 'reaction-count';
        countSpan.textContent = count;

        badge.appendChild(emojiSpan);
        badge.appendChild(countSpan);
        container.appendChild(badge);
    });

    return container;
}

// Format timestamp
function formatTimestamp(timestamp) {
    if (!timestamp) return '';

    try {
        const date = new Date(timestamp);
        if (isNaN(date.getTime())) return timestamp;

        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            return 'Today at ' + date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit'
            });
        } else if (diffDays === 1) {
            return 'Yesterday at ' + date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit'
            });
        } else {
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    } catch (error) {
        return timestamp;
    }
}

// Format date for meta
function formatDate(dateStr) {
    if (!dateStr) return '';

    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;

        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / (1000 * 60));
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;

        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } catch (error) {
        return dateStr;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', init);
