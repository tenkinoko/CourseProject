async function fetchData(input) {
    var posts = getResult(input);
    document.getElementById("posts").innerHTML = posts.data.map(item=>`<li><a href=${item.link} target="_blank">${item.title}</a></li>`).join('');

}

function getResult(keyword) {
    var results = {data: 
        [{title: "hahaTopics to be covered in Exam 2", link: "https://www.w3schools.com"},
        {title: "Constriant of PLSA",link: "https://www.w3schools.com"}, 
        {title: "Progress Report See Updated Reviews?", link: "https://www.w3schools.com"}]
    };
    return results;
}

document.getElementById("search").onclick = async () => {
    console.log('clicked');
    var input = document.getElementById("keyword");
    fetchData(input);
};
