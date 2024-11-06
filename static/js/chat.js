let socket = new WebSocket(`${location.origin.replace('http', 'ws')}/chat/ws`);

socket.onmessage = function (event) {
    let message = JSON.parse(event.data);
    let messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += "<p>" + message.user + ": " + message.text + "</p>";
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
};

// 发送消息的函数
function sendMessage() {
    let input = document.getElementById("message-input");
    let message = {
        text: input.value
    };
    if (input.value.trim() !== "") { // 检查输入不为空
        socket.send(JSON.stringify(message));
        input.value = ""; // 清空输入框
    }
}

// 绑定发送按钮点击事件
document.getElementById("send-button").onclick = sendMessage;

// 绑定回车键事件
document.getElementById("message-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") { // 检查是否按下回车
        sendMessage(); // 调用发送消息的函数
        event.preventDefault(); // 防止默认行为（例如换行）
    }
});