import { Lab } from "./lab";
import { registry } from "./registry";
import { Rows } from "./rows";

const h = registry.hypotheses;

function failing(map: Record<string, Record<string, boolean>>): string {
  const out: string[] = [];
  for (const [block, checks] of Object.entries(map)) {
    for (const [name, ok] of Object.entries(checks)) {
      if (!ok) out.push(`${block} block: ${name}`);
    }
  }
  return out.join("; ");
}

const rows = [
  {
    id: "H1",
    text: "GUE beats Poisson: in both blocks, both the spacing distance and the pair-correlation distance are smaller to GUE than to Poisson.",
    confirmed: h.H1.confirmed,
    yes: "Confirmed",
    no: "Falsified",
    detail: "",
  },
  {
    id: "H2",
    text: "Level repulsion: in both blocks fewer than 7.37% of spacings fall below 0.25 (one third of the Poisson value).",
    confirmed: h.H2.confirmed,
    yes: "Confirmed",
    no: "Falsified",
    detail: "",
  },
  {
    id: "H3",
    text: "Indistinguishable from GUE at this sample size: each measured distance sits inside the 95% sampling band of 150 simulated GUE samples of the same size, and the spacing variance sits inside its band.",
    confirmed: h.H3.confirmed,
    yes: "Confirmed",
    no: "Not confirmed",
    detail: failing(h.H3.per_block),
  },
  {
    id: "H4",
    text: "Agreement improves with height: the high block is closer to GUE than the low block on both distances.",
    confirmed: h.H4.confirmed,
    yes: "Confirmed",
    no: "Not confirmed",
    detail: Object.entries(h.H4.checks)
      .filter(([, ok]) => !ok)
      .map(([name]) => name)
      .join("; "),
  },
];

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <nav className="nav">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">
            ζ
          </span>
          <span>Zeta Zeros Lab</span>
        </div>
        <div className="nav__links">
          <a href="#see">See it</a>
          <a href="#lab">Laboratory</a>
          <a href="#report">Report</a>
          <a href="#sources">Sources</a>
        </div>
      </nav>

      <main id="main">
        <section className="hero">
          <div className="eyebrow">
            <span>Number theory × random matrices</span>
            <span>Question → measurement → finding → boundary</span>
          </div>
          <h1>
            Do the zeros of the zeta function behave like <em>random matrices</em>?
          </h1>
          <p className="hero__lead">
            The Riemann zeta zeros encode the primes, and their spacings look strangely like the eigenvalues of
            large random matrices. This laboratory measures that resemblance on 4,000 real zeros, against the
            exact random-matrix law, a random-points control, and a simulated null that shows how far genuine
            random matrices stray by chance.
          </p>
          <div className="hero__actions">
            <a className="button button--primary" href="#see">
              Try to spot the difference
            </a>
            <a className="button button--ghost" href="https://github.com/lindgreendavid/zeta-zeros-lab">
              View the repository
            </a>
          </div>
          <div className="hero__principles">
            <span>Preregistered thresholds</span>
            <span>Exact GUE reference</span>
            <span>Calibrated simulated null</span>
            <span>Riemann Hypothesis not claimed</span>
          </div>
        </section>

        <section className="lab" id="see">
          <div className="section-heading">
            <div>
              <span className="section-index">01</span>
              <p>First impression</p>
            </div>
            <h2>One of these rows is random</h2>
          </div>
          <Rows />
        </section>

        <section className="lab" id="lab">
          <div className="section-heading">
            <div>
              <span className="section-index">02</span>
              <p>Laboratory</p>
            </div>
            <h2>Measure it</h2>
          </div>
          <div className="limitations-first">
            <h3>Before you read the charts</h3>
            <ul>
              <li>
                This measures numerical agreement on two blocks of 2,000 zeros. It is not a proof, and it says
                nothing about whether the Riemann Hypothesis is true.
              </li>
              <li>
                Distances are not p-values: neighbouring zeros are not independent, so the study calibrates every
                distance against simulated random-matrix data of the same size instead.
              </li>
              <li>Only nearest-neighbour spacing and pair correlation are tested, using smooth-density unfolding.</li>
            </ul>
          </div>
          <Lab />
        </section>

        <section className="report" id="report">
          <div className="section-heading section-heading--light">
            <div>
              <span className="section-index">03</span>
              <p>Preregistered hypotheses</p>
            </div>
            <h2>What the data said</h2>
          </div>
          <table className="hypothesis-table">
            <caption className="sr-only">Preregistered hypotheses and their disposition</caption>
            <thead>
              <tr>
                <th scope="col">Hypothesis</th>
                <th scope="col">Disposition</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td>
                    <strong>{r.id}</strong> — {r.text}
                    {r.detail ? <div className="diagram-caption">Failed checks: {r.detail}</div> : null}
                  </td>
                  <td>
                    <span className={`disposition ${r.confirmed ? "disposition--confirmed" : "disposition--mixed"}`}>
                      {r.confirmed ? r.yes : r.no}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p>
            Full protocol, results and limitations:{" "}
            <a href="https://github.com/lindgreendavid/zeta-zeros-lab/blob/main/docs/research-report.md">
              docs/research-report.md
            </a>
            . The protocol was committed before the registry was generated.
          </p>
        </section>

        <section id="sources">
          <div className="section-heading">
            <div>
              <span className="section-index">04</span>
              <p>Research trail</p>
            </div>
            <h2>Sources</h2>
          </div>
          <div className="source-list">
            <a href="https://github.com/lindgreendavid/zeta-zeros-lab">
              <span>Repository</span>
              <strong>zeta-zeros-lab</strong>
              <p>Code, frozen zeros, tests, protocol, report and registry.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/zeta-zeros-lab/blob/main/docs/research-protocol.md">
              <span>Protocol</span>
              <strong>docs/research-protocol.md</strong>
              <p>Hypotheses and thresholds, fixed before any result existed.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/zeta-zeros-lab/blob/main/docs/research-report.md">
              <span>Report</span>
              <strong>docs/research-report.md</strong>
              <p>Dispositions, numbers, limitations, and what remains open.</p>
              <b aria-hidden="true">→</b>
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div>
          <span className="brand__mark" aria-hidden="true">
            ζ
          </span>
          <p>Part of the Lab Notes research portfolio.</p>
        </div>
        <a href="https://github.com/lindgreendavid/zeta-zeros-lab/blob/main/ACCESSIBILITY.md">
          Accessibility statement
        </a>
      </footer>
    </>
  );
}
