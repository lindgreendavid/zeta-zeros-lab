"use client";

import { registry, type Block } from "./registry";

const W = 640;
const H = 300;
const M = { l: 44, r: 12, t: 12, b: 30 };

function sx(v: number, max: number): number {
  return M.l + (v / max) * (W - M.l - M.r);
}
function sy(v: number, max: number): number {
  return H - M.b - (v / max) * (H - M.t - M.b);
}
function path(xs: number[], ys: number[], xmax: number, ymax: number): string {
  return xs
    .map((x, i) => `${i === 0 ? "M" : "L"} ${sx(x, xmax).toFixed(1)} ${sy(ys[i], ymax).toFixed(1)}`)
    .join(" ");
}

function Legend({ gueLabel, poissonLabel }: { gueLabel: string; poissonLabel: string }) {
  return (
    <div className="legend">
      <span>
        <i className="swatch-zeta" /> Zeta zeros (measured)
      </span>
      <span>
        <i className="swatch-gue" /> {gueLabel}
      </span>
      <span>
        <i className="swatch-poisson" /> {poissonLabel}
      </span>
    </div>
  );
}

export function SpacingChart({ block }: { block: Block }) {
  const ref = registry.reference;
  const hist = block.spacing_histogram;
  const xmax = 3;
  const ymax = 1.1;
  const binW = xmax / hist.length;
  return (
    <div className="chart-wrap">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label="Histogram of normalized zero spacings compared with the GUE and Poisson predictions"
      >
        {[0, 0.5, 1].map((t) => (
          <g key={t}>
            <line x1={M.l} x2={W - M.r} y1={sy(t, ymax)} y2={sy(t, ymax)} stroke="#cdd5e5" />
            <text x={6} y={sy(t, ymax) + 3}>
              {t.toFixed(1)}
            </text>
          </g>
        ))}
        {[0, 1, 2, 3].map((t) => (
          <text key={t} x={sx(t, xmax) - 3} y={H - 10}>
            {t}
          </text>
        ))}
        {hist.map((d, i) => (
          <rect
            key={i}
            x={sx(i * binW, xmax) + 1}
            y={sy(d, ymax)}
            width={sx(binW, xmax) - M.l - 2}
            height={sy(0, ymax) - sy(d, ymax)}
            fill="#f2c14e"
            stroke="#10182b"
            strokeWidth="0.6"
          />
        ))}
        <path d={path(ref.spacing_grid, ref.gue_pdf, xmax, ymax)} fill="none" stroke="#1b5bb8" strokeWidth="2.5" />
        <path
          d={path(ref.spacing_grid, ref.poisson_pdf, xmax, ymax)}
          fill="none"
          stroke="#4b5876"
          strokeWidth="2"
          strokeDasharray="6 5"
        />
        <text x={W / 2 - 60} y={H - 1}>
          normalized spacing s
        </text>
      </svg>
      <Legend gueLabel="GUE (exact)" poissonLabel="Poisson (random points)" />
      <details className="data-alternative">
        <summary>Read the spacing histogram as a table</summary>
        {/* A scrollable region must be keyboard-focusable (WCAG 2.1.1). */}
        {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
        <div className="table-scroll" tabIndex={0} role="region" aria-label="Scrollable spacing data table">
          <table>
            <caption>Spacing density by bin: measured, exact GUE, Poisson</caption>
            <thead>
              <tr>
                <th scope="col">s from</th>
                <th scope="col">Zeta</th>
                <th scope="col">GUE</th>
                <th scope="col">Poisson</th>
              </tr>
            </thead>
            <tbody>
              {hist.map((d, i) => {
                const gi = ((i + 0.5) * binW) / 0.05;
                const gue = (ref.gue_pdf[Math.floor(gi)] + ref.gue_pdf[Math.ceil(gi)]) / 2;
                return (
                  <tr key={i}>
                    <td>{(i * binW).toFixed(1)}</td>
                    <td>{d.toFixed(3)}</td>
                    <td>{gue.toFixed(3)}</td>
                    <td>{Math.exp(-(i + 0.5) * binW).toFixed(3)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  );
}

export function PairChart({ block }: { block: Block }) {
  const ref = registry.reference;
  const data = block.pair_correlation;
  const xmax = 3;
  const ymax = 1.5;
  return (
    <div className="chart-wrap">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label="Pair correlation of the zeros compared with the GUE curve and the Poisson line"
      >
        {[0, 0.5, 1, 1.5].map((t) => (
          <g key={t}>
            <line x1={M.l} x2={W - M.r} y1={sy(t, ymax)} y2={sy(t, ymax)} stroke="#cdd5e5" />
            <text x={6} y={sy(t, ymax) + 3}>
              {t.toFixed(1)}
            </text>
          </g>
        ))}
        {[0, 1, 2, 3].map((t) => (
          <text key={t} x={sx(t, xmax) - 3} y={H - 10}>
            {t}
          </text>
        ))}
        <line
          x1={M.l}
          x2={W - M.r}
          y1={sy(1, ymax)}
          y2={sy(1, ymax)}
          stroke="#4b5876"
          strokeWidth="2"
          strokeDasharray="6 5"
        />
        <path
          d={path(ref.gue_pair_correlation_curve_x, ref.gue_pair_correlation_curve, xmax, ymax)}
          fill="none"
          stroke="#1b5bb8"
          strokeWidth="2.5"
        />
        {data.map((d, i) => (
          <circle
            key={i}
            cx={sx(ref.pair_centers[i], xmax)}
            cy={sy(d, ymax)}
            r="4"
            fill="#f2c14e"
            stroke="#10182b"
            strokeWidth="1"
          />
        ))}
        <text x={W / 2 - 60} y={H - 1}>
          distance between zeros r
        </text>
      </svg>
      <Legend gueLabel="GUE: 1 − (sin πr / πr)²" poissonLabel="Poisson: 1" />
      <details className="data-alternative">
        <summary>Read the pair correlation as a table</summary>
        {/* A scrollable region must be keyboard-focusable (WCAG 2.1.1). */}
        {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
        <div className="table-scroll" tabIndex={0} role="region" aria-label="Scrollable pair correlation data table">
          <table>
            <caption>Pair correlation by lag bin</caption>
            <thead>
              <tr>
                <th scope="col">Lag r (bin centre)</th>
                <th scope="col">Zeta</th>
                <th scope="col">GUE</th>
              </tr>
            </thead>
            <tbody>
              {data.map((d, i) => (
                <tr key={i}>
                  <td>{ref.pair_centers[i].toFixed(2)}</td>
                  <td>{d.toFixed(3)}</td>
                  <td>{ref.gue_pair_correlation[i].toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </div>
  );
}
