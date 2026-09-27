"use client";

import { useEffect, useState } from "react";

type Summary = {
  food_waste_prevented_kg: number;
  meals_redistributed_est: number;
  co2e_avoided_kg: number;
  total_redistribution_matches: number;
};

export default function Dashboard() {
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    fetch("/api/analytics/summary")
      .then((r) => r.json())
      .then(setSummary)
      .catch(() => setSummary(null));
  }, []);

  const stat = (label: string, value: string | number) => (
    <div
      style={{
        background: "white",
        border: "1px solid #e2e8e5",
        borderRadius: 12,
        padding: 20,
        minWidth: 160,
      }}
    >
      <div style={{ fontSize: 13, color: "#667" }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700, color: "#1f6f50" }}>{value}</div>
    </div>
  );

  return (
    <main style={{ maxWidth: 900, margin: "60px auto", padding: "0 24px" }}>
      <h1 style={{ color: "#1f6f50" }}>Sustainability Dashboard</h1>
      <p style={{ color: "#556" }}>
        Live metrics from the Redistribution Matching &amp; Analytics Agents.
        Wire this up to your deployed backend via <code>NEXT_PUBLIC_API_BASE</code>.
      </p>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginTop: 24 }}>
        {stat("Food waste prevented (kg)", summary?.food_waste_prevented_kg ?? "—")}
        {stat("Meals redistributed (est.)", summary?.meals_redistributed_est ?? "—")}
        {stat("CO2e avoided (kg)", summary?.co2e_avoided_kg ?? "—")}
        {stat("Redistribution matches", summary?.total_redistribution_matches ?? "—")}
      </div>
    </main>
  );
}
