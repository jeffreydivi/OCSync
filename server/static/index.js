function loadPage(target) {
    const pages = document.querySelectorAll("page")
    for (let i = 0; i < pages.length; i++)
        pages[i].style.display = "none";
    document.getElementById(target).style.display = "block";
}

function toast(msg) {
    let toast = document.createElement("toast");
    toast.innerText = msg;
    toast.onclick = (evt) => {
        evt.target.parentElement.removeChild(evt.target);
    }
    setTimeout((evt) => {
        toast.parentElement.removeChild(toast);
    }, 10000);
    document.querySelector("nav").append(toast);
}

function main() {
    document.querySelector("#login > .center > button").onclick = (evt) => {
        const username = document.querySelector("#login > .center > input[type=text]").value;
        const password = document.querySelector("#login > .center > input[type=password]").value;
        localStorage.setItem("auth", JSON.stringify({
            "username": username,
            "password": password
        }));
        socket.emit("get", {
            "auth": {
                    "username": username,
                    "password": password
                },
            "firstTime": true
        });
    }

    document.querySelector("#newUser > button").onclick = (evt) => {
        const newUsername = document.querySelector("#newUser > input[type=text]").value;
        const newPassword = document.querySelector("#newUser > input[type=password]").value;
        let auth = JSON.parse(localStorage.getItem("auth"))
        socket.emit("newUser", {
            "auth": {
                    "username": auth["username"],
                    "password": auth["password"]
                },
            "username": newUsername,
            "password": newPassword
        });
    }
}

let socket = io();

socket.on("connect", () => {
    console.log("Connected!");
    let data = localStorage.getItem("auth");
    if (data) {
        data = JSON.parse(data);
        socket.emit("get", {
            "auth": {
                    "username": data["username"],
                    "password": data["password"]
                },
            "firstTime": true
        });
    } else {
        loadPage("login");
    }
});

socket.on("response", (data) => {
    console.log(data);
    if (data["error"] === 403) {
        loadPage("login");
        document.querySelector("#login > .center > p#error").innerText = "Error: Invalid credentials!";
    } else if (data["error"] === 401) {
        loadPage("login");
        document.querySelector("#login > .center > p#error").innerText = "Error: Could not authenticate.";
    } else if (data["status"] === "first") {
        // First load of page.
        loadPage("main");
        document.querySelector("nav > h2").innerText = data["user"];
    } else if (data["status"] === "newUser") {
        toast(data["message"])
    }

    if (data["status"] === "first" || data["status"] === "update") {
        document.querySelector("code").innerText = JSON.stringify(data["data"]);
    }
});

main();