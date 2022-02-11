const login_url =  "http://localhost:8000/api/token/";
let form = document.getElementById("login--form");
form.addEventListener('submit', (e) => {
    e.preventDefault();
    let username = form.username.value;
    let password = form.password.value;
    let formData = {
        username,
        password
    }
    fetch(login_url, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if( data.access){
            localStorage.setItem("token", data.access);
            console.log("Login Success");
            window.location = "file:///Users/f.silva/Desktop/devsearch/zfront/projects.html";
        }
    })

});