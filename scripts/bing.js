export default function bing() {
  const pageUrl = "https://www.bing.com";
  return fetch(`${pageUrl}/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-GB`)
    .then((response) => response.json())
    .then((json) => json.images?.[0])
    .then((image) => [
      {
        source: "Bing",
        description: image.copyright ?? "",
        pageUrl,
        imageUrl: `${pageUrl}${image.url.split("&")[0]}`,
      },
    ])
    .catch(() => []);
}
