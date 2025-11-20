import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [rule1, setRule1] = useState("");
  const [rule2, setRule2] = useState("");
  const [rule3, setRule3] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const backendURL = "http://127.0.0.1:8000/check-rules";

  async function checkDocument() {
    if (!file) return setError("Please upload a PDF.");
    if (!rule1 || !rule2 || !rule3)
      return setError("Please enter all 3 rules.");

    setLoading(true);
    setError("");
    setResults([]);

    const form = new FormData();
    form.append("file", file);
    form.append("rule1", rule1);
    form.append("rule2", rule2);
    form.append("rule3", rule3);

    try {
      const res = await fetch(backendURL, {
        method: "POST",
        body: form,
      });

      const data = await res.json();

      let parsed;
      try {
        parsed = JSON.parse(data.results);
      } catch (e) {
        return setError("AI returned invalid JSON. Try again.");
      }

      setResults(parsed);
    } catch (err) {
      setError("Request failed: " + err);
    }

    setLoading(false);
  }

  return (
    <div style={{ padding: 30, fontFamily: "Arial" }}>
      <h1>PDF Rule Checker</h1>

      <h3>1) Upload PDF</h3>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br />

      <h3>2) Enter 3 Rules</h3>
      <input
        type="text"
        placeholder="Rule 1"
        value={rule1}
        onChange={(e) => setRule1(e.target.value)}
        style={{ width: "300px", marginBottom: 8 }}
      />
      <br />
      <input
        type="text"
        placeholder="Rule 2"
        value={rule2}
        onChange={(e) => setRule2(e.target.value)}
        style={{ width: "300px", marginBottom: 8 }}
      />
      <br />
      <input
        type="text"
        placeholder="Rule 3"
        value={rule3}
        onChange={(e) => setRule3(e.target.value)}
        style={{ width: "300px", marginBottom: 8 }}
      />
      <br />

      <button onClick={checkDocument} disabled={loading}>
        {loading ? "Checking..." : "Check Document"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 20 }}>
          <b>Error:</b> {error}
        </p>
      )}

      {results.length > 0 && (
        <>
          <h3 style={{ marginTop: 30 }}>Results</h3>
          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Rule</th>
                <th>Status</th>
                <th>Evidence</th>
                <th>Reasoning</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{r.rule}</td>
                  <td
                    style={{
                      color: r.status === "pass" ? "green" : "red",
                      fontWeight: "bold",
                    }}
                  >
                    {r.status}
                  </td>
                  <td>{r.evidence}</td>
                  <td>{r.reasoning}</td>
                  <td>{r.confidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
