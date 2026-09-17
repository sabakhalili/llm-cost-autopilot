import { useState } from "react";

const TIER_LABEL = { simple: "Simple", medium: "Medium", hard: "Hard" };

function formatCost(value) {
  return `$${value.toFixed(6)}`;
}

export default function RoutingStrip({ routing }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`routing-strip tier-${routing.complexity_tier}`}>
      <button className="routing-strip-header" onClick={() => setExpanded((e) => !e)}>
        <span className={`tier-badge tier-${routing.complexity_tier}`}>
          {TIER_LABEL[routing.complexity_tier]}
        </span>
        <span className="routing-model">{routing.model_display_name}</span>
        <span className="routing-saved">saved {formatCost(routing.cost_saved)}</span>
        <span className="routing-caret">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <div className="routing-strip-details">
          <p className="routing-reason">{routing.reason}</p>
          <dl>
            <dt>Tokens</dt>
            <dd>{routing.input_tokens} in / {routing.output_tokens} out</dd>
            <dt>Latency</dt>
            <dd>{Math.round(routing.latency_ms)} ms</dd>
            <dt>Actual cost</dt>
            <dd>{formatCost(routing.cost_actual)}</dd>
            <dt>Baseline cost ({routing.baseline_model_display_name})</dt>
            <dd>{formatCost(routing.cost_baseline)}</dd>
          </dl>
        </div>
      )}
    </div>
  );
}
