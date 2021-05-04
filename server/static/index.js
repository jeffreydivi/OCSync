function loadPage(target) {
    const pages = document.querySelectorAll("page")
    for (let i = 0; i < pages.length; i++)
        pages[i].style.display = "none";
    document.getElementById(target).style.display = "block";
}

function main() {
    document.querySelector("#login > button").onclick = (evt) => {
        socket.emit("get", {
            "auth": {
                    "username": document.querySelector("#login > input[type=text]").value,
                    "password": document.querySelector("#login > input[type=password]").value
                },
            "firstTime": true
        });
    }
}

let socket = io();

socket.on("connect", () => {
    console.log("Connected!");
    loadPage("login");
});

socket.on("response", (data) => {
    console.log(data);
    if (data["error"] === 403) {
        loadPage("login");
        document.querySelector("#login > p#error").innerText = "Invalid credentials!";
    } else if (data["error"] === 401) {
        document.querySelector("#login > p#error").innerText = "Could not authenticate.";
    } else if (data["status"] === "first") {
        loadPage("main");
    }

    if (data["status"] === "first" || data["status"] === "update") {
        document.querySelector("code").innerText = JSON.stringify(data["data"]);
    }
});

main();