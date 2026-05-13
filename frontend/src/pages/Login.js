import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
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
      const response = await api.post("/auth/token/", formData);

      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      const meResponse = await api.get("/users/me/");

      const role = meResponse.data.role;

      if (
          role === "institution_officer" ||
          role === "institution_admin" ||
          role === "system_admin"
         ) {
            navigate("/institution");
          } else {
            navigate("/citizen");
          }

      navigate("/citizen");
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>Vehicle Management System</h1>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            style={styles.input}
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            style={styles.input}
          />

          {error && <p style={styles.error}>{error}</p>}

          <button type="submit" style={styles.button}>
            Login
          </button>
          <button
              type="button"
              style={styles.linkButton}
              onClick={() => navigate("/register")}
          >
                 Create new citizen account
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#f4f7fb",
  },

  card: {
    width: "400px",
    padding: "40px",
    background: "white",
    borderRadius: "12px",
    boxShadow: "0 0 20px rgba(0,0,0,0.1)",
  },

  input: {
    width: "100%",
    padding: "12px",
    marginTop: "15px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },

  button: {
    width: "100%",
    padding: "12px",
    marginTop: "20px",
    background: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },

  error: {
    color: "red",
    marginTop: "10px",
  },
  linkButton: {
  width: "100%",
  marginTop: "12px",
  background: "transparent",
  border: "none",
  color: "#2563eb",
  cursor: "pointer",
  fontWeight: 700,
},
};

export default Login;