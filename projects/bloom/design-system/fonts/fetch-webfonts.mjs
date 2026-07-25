// 확인된 소스에서 웹폰트를 내려받습니다. 폰트 바이너리는 커밋하지 않습니다.
// 사용: node design-system/fonts/fetch-webfonts.mjs
import { writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const targets = [
  { url: "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2", file: "PretendardVariable.woff2" }
];

for (const { url, file } of targets) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${file}: ${response.status} ${response.statusText}`);
  }
  await writeFile(join(here, file), Buffer.from(await response.arrayBuffer()));
  console.log(`fetched ${file}`);
}
