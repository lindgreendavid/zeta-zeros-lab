"use client";

import { useState } from "react";
import { PairChart, SpacingChart } from "./charts";
import { registry } from "./registry";

type BlockKey = "low" | "high";
type View = "spacing" | "pair";

function Verdict({ ok, yes, no }: { ok: boolean; yes: string; no: string }) {
  return <span className={`verdict ${ok ? "verdict--yes" : "verdict--no"}`}>{ok ? yes : no}</span>;
}

export function Lab() {
  const [blockKey, setBlockKey] = useState<BlockKey>("low");
  const [view, setView] = useState<View>("spacing");
  const block = registry.blocks[blockKey];
  const s = block.stats;
  const nul = registry.simulated_gue_null;
  const ref = registry.reference;

  return (
    <div>
      <div className="block-switch" role="group" aria-label="Which block of zeros">
        {(["low", "high"] as const).map((k) => (
          <button key={k} type="button" aria-pressed={blockKey === k} onClick={() => setBlockKey(k)}>
            {k === "low" ? "Low zeros" : "High zeros"} (n = {registry.blocks[k].first_index.toLocaleString("en-US")}–
            {(registry.blocks[k].first_index + registry.blocks[k].n_zeros - 1).toLocaleString("en-US")})
          </button>
        ))}
      </div>
      <div className="block-switch" role="group" aria-label="Which statistic">
        <button type="button" aria-pressed={view === "spacing"} onClick={() => setView("spacing")}>
          Neighbour spacings
        </button>
        <button type="button" aria-pressed={view === "pair"} onClick={() => setView("pair")}>
          Pair correlation
        </button>
      </div>

      <p className="diagram-caption">
        Heights {block.gamma_min.toLocaleString("en-US", { maximumFractionDigits: 1 })} to{" "}
        {block.gamma_max.toLocaleString("en-US", { maximumFractionDigits: 1 })}; {block.n_zeros.toLocaleString("en-US")}{" "}
        consecutive zeros, {s.n_spacings.toLocaleString("en-US")} spacings.
      </p>

      {view === "spacing" ? <SpacingChart block={block} /> : <PairChart block={block} />}

      <table className="stat-table">
        <caption>
          Measured statistics for this block, against exact GUE, Poisson, and the {nul.n_replicates} simulated GUE
          samples of the same size
        </caption>
        <thead>
          <tr>
            <th scope="col">Statistic</th>
            <th scope="col">Measured</th>
            <th scope="col">GUE sampling band (95%)</th>
            <th scope="col">Reading</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Spacing distance to GUE (KS)</td>
            <td>{s.ks_gue.toFixed(4)}</td>
            <td>up to {nul.ks_gue.q975.toFixed(4)}</td>
            <td>
              <Verdict ok={s.ks_gue <= nul.ks_gue.q975} yes="Within GUE scatter" no="Beyond GUE scatter" />
            </td>
          </tr>
          <tr>
            <td>Spacing distance to Poisson (KS)</td>
            <td>{s.ks_poisson.toFixed(4)}</td>
            <td>n/a</td>
            <td>
              <Verdict ok={s.ks_gue < s.ks_poisson} yes="GUE is closer" no="Poisson is closer" />
            </td>
          </tr>
          <tr>
            <td>Pair-correlation RMS to GUE</td>
            <td>{s.r2_rms_gue.toFixed(4)}</td>
            <td>up to {nul.r2_rms_gue.q975.toFixed(4)}</td>
            <td>
              <Verdict ok={s.r2_rms_gue <= nul.r2_rms_gue.q975} yes="Within GUE scatter" no="Beyond GUE scatter" />
            </td>
          </tr>
          <tr>
            <td>Pair-correlation RMS to Poisson</td>
            <td>{s.r2_rms_poisson.toFixed(4)}</td>
            <td>n/a</td>
            <td>
              <Verdict ok={s.r2_rms_gue < s.r2_rms_poisson} yes="GUE is closer" no="Poisson is closer" />
            </td>
          </tr>
          <tr>
            <td>Spacing variance (GUE {ref.gue_spacing_variance.toFixed(3)}, Poisson 1)</td>
            <td>{s.variance.toFixed(4)}</td>
            <td>
              {nul.variance.q025.toFixed(4)} to {nul.variance.q975.toFixed(4)}
            </td>
            <td>
              <Verdict
                ok={s.variance >= nul.variance.q025 && s.variance <= nul.variance.q975}
                yes="Within GUE scatter"
                no="Beyond GUE scatter"
              />
            </td>
          </tr>
          <tr>
            <td>
              Share of spacings below {registry.small_spacing_cutoff} (GUE {ref.gue_small_fraction.toFixed(4)}, Poisson{" "}
              {ref.poisson_small_fraction.toFixed(4)})
            </td>
            <td>{s.small_fraction.toFixed(4)}</td>
            <td>
              {nul.small_fraction.q025.toFixed(4)} to {nul.small_fraction.q975.toFixed(4)}
            </td>
            <td>
              <Verdict ok={s.small_fraction < 0.0737} yes="Repulsion present" no="No repulsion" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
