// one-image-news — entry for make.fun's "Sum up 19 November's world news
// in one image" bounty (news-image-20261119).
//
// The repository holds the finished front page as front-page-v2.png (the
// illustrated V2 edition; V1 remains alongside it as front-page.png). This
// program copies the V2 page, byte for byte, to entry.png in the output
// directory (MAKEFUN_OUTPUT_DIR, or /output when unset). It uses only the
// Node.js standard library and no network, so every run writes identical
// bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "front-page-v2.png"), join(outDir, "entry.png"));
