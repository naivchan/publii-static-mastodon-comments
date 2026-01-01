async function loadMastodonComments(mId) {
    const container = document.getElementById('mastodon-comments-list');
    const badge = document.getElementById('comment-count-badge');
    
    if (!mId || !container) return;

	const jsonPath = `/media/files/comments/${mId}.json`;

    try {
        console.log("Fetching from:", jsonPath);
        const response = await fetch(jsonPath);
        
        if (!response.ok) throw new Error(`File not found: ${response.status}`);
        
        const data = await response.json();
        container.innerHTML = ''; 

        const replies = data.descendants || [];

        if (badge) {
            badge.innerText = `${replies.length} Comments`;
            badge.style.display = 'inline-block';
        }

        if (replies.length === 0) {
            container.innerHTML = '<p>No comments yet.</p>';
            return;
        }

      // 1. Create a map of all comments for easy lookup
const commentMap = {};
replies.forEach(reply => {
    commentMap[reply.id] = { ...reply, children: [] };
});

const threadedComments = [];
replies.forEach(reply => {
    // If the reply is to a comment we have in our list, add it as a child
    if (reply.in_reply_to_id && commentMap[reply.in_reply_to_id]) {
        commentMap[reply.in_reply_to_id].children.push(commentMap[reply.id]);
    } else {
        // Otherwise, it's a top-level comment
        threadedComments.push(commentMap[reply.id]);
    }
});

// 2. Function to render comments recursively
function render(comment, depth = 0) {
    // 1. Create the date, year, and time string
    const commentDate = new Date(comment.created_at).toLocaleString(undefined, {
        month: 'short', 
        day: 'numeric', 
        year: 'numeric', // Added year back
        hour: '2-digit',
        minute: '2-digit'
    });

    const indent = depth > 0 ? `masto-indent-${Math.min(depth, 3)}` : '';
    
    // 2. Build the HTML
    let html = `
        <div class="masto-comment ${indent}">
            <div class="masto-comment-header">
                <img src="${comment.account.avatar}" referrerpolicy="no-referrer" class="masto-avatar">
                <div class="masto-meta">
                    <span class="masto-author">${comment.account.display_name}</span>
                    <span class="masto-handle">@${comment.account.acct} • <span class="masto-date">${commentDate}</span></span>
                </div>
            </div>
            <div class="masto-content">${comment.content}</div>
        </div>`;
    
    if (comment.children && comment.children.length > 0) {
        comment.children.forEach(child => html += render(child, depth + 1));
    }
    return html;
}

// 3. Clear container and start rendering
container.innerHTML = '';
threadedComments.forEach(comment => {
    container.insertAdjacentHTML('beforeend', renderComment(comment));
});
    } catch (err) {
        console.error("Mastodon Load Error:", err);
        container.innerHTML = '<p>Comments available on Mastodon.</p>';
    }
}