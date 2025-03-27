
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./index.css";
import ECFRDashboard from "./ECFRDashboard";
import MetricsDashboard from "./MetricsDashboard";
import Layout from "./Layout";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<ECFRDashboard />} />
          <Route path="/metrics" element={<MetricsDashboard />} />
        </Routes>
      </Layout>
    </Router>
  </React.StrictMode>
);
