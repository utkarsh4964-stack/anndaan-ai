export default function Home() {
  return (
    <main style={{ maxWidth: 720, margin: "80px auto", padding: "0 24px" }}>
      <h1 style={{ color: "#1f6f50" }}>Anndaan.AI</h1>
      <p style={{ color: "#444", lineHeight: 1.6 }}>
        AI-powered smart food waste reduction &amp; redistribution platform for
        institutional kitchens and food processing units (SIH PS 26234).
      </p>
      <a
        href="/dashboard"
        style={{
          display: "inline-block",
          marginTop: 16,
          padding: "10px 18px",
          background: "#1f6f50",
          color: "white",
          borderRadius: 8,
          textDecoration: "none",
        }}
      >
        Open Dashboard →
      </a>
    </main>
  );
}
