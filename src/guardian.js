import { JSDOM } from "jsdom";

export default function guardian() {
  const pageUrl =
    "https://www.theguardian.com/news/series/ten-best-photographs-of-the-day";
  return fetch(pageUrl)
    .then((r) => r.text())
    .then((html) => new JSDOM(html).window.document)
    .then((document) => document.querySelector("picture"))
    .then((picture) => {
      const candidates = [...picture.querySelectorAll("source[srcset]")]
        .flatMap((source) => source.getAttribute("srcset").split(","))
        .map((entry) => entry.trim().split(/\s+/))
        .map(([url, width]) => ({ url, width: parseInt(width, 10) || 0 }))
        .sort((a, b) => b.width - a.width);

      return [
        {
          source: "Guardian",
          description: picture.querySelector("img")?.alt ?? "",
          pageUrl,
          imageUrl: candidates[0]?.url ?? picture.querySelector("img")?.src,
        },
      ];
    })
    .catch(() => []);
}
