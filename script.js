async function generateText() {
  const input = document.getElementById('inputText').value;
  const output = document.getElementById('output');
  output.textContent = 'Generating...';

  try {
    const response = await fetch("http://127.0.0.1:5000/generate", { 
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ input })
    });

    const data = await response.json();

    if (data.error) {
      output.textContent = "❌ Error: " + data.error;
    } else {
      output.textContent = data[0]?.generated_text || "No output.";
    }
  } catch (err) {
    console.error(err);
    output.textContent = "❌ Server Error.";
  }
}
