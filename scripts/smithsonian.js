import { JSDOM } from "jsdom";

const CATEGORIES = [
  "artistic",
  "drone-aerial",
  "people",
  "travel",
  "natural-world",
];

function extractOriginalImageUrl(url) {
  if (!url) {
    return null;
  }
  if (!url.includes("th-thumbnailer.cdn-si-edu.com")) {
    return url;
  }
  const marker = "/https%3A";
  const pos = url.indexOf(marker);
  if (pos === -1) {
    return url;
  }
  try {
    return decodeURIComponent(url.substring(pos + 1));
  } catch {
    return url;
  }
}

async function fetchCategory(category) {
  const categoryUrl = `https://photocontest.smithsonianmag.com/photocontest/categories/${category}/`;
  const categoryResponse = await fetch(categoryUrl);
  if (!categoryResponse.ok) {
    throw new Error(`Category ${categoryResponse.status}`);
  }
  const categoryHtml = await categoryResponse.text();
  const categoryDom = new JSDOM(categoryHtml);
  const detailLink = categoryDom.window.document.querySelector(
    'a[href*="/photocontest/detail/"]',
  );
  if (!detailLink) {
    console.warn(`No detail page for ${category}`);
    return null;
  }
  const detailUrl = new URL(detailLink.href, categoryUrl).href;
  const detailResponse = await fetch(detailUrl);
  if (!detailResponse.ok) {
    throw new Error(`Detail ${detailResponse.status}`);
  }
  const detailHtml = await detailResponse.text();
  const detailDom = new JSDOM(detailHtml);
  const document = detailDom.window.document;
  const ogImage = document.querySelector('meta[property="og:image"]')?.content;
  const description =
    document.querySelector('meta[property="og:description"]')?.content ?? "";
  if (!ogImage) {
    console.warn(`No og:image for ${category}`);
    return null;
  }
  const source = `smithsonian-${category}`;
  const date = new Date().toISOString().slice(0, 10);
  return {
    id: `${source}-${date}`,
    source,
    date,
    description,
    pageUrl: detailUrl,
    imageUrl: extractOriginalImageUrl(ogImage),
  };
}

export async function fetchPicture() {
  const results = [];
  for (const category of CATEGORIES) {
    try {
      const item = await fetchCategory(category);
      if (item) {
        results.push(item);
      }
    } catch (err) {
      console.error(`Smithsonian ${category}:`, err.message);
    }
  }
  return results;
}
