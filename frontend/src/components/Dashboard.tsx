import { useEffect, useState } from "react";
import API from "../services/api";

interface StatCard {
  label: string;
  value: string;
  unit?: string;
}

function Dashboard() {
  const [stats, setStats] = useState<StatCard[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await API.get("/stats");
        setStats(response.data.stats);
      } catch {
        // Backend endpoint not wired yet — fall back to a clear empty state
        setStats(null);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  return (
    <>
      <header className="page-header">
        <h1>Insights.</h1>
        <p>How your document assistant is performing.</p>
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
            <p className="empty-text">
              Wire up a /stats endpoint that pulls latency, eval scores, and usage from Langfuse to see them here.
            </p>
          </div>
        )}
      </div>
    </>
  );
}

export default Dashboard;