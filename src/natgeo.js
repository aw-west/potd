import { JSDOM } from "jsdom";

export default function natgeo() {
  const pageUrl =
    "https://www.nationalgeographic.com/photography/photo-of-the-day/";
  return fetch(pageUrl)
    .then((response) => response.text())
    .then((html) => new JSDOM(html).window.document)
    .then((document) => [
      {
        source: "National Geographic",
        description:
          document.querySelector('meta[property="og:description"]')?.content ??
          "",
        pageUrl,
        imageUrl: document.querySelector('meta[property="og:image"]').content,
      },
    ])
    .catch(() => []);
}
