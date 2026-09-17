import { useEffect, useState } from "react";

export default function SavingsTicker({ totalSaved }) {
  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    if (totalSaved === 0) return;
    setPulse(true);
    const timeout = setTimeout(() => setPulse(false), 400);
    return () => clearTimeout(timeout);
  }, [totalSaved]);

  return (
    <div className={`savings-ticker ${pulse ? "pulse" : ""}`}>
      <span className="savings-label">Session savings vs. always-flagship</span>
      <span className="savings-value">${totalSaved.toFixed(6)}</span>
    </div>
  );
}
