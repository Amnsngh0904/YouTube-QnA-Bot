document.getElementById("submit").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const videoUrl = tab.url;
  const question = document.getElementById("question").value;

  const formData = new FormData();
  formData.append("video_url", videoUrl);
  formData.append("question", question);

  const res = await fetch("http://localhost:8000/process", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("answer").innerText = data.answer;
});
