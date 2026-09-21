export async function fetchPicture() {
  const response = await fetch(
    "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-GB",
  );
  if (!response.ok) {
    throw new Error(`Bing: ${response.status}`);
  }

  const data = await response.json();
  if (!data.images?.length) {
    return null;
  }

  const image = data.images[0];
  const source = "bing";
  const date = `${image.enddate.slice(0, 4)}-${image.enddate.slice(4, 6)}-${image.enddate.slice(6, 8)}`;
  return {
    id: `${source}-${date}`,
    source,
    date,
    description: image.copyright ?? "",
    pageUrl: "https://www.bing.com",
    imageUrl: `https://www.bing.com${image.url}`,
  };
}
