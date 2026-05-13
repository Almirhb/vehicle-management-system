import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function UserDashboard() {
  const [summary, setSummary] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [vehicleOverview, setVehicleOverview] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [payments, setPayments] = useState([]);

  const navigate = useNavigate();

  const formatDate = (date) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString("sq-AL");
  };
 








const downloadReceipt = async (paymentId) => {
  try {
    const response = await api.get(`/payments/${paymentId}/receipt/`, {
      responseType: "blob",
    });

    const fileURL = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");

    link.href = fileURL;
    link.setAttribute("download", `receipt_${paymentId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(fileURL);
  } catch (err) {
    console.error(err);
    alert("Fatura nuk mund te shkarkohet.");
  }
};








  const statusColor = (status) => {
    if (status === "paid") return "#16a34a";
    if (status === "overdue") return "#dc2626";
    if (status === "pending") return "#f59e0b";
    return "#64748b";
  };

  const loadDashboard = async () => {
    const summaryRes = await api.get("/dashboard/user-summary/");
    setSummary(summaryRes.data);
  
  const payObligation = async (id) => {
    try {
      await api.post(`/obligations/${id}/pay/`, {
        method: "card",
        provider_reference: "FRONTEND-MOCK-PAYMENT",
      });

    await loadDashboard();
  } catch (err) {
    console.error(err);
  }
};

    const vehiclesRes = await api.get("/dashboard/user-vehicles/");
    setVehicles(vehiclesRes.data);

    const overviewRes = await api.get("/dashboard/user-vehicle-overview/");
    setVehicleOverview(overviewRes.data);

    const notificationsRes = await api.get("/dashboard/user-notifications/");
    setNotifications(notificationsRes.data);

    const paymentsRes = await api.get("/dashboard/user-payments/");
    setPayments(paymentsRes.data);
  };

  const payObligation = async (id) => {
    await api.post(`/obligations/${id}/pay/`, {
      method: "card",
      provider_reference: "MOCK-CARD-PAYMENT",
    });

    await loadDashboard();
  };

  useEffect(() => {
    loadDashboard().catch((err) => console.error(err));
  }, []);

  if (!summary) {
    return <div style={{ padding: 30 }}>Loading dashboard...</div>;
  }

  return (
    <div style={styles.page}>
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>VehicleMS</h2>
        <p style={styles.navItem}>Dashboard</p>
        <p style={styles.navItem}>My Vehicles</p>
        <p style={styles.navItem}>Payments</p>
        <p style={styles.navItem}>Notifications</p>
        <p style={styles.navItem}>Documents</p>
      </aside>

      <main style={styles.main}>
        <header style={styles.header}>
          <div>
            <h1 style={styles.title}>Welcome back</h1>
            <p style={styles.subtitle}>Manage your vehicles, payments, and obligations.</p>
          </div>

          <button
            style={styles.primaryButton}
            onClick={() => navigate("/citizen/register-vehicle")}
          >
            Add Vehicle
          </button>
        </header>

        <section style={styles.grid}>
          <Card title="Total Vehicles" value={summary.total_vehicles} />
          <Card title="Active Vehicles" value={summary.active_vehicles} />
          <Card title="Pending Transfers" value={summary.pending_transfers} />
          <Card title="Unpaid Obligations" value={`$${summary.unpaid_obligations}`} />
        </section>

        <section style={styles.contentGrid}>
          <div>
            <Panel title="My Vehicles">
              {vehicles.length === 0 ? (
                <Empty text="No vehicles found." />
              ) : (
                vehicles.map((v) => (
                  <div key={v.id} style={styles.vehicleRow}>
                    <div>
                      <h3 style={styles.rowTitle}>{v.plate_number}</h3>
                      <p style={styles.rowText}>
                        {v.year} {v.make} {v.model}
                      </p>
                      <p style={styles.rowSmall}>
                        Siguracion: {formatDate(v.insurance_expiry)} · Kolaudim: {formatDate(v.inspection_expiry)}
                      </p>
                    </div>

                    <span style={badgeStyle(v.status)}>{v.status}</span>




<div style={{ display: "flex", gap: 10 }}>
  <span style={badgeStyle(v.status)}>{v.status}</span>

  {(v.status === "draft" || v.status === "rejected") && (
    <button
      style={styles.deleteButton}
      onClick={async () => {
        try {
          await api.delete(`/vehicles/${v.id}/`);
          window.location.reload();
        } catch (err) {
          console.error(err);
        }
      }}
    >
      Delete
    </button>
  )}
</div>


                  </div>


                ))
              )}
            </Panel>

            <Panel title="Afatet dhe detyrimet sipas mjeteve">
  {vehicleOverview.length === 0 ? (
    <Empty text="Nuk ka mjete aktive." />
  ) : (
    vehicleOverview.map((vehicle) => (
      <div key={vehicle.id} style={styles.vehicleOverviewCard}>
        <div style={styles.vehicleOverviewHeader}>
          <div>
            <h3 style={styles.vehiclePlate}>
              {vehicle.plate_number}
            </h3>

            <p style={styles.vehicleInfo}>
              {vehicle.year} {vehicle.make} {vehicle.model}
            </p>
          </div>

          <span style={badgeStyle(vehicle.status)}>
            {vehicle.status}
          </span>
        </div>

        <div style={styles.expiryGrid}>
          <div style={styles.expiryItem}>
            <strong>Leje qarkullimi</strong>
            <p>
              {formatDate(vehicle.circulation_permit_expiry)}
            </p>
          </div>

          <div style={styles.expiryItem}>
            <strong>Taksa</strong>
            <p>
              {formatDate(vehicle.road_tax_expiry)}
            </p>
          </div>

          <div style={styles.expiryItem}>
            <strong>Kolaudim</strong>
            <p>
              {formatDate(vehicle.inspection_expiry)}
            </p>
          </div>

          <div style={styles.expiryItem}>
            <strong>Siguracion</strong>
            <p>
              {formatDate(vehicle.insurance_expiry)}
            </p>
          </div>
        </div>

        <div style={{ marginTop: 20 }}>
          <h4 style={{ marginBottom: 12 }}>
            Detyrimet
          </h4>

          {vehicle.obligations.length === 0 ? (
            <p style={styles.empty}>
              Nuk ka detyrime.
            </p>
          ) : (
            vehicle.obligations.map((o) => (
              <div
                key={o.id}
                style={styles.obligationRow}
              >
                <div>
                  <p style={styles.obligationTitle}>
                    {o.title}
                  </p>

                  <p
                    style={{
                      color: statusColor(o.status),
                      fontWeight: 700,
                    }}
                  >
                    {o.status}
                  </p>

                  <p style={styles.rowSmall}>
                    Skadon më:{" "}
                    {formatDate(o.due_date)}
                  </p>
                </div>

                <div style={styles.obligationActions}>
                <strong>${o.amount}</strong>

                {o.status !== "paid" && (
               <button
               style={styles.payButton}
               onClick={() => payObligation(o.id)}
               >
               Paguaj
             </button>
             )}
             </div>
              </div>
            ))
          )}
        </div>
      </div>
    ))
  )}
</Panel>
          </div>

          <div>
            <Panel title="Notifications">
              {notifications.length === 0 ? (
                <Empty text="No notifications." />
              ) : (
                notifications.slice(0, 5).map((n) => (
  <div key={n.id} style={styles.notificationRow}>
    <div>
      <h3 style={styles.rowTitle}>{n.title}</h3>
      <p style={styles.rowText}>{n.message}</p>
      <p style={styles.rowSmall}>
        {n.is_read ? "Lexuar" : "Pa lexuar"}
      </p>
    </div>

    {!n.is_read && (
      <button
        style={styles.smallButton}
        onClick={() => markNotificationRead(n.id)}
      >
        Mark as read
      </button>
    )}
  </div>
))
              )}
            </Panel>

            <Panel title="Payment History">
              {payments.length === 0 ? (
                <Empty text="No payments found." />
              ) : (

                payments.slice(0, 5).map((p) => (
                   <div key={p.id} style={styles.paymentCard}>
                  <div>
                  <h3 style={styles.rowTitle}>
                  {p.vehicle_plate}
                 </h3>

                 <p style={styles.rowText}>
                 {p.obligation_title}
                </p>

                <p style={styles.rowSmall}>
                 Ref: {p.transaction_reference}
                  </p>

                <p style={styles.rowSmall}>
                 {p.method}
              </p>
                 </div>

                 <div style={{ textAlign: "right" }}>
                   <strong>${p.amount}</strong>

                     <p
                    style={{
          color:
            p.status === "successful"
              ? "#16a34a"
              : "#dc2626",
          fontWeight: 700,
          marginTop: 8,
        }}
      >
        {p.status}
      </p>


      <button
  style={styles.receiptButton}
  onClick={() => downloadReceipt(p.id)}
>
  Shkarko faturën
</button>
    </div>
  </div>
))
              )}
            </Panel>

            <Panel title="Quick Actions">
              <button
                style={styles.actionButton}
                onClick={() => navigate("/citizen/register-vehicle")}
              >
                Register New Vehicle
              </button>

              <button style={styles.actionButton}>Make Payment</button>
              <button style={styles.actionButton}>Transfer Ownership</button>
            </Panel>
          </div>
        </section>
      </main>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={styles.card}>
      <p style={styles.cardTitle}>{title}</p>
      <h2 style={styles.cardValue}>{value}</h2>
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

function Empty({ text }) {
  return <p style={styles.empty}>{text}</p>;
}

function badgeStyle(status) {
  const base = {
    padding: "6px 10px",
    borderRadius: 20,
    fontSize: 13,
    fontWeight: 600,
    textTransform: "capitalize",
  };

  if (status === "active") {
    return { ...base, background: "#dcfce7", color: "#15803d" };
  }

  if (status === "pending_approval") {
    return { ...base, background: "#e0e7ff", color: "#3730a3" };
  }

  if (status === "draft") {
    return { ...base, background: "#e5e7eb", color: "#374151" };
  }

  if (status === "pending_transfer") {
    return { ...base, background: "#ffedd5", color: "#c2410c" };
  }

  if (status === "blocked") {
    return { ...base, background: "#fee2e2", color: "#b91c1c" };
  }

  return { ...base, background: "#e5e7eb", color: "#374151" };
}

const styles = {
  page: {
    display: "flex",
    minHeight: "100vh",
    background: "#f4f7fb",
    color: "#0f172a",
    fontFamily: "Arial, sans-serif",
  },
  sidebar: {
    width: 260,
    background: "#0f172a",
    color: "white",
    padding: 28,
  },
  logo: {
    marginBottom: 32,
  },
  navItem: {
    margin: "18px 0",
    cursor: "pointer",
    fontWeight: 600,
  },
  main: {
    flex: 1,
    padding: 32,
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: {
    fontSize: 34,
    margin: 0,
  },
  subtitle: {
    color: "#64748b",
  },
  primaryButton: {
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
    marginTop: 28,
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
  contentGrid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: 24,
    marginTop: 28,
  },
  panel: {
    background: "white",
    padding: 24,
    borderRadius: 16,
    boxShadow: "0 4px 14px rgba(0,0,0,0.07)",
    marginBottom: 24,
  },
  panelTitle: {
    marginTop: 0,
    marginBottom: 18,
  },
  vehicleRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    marginBottom: 14,
  },
  notificationRow: {
    padding: 14,
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    marginBottom: 12,
  },
  paymentRow: {
    display: "flex",
    justifyContent: "space-between",
    padding: "12px 0",
    borderBottom: "1px solid #e5e7eb",
  },
  activityRow: {
    display: "flex",
    justifyContent: "space-between",
    padding: "14px 0",
    borderBottom: "1px solid #e5e7eb",
  },
  rowTitle: {
    margin: 0,
    fontSize: 16,
  },
  rowText: {
    margin: "6px 0",
    color: "#475569",
  },
  rowSmall: {
    margin: 0,
    color: "#64748b",
    fontSize: 13,
  },
  statusText: {
    margin: "6px 0",
    fontWeight: 700,
    textTransform: "capitalize",
  },
  expiryDate: {
    fontSize: 14,
    color: "#475569",
    marginTop: 4,
  },
  actionButton: {
    width: "100%",
    padding: 12,
    marginBottom: 10,
    border: "1px solid #2563eb",
    background: "white",
    color: "#2563eb",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: 700,
  },
  empty: {
    color: "#64748b",
  },
  smallButton: {
  padding: "8px 10px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: 8,
  cursor: "pointer",
  fontWeight: 700,
},
deleteButton: {
  background: "#dc2626",
  color: "white",
  border: "none",
  padding: "8px 12px",
  borderRadius: 8,
  cursor: "pointer",
  fontWeight: 700,
},
vehicleOverviewCard: {
  border: "1px solid #e5e7eb",
  borderRadius: 16,
  padding: 20,
  marginBottom: 20,
},

vehicleOverviewHeader: {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: 20,
},

vehiclePlate: {
  margin: 0,
  fontSize: 22,
},

vehicleInfo: {
  marginTop: 6,
  color: "#64748b",
},

expiryGrid: {
  display: "grid",
  gridTemplateColumns: "repeat(4, 1fr)",
  gap: 14,
},

expiryItem: {
  background: "#f8fafc",
  padding: 14,
  borderRadius: 12,
},

obligationRow: {
  display: "flex",
  justifyContent: "space-between",
  padding: "12px 0",
  borderBottom: "1px solid #e5e7eb",
},

obligationTitle: {
  margin: 0,
  fontWeight: 700,
},
obligationActions: {
  display: "flex",
  alignItems: "center",
  gap: 12,
},

payButton: {
  background: "#2563eb",
  color: "white",
  border: "none",
  padding: "8px 12px",
  borderRadius: 8,
  cursor: "pointer",
  fontWeight: 700,
},
paymentCard: {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: 16,
  border: "1px solid #e5e7eb",
  borderRadius: 12,
  marginBottom: 12,
},
receiptButton: {
  marginTop: 8,
  background: "white",
  color: "#2563eb",
  border: "1px solid #2563eb",
  padding: "8px 10px",
  borderRadius: 8,
  cursor: "pointer",
  fontWeight: 700,
},
};

export default UserDashboard;