import fs from "fs-extra";

import { fetchPicture as nasa } from "./nasa.js";
import { fetchPicture as bing } from "./bing.js";
import { fetchPicture as wiki } from "./wiki.js";
import { fetchPicture as natgeo } from "./natgeo.js";
import { fetchPicture as guardian } from "./guardian.js";
import { fetchPicture as smithsonian } from "./smithsonian.js";

const sources = [nasa, bing, wiki, natgeo, guardian, smithsonian];

const archiveFile = "./docs/archive.json";
let archive = [];

try {
  archive = await fs.readJson(archiveFile);
} catch {
  archive = [];
}

for (const source of sources) {
  const result = await source();
  if (!result) {
    continue;
  }
  const items = Array.isArray(result) ? result : [result];
  for (const item of items) {
    const exists = archive.some((x) => x.imageUrl === item.imageUrl);
    if (!exists) {
      archive.unshift(item);
    }
  }
}

archive.sort((a, b) => new Date(b.date) - new Date(a.date));
await fs.writeJson(archiveFile, archive, { spaces: 2 });
await fs.writeJson("./docs/latest.json", archive, { spaces: 2 });
console.log(`Stored ${archive.length} images`);
