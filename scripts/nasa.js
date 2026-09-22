export default function nasa() {
  return fetch("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    .then((r) => r.json())
    .then((apod) => [
      {
        source: "NASA",
        description: apod.title ?? apod.explanation ?? "",
        pageUrl: "https://apod.nasa.gov/",
        imageUrl: apod.hdurl ?? apod.url,
      },
    ])
    .catch(() => []);
}
