import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import "./App.css";

function App() {
  const [documentReady, setDocumentReady] = useState(false);
  const [chatResetKey, setChatResetKey] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState("");

 const handleUploadSuccess = (fileName: string) => {
  setDocumentReady(true);
  setUploadedFileName(fileName);
  setChatResetKey((prev) => prev + 1);
};
  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>EduRAG Assistant</h1>
          <p>
            Upload academic PDFs, ask questions, generate summaries, and create quizzes using local RAG.
          </p>
        </header>

        <main className="main-card">
          <FileUpload onUploadSuccess={handleUploadSuccess} />

          <hr className="divider" />

          <ChatBox
  key={chatResetKey}
  documentReady={documentReady}
  uploadedFileName={uploadedFileName}
/>
        </main>
      </div>
    </div>
  );
}

export default App;