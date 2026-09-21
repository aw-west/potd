import { JSDOM } from "jsdom";

const FEEDS = [
  {
    source: "Guardian UK",
    pageUrl:
      "https://www.theguardian.com/news/series/ten-best-photographs-of-the-day",
  },
  {
    source: "Guardian International",
    pageUrl: "https://www.theguardian.com/international",
  },
];

async function fetchFeed(feed) {
  const response = await fetch(feed.pageUrl);
  const html = await response.text();
  const dom = new JSDOM(html);
  const image = dom.window.document.querySelector("picture img");
  if (!image) return null;
  const date = new Date().toISOString().slice(0, 10);
  const source = feed.source;
  return {
    id: `${date}-${source.toLowerCase().replaceAll(" ", "-")}`,
    source,
    date,
    description: image.alt ?? "",
    pageUrl: feed.pageUrl,
    imageUrl: image.src,
  };
}

export async function fetchPicture() {
  const results = [];
  for (const feed of FEEDS) {
    try {
      const item = await fetchFeed(feed);

      if (item) results.push(item);
    } catch (err) {
      console.error(`${feed.source}:`, err.message);
    }
  }
  return results;
}
