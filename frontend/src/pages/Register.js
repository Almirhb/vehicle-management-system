import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    national_id: "",
    phone: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/users/", {
        ...formData,
        role: "citizen",
      });

      setSuccess("Account created successfully. You can now login.");
      setError("");

      setTimeout(() => {
        navigate("/");
      }, 1000);
    } catch (err) {
      setError("Registration failed. Check your data.");
      setSuccess("");
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>Create Citizen Account</h1>
        <p style={styles.subtitle}>
          Register to manage your vehicles, obligations, documents, and payments.
        </p>

        <form onSubmit={handleSubmit}>
          <input
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            style={styles.input}
            required
          />

          <input
            name="email"
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
            required
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            style={styles.input}
            required
          />

          <input
            name="national_id"
            placeholder="National ID"
            value={formData.national_id}
            onChange={handleChange}
            style={styles.input}
            required
          />

          <input
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            style={styles.input}
          />

          {error && <p style={styles.error}>{error}</p>}
          {success && <p style={styles.success}>{success}</p>}

          <button type="submit" style={styles.button}>
            Register
          </button>
        </form>

        <button style={styles.linkButton} onClick={() => navigate("/")}>
          Already have an account? Login
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "#f4f7fb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Arial, sans-serif",
  },
  card: {
    width: 430,
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
    marginBottom: 14,
    border: "1px solid #d1d5db",
    borderRadius: 10,
  },
  button: {
    width: "100%",
    padding: 12,
    border: "none",
    borderRadius: 10,
    background: "#2563eb",
    color: "white",
    fontWeight: 700,
    cursor: "pointer",
  },
  linkButton: {
    marginTop: 14,
    width: "100%",
    background: "transparent",
    border: "none",
    color: "#2563eb",
    cursor: "pointer",
    fontWeight: 700,
  },
  error: {
    color: "#dc2626",
  },
  success: {
    color: "#16a34a",
  },
};

export default Register;