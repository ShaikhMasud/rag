import { spawn } from "child_process";

function askRAG(question) {
  return new Promise((resolve, reject) => {
    const py = spawn("python", ["query.py", question]);

    let output = "";
    let error = "";

    py.stdout.on("data", (data) => {
      output += data.toString();
    });

    py.stderr.on("data", (data) => {
      error += data.toString();
    });

    py.on("close", (code) => {
      if (code !== 0 || error) {
        reject(error);
      } else {
        resolve(JSON.parse(output));
      }
    });
  });
}

// Example usage
askRAG("fuzzy control system example")
  .then(res => {
    console.log("Answer from Python RAG:\n");
    console.log(res.answer);
  })
  .catch(err => {
    console.error("Error:", err);
  });