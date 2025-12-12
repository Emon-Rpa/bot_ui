// API endpoints
const API_PLATFORMS = '/api/platforms';
const API_GROUPS = '/api/groups';
const API_MESSAGES = '/api/messages';

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
        sidebarTitle.textContent = 'WhatsApp Channels';
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
            allItems = data.groups || [];
            groupCount.textContent = `${allItems.length} group${allItems.length !== 1 ? 's' : ''}`;
        } else {
            allItems = data.channels || [];
            groupCount.textContent = `${allItems.length} channel${allItems.length !== 1 ? 's' : ''}`;
        }

        renderItemsList();

        // Load first item by default
        if (allItems.length > 0) {
            const identifier = currentPlatform === 'messenger'
                ? allItems[0].Title
                : allItems[0].Source_name;
            loadItem(identifier);
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

    allItems.forEach(item => {
        const itemElement = createItemElement(item);
        groupsList.appendChild(itemElement);
    });
}

// Create item element for sidebar
function createItemElement(item) {
    const element = document.createElement('div');
    element.className = 'group-item';

    const identifier = currentPlatform === 'messenger' ? item.Title : item.Source_name;
    if (currentItem === identifier) {
        element.classList.add('active');
    }

    const title = document.createElement('div');
    title.className = 'group-title';
    title.textContent = identifier || 'Untitled';

    const subtitle = document.createElement('div');
    subtitle.className = 'group-subtitle';

    if (currentPlatform === 'messenger') {
        subtitle.textContent = item.Sub_Title || 'No description';
    } else {
        subtitle.textContent = `${item.Followers || '0'} followers`;
    }

    const meta = document.createElement('div');
    meta.className = 'group-meta';

    const count = currentPlatform === 'messenger' ? item.message_count : item.post_count;
    const label = currentPlatform === 'messenger' ? 'messages' : 'posts';

    meta.innerHTML = `
        <span>${count || 0} ${label}</span>
        <span>${item.last_updated ? formatDate(item.last_updated) : ''}</span>
    `;

    element.appendChild(title);
    element.appendChild(subtitle);
    element.appendChild(meta);

    element.addEventListener('click', () => loadItem(identifier));

    return element;
}

// Load specific item (group or channel)
async function loadItem(identifier) {
    try {
        currentItem = identifier;

        // Update active state
        document.querySelectorAll('.group-item').forEach(item => {
            item.classList.remove('active');
        });

        loadingElement.style.display = 'block';
        messagesContainer.innerHTML = '';
        errorElement.style.display = 'none';

        const param = currentPlatform === 'messenger' ? 'title' : 'source';
        const response = await fetch(`${API_MESSAGES}?platform=${currentPlatform}&${param}=${encodeURIComponent(identifier)}`);

        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();

        // Update header
        if (currentPlatform === 'messenger') {
            titleElement.textContent = data.Title || 'Messages';
            subtitleElement.textContent = data.Sub_Title || '';
            renderMessages(data.messages || []);
        } else {
            titleElement.textContent = data.Source_name || 'Channel';
            subtitleElement.textContent = `${data.Followers || '0'} followers`;
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

    messages.forEach((message, index) => {
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

    posts.forEach((post, index) => {
        const card = createPostCard(post, index);
        messagesContainer.appendChild(card);
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

    // Message text
    if (message.text && message.text.trim()) {
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = message.text;
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

    // Post text
    if (post.Post_text && post.Post_text.trim()) {
        const postText = document.createElement('div');
        postText.className = 'message-text';
        postText.textContent = post.Post_text;
        card.appendChild(postText);
    }

    // Post image
    if (post.Post_image) {
        const mediaGallery = document.createElement('div');
        mediaGallery.className = 'media-gallery';

        const img = document.createElement('img');
        img.className = 'media-item';
        img.src = post.Post_image;
        img.alt = 'Post image';
        img.loading = 'lazy';
        img.addEventListener('click', () => window.open(post.Post_image, '_blank'));

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
