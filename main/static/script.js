document.addEventListener('DOMContentLoaded', function () {
    const regexForMentions = /(\B@(\d+)\b)/g;

    for (post of document.getElementsByClassName("post-container")) {
        // Turn mentions into links
        postContent = post.getElementsByClassName("post-content")[0];
        element = postContent.getElementsByTagName("p")[0];
        element.innerHTML = element.innerHTML.replace(
            regexForMentions,
            "<a href=https://anorum.com/mention/$2>$1</a>"
        );

        // Add reply button functionality
        replyButton = post.getElementsByClassName("post-reply")[0];
        if (typeof replyButton !== 'undefined') {
            replyButton.addEventListener('click', _ => replyToPost(post.id));
        }
    }
});

function replyToPost(post_id) {
    replyBox = document.getElementsByTagName("textarea")[0];

    if (
        replyBox.value.length > 0 &&
        /\w/.test(replyBox.value[replyBox.value.length - 1])
    ) {
        replyBox.value += " ";
    }
    replyBox.value += `@${post_id} `;
}
