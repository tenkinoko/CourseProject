const serverURL = "http://127.0.0.1:5000/";

async function fetchData(input) {
    var posts = getResult(input);
    document.getElementById("posts").innerHTML = posts.data.map(item=>`<li><a href=${item.link} target="_blank">${item.title}</a></li>`).join('');

}

function getResult(keyword) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", serverURL + keyword, true);

    xhr.onreadystatechange = function () {
        console.log(xhr);
        if (xhr.readyState == 4) {
            console.log("here", xhr.responseText);
            callback(xhr.responseText)
        }
    }
    xhr.send();

    // return new Promise(function (resolve, reject) {
    //     xhr.open("GET", serverURL + keyword, true);
    //     xhr.onreadystatechange = function (e) {
    //         // check if XHR transaction is complete
    //         if (xhr.readyState === 4) {
    //             responseText = JSON.parse(xhr.response)
    //             resolve(responseText);
    //         } else {
    //             reject(xhr.statusText);
    //         }
    //     };
    //     xhr.send();
    // });
    
    var results = {data: 
        [{title: "hahaTopics to be covered in Exam 2", link: "https://www.w3schools.com"},
        {title: "Constriant of PLSA",link: "https://www.w3schools.com"}, 
        {title: "Progress Report See Updated Reviews?", link: "https://www.w3schools.com"}]
    };
    return results;
}

function callback(responseText) {
    return responseText
}

document.getElementById("search").onclick = async () => {
    console.log('clicked');
    var input = document.getElementById("keyword").value;
    fetchData(input);
};
