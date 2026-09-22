import { JSDOM } from "jsdom";

const CATEGORIES = [
  "Artistic",
  "Drone-Aerial",
  "Natural-World",
  "People",
  "Travel",
  "Wildlife",
];

function extractOriginalImageUrl(url) {
  if (!url?.includes("th-thumbnailer.cdn-si-edu.com")) {
    return url;
  }

  try {
    return decodeURIComponent(url.substring(url.indexOf("/https%3A") + 1));
  } catch {
    return url;
  }
}

function fetchCategory(category) {
  const pageUrl = `https://photocontest.smithsonianmag.com/photocontest/categories/${category}/`;

  return fetch(pageUrl)
    .then((r) => r.text())
    .then((html) => new JSDOM(html).window.document)
    .then(
      (document) =>
        new URL(
          document.querySelector('a[href*="/photocontest/detail/"]').href,
          pageUrl,
        ).href,
    )
    .then((detailUrl) =>
      fetch(detailUrl)
        .then((r) => r.text())
        .then((html) => ({
          detailUrl,
          document: new JSDOM(html).window.document,
        })),
    )
    .then(({ detailUrl, document }) => ({
      source: `Smithsonian ${category}`,
      description:
        document.querySelector('meta[property="og:description"]')?.content ??
        "",
      pageUrl: detailUrl,
      imageUrl: extractOriginalImageUrl(
        document.querySelector('meta[property="og:image"]').content,
      ),
    }))
    .catch(() => null);
}

export default function smithsonian() {
  return Promise.all(CATEGORIES.map(fetchCategory));
}
