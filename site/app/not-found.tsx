import Link from "next/link";

export default function NotFound() {
  return (
    <main className="status-page">
      <span className="brand__mark" aria-hidden="true">
        ζ
      </span>
      <p>404 · off the critical line</p>
      <h1>This page is not part of the study.</h1>
      <Link className="button button--primary" href="/">
        Return to Zeta Zeros Lab
      </Link>
    </main>
  );
}
