import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import Dashboard from "./components/Dashboard";
import DocumentSelector from "./components/DocumentSelector";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { AuthProvider, useAuth } from "./context/AuthContext";
import "./App.css";

type View = "study" | "insights";

function AppShell() {
  const { isAuthenticated, email, logout } = useAuth();
  const [authView, setAuthView] = useState<"login" | "signup">("login");
  const [documentReady, setDocumentReady] = useState(false);
  const [chatResetKey, setChatResetKey] = useState(0);
  const [docListRefreshKey, setDocListRefreshKey] = useState(0);
  const [selectedDocumentIds, setSelectedDocumentIds] = useState<string[]>([]);
  const [view, setView] = useState<View>("study");

  const handleUploadSuccess = () => {
    setDocListRefreshKey((prev) => prev + 1);
  };

  const handleLogout = () => {
    logout();
    setDocumentReady(false);
    setChatResetKey((prev) => prev + 1);
    setSelectedDocumentIds([]);
    setView("study");
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
          <button className={`nav-item ${view === "study" ? "active" : ""}`} onClick={() => setView("study")}>
            Study
          </button>
          <button className={`nav-item ${view === "insights" ? "active" : ""}`} onClick={() => setView("insights")}>
            Insights
          </button>
        </nav>

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
              <h1>Study your documents.</h1>
              <p>Upload PDFs, then ask questions scoped to one, several, or all of them.</p>
            </header>

            <div className="main-card">
              <FileUpload onUploadSuccess={handleUploadSuccess} />

              <DocumentSelector
                refreshKey={docListRefreshKey}
                selectedIds={selectedDocumentIds}
                onSelectionChange={setSelectedDocumentIds}
                onDocumentsLoaded={setDocumentReady}
              />

              <hr className="divider" />

              <ChatBox
                key={chatResetKey}
                documentReady={documentReady}
                uploadedFileName=""
                selectedDocumentIds={selectedDocumentIds}
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