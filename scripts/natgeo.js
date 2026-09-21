import { JSDOM } from "jsdom";

export async function fetchPicture() {
  const pageUrl =
    "https://www.nationalgeographic.com/photography/photo-of-the-day/";
  const response = await fetch(pageUrl);
  const html = await response.text();
  const dom = new JSDOM(html);
  const document = dom.window.document;
  const imageUrl = document.querySelector('meta[property="og:image"]')?.content;
  const description =
    document.querySelector('meta[property="og:description"]')?.content ?? "";
  if (!imageUrl) return null;
  const date = new Date().toISOString().slice(0, 10);
  return {
    id: `${date}-national-geographic`,
    source: "National Geographic",
    date,
    description,
    pageUrl,
    imageUrl,
  };
}
