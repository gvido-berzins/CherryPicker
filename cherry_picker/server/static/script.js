let results = document.getElementById("results")

document.addEventListener('keyup', query);

function postData(url = '', data = {}) {
    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(function(response) {
        return response.text().then(function(text) {
            results.innerHTML = ""
            results.innerHTML = text
        })
    })
}


function query(e) {
    let searchText = document.getElementById("search").value
    // console.log(`Querying: ${searchText}`)
    if (searchText.trim() != "") {
        postData("/query", {
            search: searchText
        })
    }
}

$(document).ready(function() {
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });
});
