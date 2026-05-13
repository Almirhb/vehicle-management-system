import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function RegisterVehicle() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    plate_number: "",
    vin: "",
    make: "",
    model: "",
    year: "",
    color: "",
    registration_date: "",
    inspection_expiry: "",
    insurance_expiry: "",
    engine_number: "",
    market_value: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const today = new Date().toISOString().split("T")[0];

    const payload = {
          ...formData,
        registration_date: today,
         market_value: formData.market_value || "0.00",
          };

    const res = await api.post("/vehicles/", payload);

      await api.post(`/vehicles/${res.data.id}/submit-for-approval/`);

      navigate("/citizen");
    } catch (err) {
  console.error(err);

  if (err.response && err.response.data) {
    setError(JSON.stringify(err.response.data));
  } else {
    setError("Vehicle registration failed.");
  }
}
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1>Register New Vehicle</h1>
        <p style={styles.subtitle}>
          Submit your vehicle information for institution approval.
        </p>

<form onSubmit={handleSubmit}>
  <input
    name="plate_number"
    placeholder="Targa e mjetit"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <input
    name="vin"
    placeholder="Numri i shasisë (VIN)"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <input
    name="make"
    placeholder="Marka e mjetit"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <input
    name="model"
    placeholder="Modeli"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <input
    name="year"
    placeholder="Viti i prodhimit"
    type="number"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <input
    name="color"
    placeholder="Ngjyra"
    onChange={handleChange}
    style={styles.input}
  />

  <label style={styles.label}>
    Data e skadimit të lejes së qarkullimit
  </label>

  <input
    name="circulation_permit_expiry"
    type="date"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <label style={styles.label}>
    Data e skadimit të taksave
  </label>

  <input
    name="road_tax_expiry"
    type="date"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <label style={styles.label}>
    Data e skadimit të kolaudimit
  </label>

  <input
    name="inspection_expiry"
    type="date"
    onChange={handleChange}
    style={styles.input}
    required
  />

  <label style={styles.label}>
    Data e skadimit të siguracionit
  </label>

  <input
    name="insurance_expiry"
    type="date"
    onChange={handleChange}
    style={styles.input}
    required
  />

  {error && <p style={styles.error}>{error}</p>}

  <button type="submit" style={styles.button}>
    Dërgo për aprovim
  </button>

  <button
    type="button"
    style={styles.secondaryButton}
    onClick={() => navigate("/citizen")}
  >
    Kthehu te dashboard
  </button>
</form>

      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f7fb",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Arial, sans-serif",
  },
  card: {
    width: 520,
    background: "white",
    padding: 36,
    borderRadius: 16,
    boxShadow: "0 8px 24px rgba(0,0,0,0.1)",
  },
  subtitle: {
    color: "#64748b",
    marginBottom: 20,
  },
  input: {
    width: "100%",
    padding: 12,
    marginBottom: 12,
    border: "1px solid #d1d5db",
    borderRadius: 10,
  },
  label: {
    fontSize: 13,
    fontWeight: 700,
    color: "#475569",
  },
  button: {
    width: "100%",
    padding: 12,
    background: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: 10,
    fontWeight: 700,
    cursor: "pointer",
  },
  secondaryButton: {
    width: "100%",
    padding: 12,
    marginTop: 10,
    background: "white",
    color: "#2563eb",
    border: "1px solid #2563eb",
    borderRadius: 10,
    fontWeight: 700,
    cursor: "pointer",
  },
  error: {
    color: "#dc2626",
  },
};

export default RegisterVehicle;