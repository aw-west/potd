import fs from "fs-extra";

import bing from "./bing.js";
import guardian from "./guardian.js";
import nasa from "./nasa.js";
import natgeo from "./natgeo.js";
import smithsonian from "./smithsonian.js";
import wiki from "./wiki.js";

const archiveFile = "./docs/archive.json";
const latestFile = "./docs/latest.json";

const archive = await fs.readJson(archiveFile).catch(() => []);
const imageUrls = new Set(archive.map((x) => x.imageUrl));
const date = new Date().toISOString().slice(0, 10);

const latest = (
  await Promise.all([
    bing(),
    guardian(),
    nasa(),
    natgeo(),
    smithsonian(),
    wiki(),
  ])
)
  .flat()
  .filter(Boolean)
  .map((item) => ({ date, ...item }));
latest.sort(
  (a, b) => a.date.localeCompare(b.date) || a.source.localeCompare(b.source),
);

await fs.writeJson(latestFile, latest, { spaces: 2 });
archive.unshift(...latest.filter((item) => !imageUrls.has(item.imageUrl)));
await fs.writeJson(archiveFile, archive, { spaces: 2 });
