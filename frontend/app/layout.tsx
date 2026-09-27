export const metadata = {
  title: "Anndaan.AI",
  description: "AI-powered smart food waste reduction & redistribution platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif", background: "#f7faf8" }}>
        {children}
      </body>
    </html>
  );
}
