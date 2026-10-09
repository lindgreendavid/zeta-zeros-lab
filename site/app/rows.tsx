"use client";

import { useState } from "react";
import { registry } from "./registry";

const ROWS = [
  { id: "A", key: "poisson", label: "Row A" },
  { id: "B", key: "zeta", label: "Row B" },
  { id: "C", key: "gue", label: "Row C" },
] as const;

const W = 640;
const PAD = 14;

/** Three rows of 61 points with the same average spacing. One is independent random points
 * (Poisson), one is the first zeta zeros after unfolding, one is a simulated random-matrix
 * (GUE) spectrum. Illustration only: every number tested in the study comes from 2,000-zero
 * blocks, not from this strip. */
export function Rows() {
  const [guess, setGuess] = useState<string | null>(null);
  const span = Math.max(...ROWS.map((r) => Math.max(...registry.samples[r.key])));
  const x = (v: number) => PAD + (v / span) * (W - 2 * PAD);

  return (
    <div>
      <div className="rows">
        <svg
          viewBox={`0 0 ${W} 190`}
          role="img"
          aria-label="Three rows of points: one random, one the first Riemann zeta zeros, one a simulated random-matrix spectrum"
        >
          {ROWS.map((row, i) => {
            const y = 40 + i * 60;
            return (
              <g key={row.id}>
                <text className="row-label" x={PAD} y={y - 16}>
                  {row.label}
                </text>
                <line x1={PAD} x2={W - PAD} y1={y} y2={y} stroke="#34405e" strokeWidth="1" />
                {registry.samples[row.key].map((v, k) => (
                  <line key={k} x1={x(v)} x2={x(v)} y1={y - 9} y2={y + 9} stroke="#f2c14e" strokeWidth="2" />
                ))}
              </g>
            );
          })}
        </svg>
      </div>
      <div className="row-guess" role="group" aria-label="Which row is the odd one out?">
        {ROWS.map((row) => (
          <button key={row.id} type="button" aria-pressed={guess === row.id} onClick={() => setGuess(row.id)}>
            {row.label} is the random one
          </button>
        ))}
      </div>
      <p className="row-result" role="status" aria-live="polite">
        {guess === null
          ? "Two rows have even, repelling spacing; one is independent random points, which clump and leave gaps. Pick the random one."
          : guess === "A"
            ? "Correct: Row A is independent random points (Poisson). Rows B and C are the first 61 zeta zeros and a simulated random-matrix spectrum, and the eye cannot tell them apart."
            : `Not quite: Row A is the independent random points. ${guess === "B" ? "Row B is the zeta zeros" : "Row C is the random-matrix simulation"}, and the two are hard to tell apart by eye, which is the surprising part.`}
      </p>
    </div>
  );
}
