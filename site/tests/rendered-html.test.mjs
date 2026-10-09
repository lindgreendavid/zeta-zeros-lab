import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the finished laboratory", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>Zeta Zeros Lab/);
  assert.match(html, /random matrices/);
  assert.match(html, /One of these rows is random/);
  assert.match(html, /Neighbour spacings/);
  assert.match(html, /Pair correlation/);
  assert.match(html, /Preregistered hypotheses/);
  assert.match(html, /Skip to main content/);
  assert.match(html, /Riemann Hypothesis not claimed/);
  assert.match(html, /Read the spacing histogram as a table/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Starter Project/);
});

test("ships accessible controls and research boundaries", async () => {
  const [page, lab, rows, layout, styles, packageJson] = await Promise.all([
    readFile(new URL("app/page.tsx", root), "utf8"),
    readFile(new URL("app/lab.tsx", root), "utf8"),
    readFile(new URL("app/rows.tsx", root), "utf8"),
    readFile(new URL("app/layout.tsx", root), "utf8"),
    readFile(new URL("app/globals.css", root), "utf8"),
    readFile(new URL("package.json", root), "utf8"),
  ]);
  assert.match(page, /className="skip-link"/);
  assert.match(page, /limitations-first/);
  assert.match(lab, /role="group" aria-label="Which block of zeros"/);
  assert.match(lab, /aria-pressed/);
  assert.match(rows, /role="status" aria-live="polite"/);
  assert.match(styles, /prefers-contrast: more/);
  assert.match(styles, /forced-colors: active/);
  assert.match(styles, /prefers-reduced-motion: reduce/);
  assert.match(layout, /Zeta Zeros Lab/);
  assert.doesNotMatch(packageJson, /react-loading-skeleton|drizzle/);
});

test("ships the frozen registry unchanged and consistent with its verdicts", async () => {
  const shipped = await readFile(new URL("app/registry.json", root), "utf8");
  const frozen = await readFile(new URL("../reports/v0.1-zeta-registry.json", root), "utf8");
  assert.deepEqual(JSON.parse(shipped), JSON.parse(frozen));
  const registry = JSON.parse(shipped);
  assert.equal(registry.schema_version, "0.1");
  assert.equal(Object.keys(registry.blocks).length, 2);
  for (const block of Object.values(registry.blocks)) {
    assert.equal(block.n_zeros, 2000);
    assert.equal(block.spacing_histogram.length, 30);
    assert.equal(block.pair_correlation.length, 30);
  }
  // Re-derive H1 from the raw statistics so the page cannot show a verdict the data contradicts.
  const h1 = Object.values(registry.blocks).every(
    (b) => b.stats.ks_gue < b.stats.ks_poisson && b.stats.r2_rms_gue < b.stats.r2_rms_poisson,
  );
  assert.equal(registry.hypotheses.H1.confirmed, h1);
});
