let socket = io();

socket.on("connect", () => {
    console.log("Connected!");
    socket.emit("get", {});
});

socket.on("response", (data) => {
    console.log(data);
});