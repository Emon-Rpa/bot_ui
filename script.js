// API endpoints
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

// State
let currentGroup = null;
let allGroups = [];

// Initialize app
async function init() {
    await loadGroups();
}

// Load all groups
async function loadGroups() {
    try {
        const response = await fetch(API_GROUPS);

        if (!response.ok) {
            throw new Error('Failed to fetch groups');
        }

        const data = await response.json();
        allGroups = data.groups || [];

        // Update group count
        groupCount.textContent = `${allGroups.length} group${allGroups.length !== 1 ? 's' : ''}`;

        // Render groups list
        renderGroupsList();

        // Load first group by default if available
        if (allGroups.length > 0) {
            loadGroup(allGroups[0].Title);
        } else {
            loadingElement.style.display = 'none';
        }

    } catch (error) {
        console.error('Error loading groups:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
        errorElement.querySelector('p').textContent = 'Failed to load groups. Please try again.';
    }
}

// Render groups list in sidebar
function renderGroupsList() {
    groupsList.innerHTML = '';

    if (allGroups.length === 0) {
        groupsList.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-secondary);">No groups yet</div>';
        return;
    }

    allGroups.forEach(group => {
        const groupItem = createGroupItem(group);
        groupsList.appendChild(groupItem);
    });
}

// Create a group item element
function createGroupItem(group) {
    const item = document.createElement('div');
    item.className = 'group-item';
    if (currentGroup === group.Title) {
        item.classList.add('active');
    }

    const title = document.createElement('div');
    title.className = 'group-title';
    title.textContent = group.Title || 'Untitled';

    const subtitle = document.createElement('div');
    subtitle.className = 'group-subtitle';
    subtitle.textContent = group.Sub_Title || 'No description';

    const meta = document.createElement('div');
    meta.className = 'group-meta';
    meta.innerHTML = `
        <span>${group.message_count || 0} messages</span>
        <span>${group.last_updated ? formatDate(group.last_updated) : ''}</span>
    `;

    item.appendChild(title);
    item.appendChild(subtitle);
    item.appendChild(meta);

    // Click handler
    item.addEventListener('click', () => {
        loadGroup(group.Title);
    });

    return item;
}

// Load a specific group
async function loadGroup(title) {
    try {
        currentGroup = title;

        // Update active state in sidebar
        document.querySelectorAll('.group-item').forEach(item => {
            item.classList.remove('active');
        });

        // Show loading
        loadingElement.style.display = 'block';
        messagesContainer.innerHTML = '';
        errorElement.style.display = 'none';

        const response = await fetch(`${API_MESSAGES}?title=${encodeURIComponent(title)}`);

        if (!response.ok) {
            throw new Error('Failed to fetch messages');
        }

        const data = await response.json();

        // Update header
        titleElement.textContent = data.Title || 'Messages';
        subtitleElement.textContent = data.Sub_Title || '';

        // Hide loading
        loadingElement.style.display = 'none';

        // Render messages
        renderMessages(data.messages || []);

        // Update active group in sidebar
        renderGroupsList();

    } catch (error) {
        console.error('Error loading group:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
        errorElement.querySelector('p').textContent = 'Failed to load messages. Please try again.';
    }
}

// Render all messages
function renderMessages(messages) {
    messagesContainer.innerHTML = '';

    if (messages.length === 0) {
        messagesContainer.innerHTML = '<div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">No messages in this group</div>';
        return;
    }

    messages.forEach((message, index) => {
        const messageCard = createMessageCard(message, index);
        messagesContainer.appendChild(messageCard);
    });
}

// Create a message card element
function createMessageCard(message, index) {
    const card = document.createElement('div');
    card.className = 'message-card';
    card.style.animationDelay = `${index * 0.05}s`;

    // User info section
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

    // Media gallery
    if (message.media && message.media.length > 0) {
        const mediaGallery = createMediaGallery(message.media);
        card.appendChild(mediaGallery);
    }

    // Reactions
    if (message.reactions && Object.keys(message.reactions).length > 0) {
        const reactions = createReactions(message.reactions);
        card.appendChild(reactions);
    }

    return card;
}

// Create media gallery
function createMediaGallery(mediaUrls) {
    const gallery = document.createElement('div');
    gallery.className = 'media-gallery';

    // Filter out emoji URLs (they're very small and not actual media)
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

        // Open image in new tab on click
        img.addEventListener('click', () => {
            window.open(url, '_blank');
        });

        gallery.appendChild(img);
    });

    return gallery;
}

// Create reactions section
function createReactions(reactions) {
    const reactionsContainer = document.createElement('div');
    reactionsContainer.className = 'reactions';

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
        reactionsContainer.appendChild(badge);
    });

    return reactionsContainer;
}

// Format timestamp to readable format
function formatTimestamp(timestamp) {
    if (!timestamp) return '';

    try {
        const date = new Date(timestamp);

        // Check if date is valid
        if (isNaN(date.getTime())) {
            return timestamp;
        }

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

// Format date for group meta
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

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
