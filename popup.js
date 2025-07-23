const RENDER_API_URL = "https://q-a-youtube.onrender.com/api/ask";

document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (tab && tab.url && tab.url.match(/^https:\/\/www\.youtube\.com\/watch\?v=/)) {
      document.getElementById("ask_btn").disabled = false;
      document.getElementById("ask_btn").dataset.videoUrl = tab.url;
    } else {
      document.getElementById("result").textContent = "Please open a YouTube video to use this extension.";
    }
  });

  document.getElementById("ask_btn").addEventListener("click", () => {
    const question = document.getElementById("question").value.trim();
    const videoUrl = document.getElementById("ask_btn").dataset.videoUrl;
    const resultDiv = document.getElementById("result");

    if (!question) {
      resultDiv.textContent = "Please enter a question.";
      return;
    }
    resultDiv.textContent = "Fetching answer...";

    fetch(RENDER_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_url: videoUrl, question: question }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.answer) {
          resultDiv.textContent = data.answer;
        } else {
          resultDiv.textContent = data.error || "No answer received.";
        }
      })
      .catch((err) => {
        resultDiv.textContent = "Error: " + err.message;
      });
  });
});
