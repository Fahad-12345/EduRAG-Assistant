import { useEffect, useState } from "react";
import API from "../services/api";

interface StatCard {
  label: string;
  value: string;
  unit?: string;
}

interface DocumentRecord {
  filename: string;
  chunks: number;
  uploaded_at: string;
}

function Dashboard() {
  const [stats, setStats] = useState<StatCard[] | null>(null);
  const [documents, setDocuments] = useState<DocumentRecord[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, docsRes] = await Promise.all([
          API.get("/stats"),
          API.get("/documents"),
        ]);
        setStats(statsRes.data.stats);
        setDocuments(docsRes.data.documents);
      } catch {
        setStats(null);
        setDocuments(null);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatDate = (iso: string) => {
    return new Date(iso).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <>
      <header className="page-header">
        <h1>Insights.</h1>
        <p>Your activity in EduRAG.</p>
      </header>

      <div className="main-card">
        {loading ? (
          <p className="empty-text">Loading insights...</p>
        ) : stats ? (
          <div className="stats-grid">
            {stats.map((stat) => (
              <div className="stat-card" key={stat.label}>
                <p className="stat-value">
                  {stat.value}
                  {stat.unit && <span className="stat-unit">{stat.unit}</span>}
                </p>
                <p className="stat-label">{stat.label}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="stats-empty">
            <p>Insights aren't connected yet.</p>
          </div>
        )}
      </div>

      <div className="main-card" style={{ marginTop: 20 }}>
        <h3 className="section-title">Your documents</h3>
        {documents && documents.length > 0 ? (
          <div className="doc-list">
            {documents.map((doc, i) => (
              <div className="doc-list-item" key={i}>
                <span className="doc-list-name">{doc.filename}</span>
                <span className="doc-list-meta">
                  {doc.chunks} chunks · {formatDate(doc.uploaded_at)}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-text">No documents uploaded yet.</p>
        )}
      </div>
    </>
  );
}

export default Dashboard;