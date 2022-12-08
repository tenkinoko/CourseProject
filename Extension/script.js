const serverURL = "http://127.0.0.1:5000/";

async function fetchData(input) {
    var posts = getResult(input);
    var linkbase = "https://campuswire.com/c/G984118D3/feed/";
    document.getElementById("posts").innerHTML = posts.data.map(item=>`<li><a href=linkbase + ${item.id} target="_blank">${item.title}</a></li>`).join('');

}

function getResult(keyword) {
    var xhr = new XMLHttpRequest();

    return new Promise(function (resolve, reject) {
        xhr.open("GET", serverURL + keyword, true);
        xhr.onreadystatechange = function (e) {
            if (xhr.readyState === 4) {
                responseText = JSON.parse(xhr.response)
                resolve(responseText);
            } else {
                reject(xhr.statusText);
            }
        };
        xhr.send();
    });
}

document.getElementById("search").onclick = async () => {
    console.log('clicked');
    var input = document.getElementById("keyword").value;
    fetchData(input);
};
