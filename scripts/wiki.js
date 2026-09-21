import { JSDOM } from "jsdom";

export async function fetchPicture() {
  const pageUrl = "https://commons.wikimedia.org/wiki/Main_Page";
  const response = await fetch(pageUrl);
  const html = await response.text();
  const dom = new JSDOM(html);
  const document = dom.window.document;
  let imageUrl = document.querySelector('meta[property="og:image"]')?.content;
  if (!imageUrl) {
    const image = [...document.querySelectorAll("img")].find(
      (img) => !img.src.endsWith(".svg"),
    );
    imageUrl = image?.src;
  }
  if (!imageUrl) return null;
  const description =
    document.querySelector('meta[property="og:description"]')?.content ??
    document.title ??
    "";
  const date = new Date().toISOString().slice(0, 10);
  return {
    id: `${date}-wikimedia`,
    source: "Wikimedia",
    date,
    description,
    pageUrl,
    imageUrl: imageUrl.startsWith("//") ? `https:${imageUrl}` : imageUrl,
  };
}
