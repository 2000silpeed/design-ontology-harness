#!/usr/bin/env node
// fetch-pretendard.mjs — download Pretendard Variable (SIL OFL 1.1) on-demand.
//
// OFL permits redistribution, but we prefer to pull from upstream at
// install-time so users always get the latest glyphs and license notices.

import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";

const TARGET = "design-system/fonts/PretendardVariable.woff2";
const URL =
  "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2";

async function main() {
  const outPath = join(process.cwd(), TARGET);
  mkdirSync(dirname(outPath), { recursive: true });

  if (existsSync(outPath) && !process.argv.includes("--force")) {
    console.log(`[pretendard] already present: ${TARGET}`);
    return;
  }

  console.log(`[pretendard] fetching ${URL}`);
  const res = await fetch(URL);
  if (!res.ok) {
    throw new Error(`fetch failed: ${res.status} ${res.statusText}`);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  writeFileSync(outPath, buf);
  console.log(`[pretendard] wrote ${buf.byteLength} bytes → ${TARGET}`);
  console.log("[pretendard] see design-system/fonts/LICENSE-FONTS for SIL OFL 1.1 notice.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
