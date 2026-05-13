import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

///import Login from "./pages/Login";
import Register from "./pages/Register";
import Login from "./pages/Login";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import RegisterVehicle from "./pages/RegisterVehicle";

function CitizenDashboard() {
  return (
    <div>
      <h1>Citizen Dashboard</h1>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    
<Routes>
  <Route path="/" element={<Login />} />
  <Route path="/citizen" element={<UserDashboard />} />
  <Route path="/institution" element={<AdminDashboard />} />
  <Route path="/register" element={<Register />} />
  <Route path="/citizen/register-vehicle" element={<RegisterVehicle />} />
</Routes>
  </BrowserRouter>
);