export async function fetchPicture() {
  const response = await fetch(
    "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY",
  );
  if (!response.ok) {
    throw new Error(`NASA API: ${response.status}`);
  }

  const apod = await response.json();
  if (apod.media_type !== "image") {
    return null;
  }

  const source = "nasa";
  const date = apod.date;
  return {
    id: `${source}-${date}`,
    source,
    date,
    description: apod.explanation ?? "",
    pageUrl: "https://apod.nasa.gov/apod/",
    imageUrl: apod.url,
  };
}
