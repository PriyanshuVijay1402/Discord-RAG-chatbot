document.getElementById("askButton").addEventListener("click", async () => {
  const query = document.getElementById("queryInput").value;
  const responseText = document.getElementById("responseText");
  responseText.innerText = "Loading...";

  try {
    const res = await fetch("http://127.0.0.1:8000/api/rag-query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, user_id: "frontend_user" }), // required by backend
    });

    const data = await res.json();
    console.log("Backend Response:", data);

    responseText.innerText = data.answer || "No response.";
  } catch (err) {
    responseText.innerText = "Error: " + err.message;
  }
});
