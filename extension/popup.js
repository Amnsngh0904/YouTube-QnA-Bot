const chatBox = document.getElementById("chatBox");
const questionInput = document.getElementById("questionInput");
const submitBtn = document.getElementById("submit");

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleQuestionSubmit() {
  const question = questionInput.value.trim();
  if (!question) return;

  addMessage(question, "user");
  questionInput.value = "";
  addMessage("Thinking...", "bot");

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const videoUrl = tab.url;

    const formData = new FormData();
    formData.append("video_url", videoUrl);
    formData.append("question", question);

    const res = await fetch("http://localhost:8000/process", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    // Remove last "Thinking..." message
    const thinking = document.querySelector(".bot:last-child");
    if (thinking) thinking.remove();

    addMessage(data.answer, "bot");
  } catch (err) {
    console.error(err);
    addMessage("Failed to get an answer. Is the backend running?", "bot");
  }
}

submitBtn.addEventListener("click", handleQuestionSubmit);

questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    handleQuestionSubmit();
  }
});
