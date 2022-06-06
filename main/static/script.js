function onBodyLoad() {
    // Turn mentions into links
    regexForMentions = /(\B@(\d+)\b)/g;
    for (postContent of document.getElementsByClassName("post-content")) {
        element = postContent.getElementsByTagName("p")[0];
        element.innerHTML = element.innerHTML.replace(
            regexForMentions,
            "<a href=https://anorum.com/mention/$2>$1</a>"
        )
    }
}
