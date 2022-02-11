const projects_url = "http://localhost:8000/api/projects";
let loginButton = document.getElementById('login-btn');
let logoutButton = document.getElementById('logout-btn');

if(localStorage.getItem('token')){
    loginButton.remove();
} else {
    logoutButton.remove();
}

logoutButton.addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('token');
    window.location = "file:///Users/f.silva/Desktop/devsearch/zfront/login.html";
})

loginButton.addEventListener('click', (e) => {
    e.preventDefault();
    window.location = "file:///Users/f.silva/Desktop/devsearch/zfront/login.html";
})

let getProjects = () => {
    fetch(projects_url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        buildProjects(data);
    })
}

let buildProjects = (projects) => {
    projects_section = document.getElementById("projects--wrapper");
    projects_section.innerHTML = '';
    for(i=0; i<projects.length; i++){
        project = projects[i]

        projects_section.innerHTML += `
        <div class="project--card">
        <img src="http://127.0.0.1:8000${project.featured_image}" />
        
        <div>
            <div class="card--header">
                <h3>${project.title}</h3>
                <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong>
                <strong class="vote--option" data-vote="down" data-project="${project.id}"  >&#8722;</strong>
            </div>
            <i>${project.vote_ratio}% Positive feedback </i>
            <p>${project.description.substring(0, 150)}</p>
        </div>
    
    </div>
        `
    }
    addVoteEvents();
}

let addVoteEvents = () => {
    let token = localStorage.getItem('token');
    voteBtns = document.getElementsByClassName("vote--option");
    for(i=0; i<voteBtns.length; i++){
        voteBtn = voteBtns[i];
        voteBtn.addEventListener('click', (e) => {
            vote = e.target.dataset.vote;
            project = e.target.dataset.project;

            fetch(projects_url + `/${project}/vote/`, {
                method: "POST",
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
                body: JSON.stringify({ 'value': vote })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);

            })
        })
    }
}

getProjects()