import { copyFile } from "node:fs/promises";

await copyFile(
  new URL("../../reports/v0.1-zeta-registry.json", import.meta.url),
  new URL("../app/registry.json", import.meta.url),
);
console.log("synced reports/v0.1-zeta-registry.json -> site/app/registry.json");
