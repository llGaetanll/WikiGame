import fetch from "isomorphic-unfetch";
import cheerio from "cheerio";

const HEADERS = new Headers();

// need cookie to load page content
HEADERS.append(
  "Cookie",
  "WMF-Last-Access=09-Apr-2022; WMF-Last-Access-Global=09-Apr-2022; GeoIP=US:NY:New_York:40.72:-74.00:v4"
);

export default async function handler(req, res) {
  console.log(req.query);

  const text = await fetch(`https://en.wikipedia.org/wiki/${req.query.page}`, {
    method: "GET",
    headers: HEADERS,
    redirect: "follow",
  })
    .then((res) => res.text())
    .catch((err) => console.error(err));

  // console.log(text);
  const $ = cheerio.load(text);
  const content = $("div#content").html();

  // console.log(content);

  res.status(200).json({ page: content });
}
