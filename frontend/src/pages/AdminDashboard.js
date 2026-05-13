import { useEffect, useState } from "react";
import api from "../services/api";

function AdminDashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      const response = await api.get("/dashboard/institution-summary/");
      setSummary(response.data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Institution dashboard could not be loaded.");
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const approveVehicle = async (id) => {
    await api.post(`/vehicles/${id}/approve/`);
    await loadDashboard();
  };

  const rejectVehicle = async (id) => {
    await api.post(`/vehicles/${id}/reject/`, {
      notes: "Rejected from institution dashboard.",
    });
    await loadDashboard();
  };

  if (error) {
    return <div style={styles.loading}>{error}</div>;
  }

  if (!summary) {
    return <div style={styles.loading}>Loading institution dashboard...</div>;
  }

  return (
    <div style={styles.page}>
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>DPSHTRR Panel</h2>
        <p style={styles.navItem}>Dashboard</p>
        <p style={styles.navItem}>Approvals</p>
        <p style={styles.navItem}>Vehicle Registry</p>
        <p style={styles.navItem}>Payments</p>
        <p style={styles.navItem}>Documents</p>
      </aside>

      <main style={styles.main}>
        <header style={styles.header}>
          <div>
            <h1 style={styles.title}>Institution Dashboard</h1>
            <p style={styles.subtitle}>
              Review vehicle registrations and manage institutional workflows.
            </p>
          </div>

          <button style={styles.refreshButton} onClick={loadDashboard}>
            Refresh
          </button>
        </header>

        <section style={styles.grid}>
          <Card title="Total Vehicles" value={summary.total_vehicles} />
          <Card title="Pending Approvals" value={summary.pending_approvals} />
          <Card title="Active Vehicles" value={summary.active_vehicles} />
          <Card title="Blocked Vehicles" value={summary.blocked_vehicles} />
        </section>

        <Panel title="Pending Vehicle Approvals">
          {!summary.pending_list || summary.pending_list.length === 0 ? (
            <p style={styles.empty}>No pending vehicle approvals.</p>
          ) : (
            summary.pending_list.map((vehicle) => (
              <div key={vehicle.id} style={styles.approvalRow}>
                <div>
                  <h3 style={styles.rowTitle}>{vehicle.plate_number}</h3>
                  <p style={styles.rowText}>
                    {vehicle.year} {vehicle.make} {vehicle.model}
                  </p>
                  <p style={styles.rowSmall}>Owner: {vehicle.owner}</p>
                  <p style={styles.rowSmall}>Status: {vehicle.status}</p>
                </div>

                <div style={styles.actions}>
                  <button
                    style={styles.approveButton}
                    onClick={() => approveVehicle(vehicle.id)}
                  >
                    Approve
                  </button>

                  <button
                    style={styles.rejectButton}
                    onClick={() => rejectVehicle(vehicle.id)}
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))
          )}
        </Panel>
      </main>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={styles.card}>
      <p style={styles.cardTitle}>{title}</p>
      <h2 style={styles.cardValue}>{value ?? 0}</h2>
    </div>
  );
}

function Panel({ title, children }) {
  return (
    <section style={styles.panel}>
      <h2 style={styles.panelTitle}>{title}</h2>
      {children}
    </section>
  );
}

const styles = {
  loading: {
    padding: 30,
    fontFamily: "Arial, sans-serif",
  },
  page: {
    display: "flex",
    minHeight: "100vh",
    background: "#f4f7fb",
    color: "#0f172a",
    fontFamily: "Arial, sans-serif",
  },
  sidebar: {
    width: 270,
    background: "#111827",
    color: "white",
    padding: 28,
  },
  logo: {
    marginBottom: 34,
  },
  navItem: {
    margin: "18px 0",
    fontWeight: 600,
    cursor: "pointer",
  },
  main: {
    flex: 1,
    padding: 32,
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 28,
  },
  title: {
    fontSize: 34,
    margin: 0,
  },
  subtitle: {
    color: "#64748b",
  },
  refreshButton: {
    background: "#2563eb",
    color: "white",
    border: "none",
    padding: "12px 18px",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: 700,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: 20,
    marginBottom: 24,
  },
  card: {
    background: "white",
    padding: 24,
    borderRadius: 16,
    boxShadow: "0 4px 14px rgba(0,0,0,0.08)",
  },
  cardTitle: {
    color: "#475569",
    margin: 0,
  },
  cardValue: {
    fontSize: 32,
    marginTop: 12,
  },
  panel: {
    background: "white",
    padding: 24,
    borderRadius: 16,
    boxShadow: "0 4px 14px rgba(0,0,0,0.07)",
    marginTop: 24,
  },
  panelTitle: {
    marginTop: 0,
    marginBottom: 18,
  },
  empty: {
    color: "#64748b",
  },
  approvalRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    marginBottom: 14,
    background: "#ffffff",
  },
  rowTitle: {
    margin: 0,
    fontSize: 18,
  },
  rowText: {
    margin: "6px 0",
    color: "#475569",
  },
  rowSmall: {
    margin: "4px 0",
    color: "#64748b",
    fontSize: 13,
  },
  actions: {
    display: "flex",
    gap: 10,
  },
  approveButton: {
    background: "#16a34a",
    color: "white",
    border: "none",
    padding: "10px 14px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 700,
  },
  rejectButton: {
    background: "white",
    color: "#dc2626",
    border: "1px solid #dc2626",
    padding: "10px 14px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 700,
  },
};

export default AdminDashboard;