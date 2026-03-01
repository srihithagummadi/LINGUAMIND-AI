async function summarize() {
  const text = document.getElementById("text").value;
  const language = document.getElementById("language").value;

  const response = await fetch("http://127.0.0.1:5000/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language })
  });

  const data = await response.json();
  document.getElementById("result").innerText = data.summary;
}