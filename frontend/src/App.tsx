import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import Dashboard from "./components/Dashboard";
import "./App.css";

type View = "study" | "insights";

function App() {
  const [documentReady, setDocumentReady] = useState(false);
  const [chatResetKey, setChatResetKey] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [view, setView] = useState<View>("study");

  const handleUploadSuccess = (fileName: string) => {
    setDocumentReady(true);
    setUploadedFileName(fileName);
    setChatResetKey((prev) => prev + 1);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">ER</span>
          <span className="brand-name">EduRAG</span>
        </div>

        <nav className="nav">
          <button
            className={`nav-item ${view === "study" ? "active" : ""}`}
            onClick={() => setView("study")}
          >
            Study
          </button>
          <button
            className={`nav-item ${view === "insights" ? "active" : ""}`}
            onClick={() => setView("insights")}
          >
            Insights
          </button>
        </nav>

        {uploadedFileName && (
          <div className="sidebar-doc">
            <span className="sidebar-doc-label">Current document</span>
            <span className="sidebar-doc-name">{uploadedFileName}</span>
          </div>
        )}
      </aside>

      <main className="content">
        {view === "study" ? (
          <>
            <header className="page-header">
              <h1>Study your document.</h1>
              <p>Upload a PDF, then ask, summarize, quiz, or explain.</p>
            </header>

            <div className="main-card">
              <FileUpload onUploadSuccess={handleUploadSuccess} />
              <hr className="divider" />
              <ChatBox
                key={chatResetKey}
                documentReady={documentReady}
                uploadedFileName={uploadedFileName}
              />
            </div>
          </>
        ) : (
          <Dashboard />
        )}
      </main>
    </div>
  );
}

export default App;