
let searchForm = document.getElementById('searchForm');
let pageLinks = document.getElementsByClassName('page-link');

if (searchForm){
    for(i=0; i<pageLinks.length; i++){
        pageLinks[i].addEventListener('click', function(e){
            e.preventDefault();
            let page = this.dataset.page;
            
            searchForm.innerHTML += `<input hidden value="${page}" name="page" />`

            searchForm.submit();
        })
    }
}


let projectTags = document.getElementsByClassName("project--tags");

for(i=0; i<projectTags.length; i++){
    projectTag = projectTags[i];
    projectTag.addEventListener('click', e => {
        e.preventDefault();
        let tag = e.target.dataset.tag;
        let project = e.target.dataset.project;

        let formData = { tag, project }
        fetch("http://localhost:8000/api/projects/tags/remove/", {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        }).then(response => response.json())
        .then(data => { 
            e.target.remove();
            console.log("Tag successfully removed")
        })
    })
}