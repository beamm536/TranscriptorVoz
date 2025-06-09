import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("auto");
  const [transcription, setTranscription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Sube un archivo de audio");

    const formData = new FormData();
    formData.append("audio", file);
    formData.append("language", language);

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000", {
        method: "POST",
        body: formData,
      });

      const text = await response.text(); // Flask devuelve HTML, no JSON
      const match = text.match(/<pre>([\s\S]*?)<\/pre>/);
      const extracted = match ? match[1] : "No se pudo extraer la transcripción";

      setTranscription(extracted);
    } catch (err) {
      setTranscription("Error al transcribir.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Transcriptor de Voz</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="es">Español</option>
          <option value="en">Inglés</option>
          <option value="fr">Francés</option>
          <option value="pt">Portugués</option>
          <option value="auto">Detectar automáticamente</option>
        </select>
        <button type="submit" disabled={loading}>
          {loading ? "Transcribiendo..." : "Transcribir"}
        </button>
      </form>

      {transcription && (
        <div className="result">
          <h2>Transcripción</h2>
          <pre>{transcription}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
