import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { AuthProvider, useAuth } from "./context/AuthContext";
import "./App.css";

type View = "study" | "insights";

function AppShell() {
  const { isAuthenticated, email, logout } = useAuth();
  const [authView, setAuthView] = useState<"login" | "signup">("login");
  const [documentReady, setDocumentReady] = useState(!!localStorage.getItem("edurag_current_doc"));
  const [chatResetKey, setChatResetKey] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState(localStorage.getItem("edurag_current_doc") || "");
  const [view, setView] = useState<View>("study");

  const handleUploadSuccess = (fileName: string) => {
    setDocumentReady(true);
    setUploadedFileName(fileName);
    setChatResetKey((prev) => prev + 1);
    localStorage.setItem("edurag_current_doc", fileName);
  };

  const handleLogout = () => {
    logout();
    setDocumentReady(false);
    setUploadedFileName("");
    setChatResetKey((prev) => prev + 1);
    setView("study");
    localStorage.removeItem("edurag_current_doc");
  };

  if (!isAuthenticated) {
    return authView === "login" ? (
      <Login onSwitchToSignup={() => setAuthView("signup")} />
    ) : (
      <Signup onSwitchToLogin={() => setAuthView("login")} />
    );
  }

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

        <div className="sidebar-user">
          <span className="sidebar-user-email">{email}</span>
          <button onClick={handleLogout} className="sidebar-logout">
            Log out
          </button>
        </div>
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

function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
}

export default App;