import { JSDOM } from "jsdom";

export default function wiki() {
  const pageUrl = "https://commons.wikimedia.org/wiki/Main_Page";
  return fetch(pageUrl)
    .then((response) => response.text())
    .then((html) => new JSDOM(html).window.document)
    .then((document) => {
      return [
        {
          source: "Wikimedia",
          description: document
            .querySelector("#mf-picture-picture .description")
            ?.textContent.trim(),
          pageUrl,
          imageUrl: document
            .querySelector("#mf-picture-picture img")
            .src.replace("/thumb.", "/upload.")
            .replace("/thumb/", "/")
            .split("/")
            .slice(0, -1)
            .join("/"),
        },
      ];
    })
    .catch(() => []);
}
