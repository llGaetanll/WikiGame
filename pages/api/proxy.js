import fetch from "isomorphic-unfetch";
import cheerio from "cheerio";
import fs from "fs";

const HEADERS = new Headers();

// need cookie to load page content
HEADERS.append(
  "Cookie",
  "WMF-Last-Access=09-Apr-2022; WMF-Last-Access-Global=09-Apr-2022; GeoIP=US:NY:New_York:40.72:-74.00:v4"
);

// list of elements to get rid of before flattening the page
const clean = [
  'a[id="top"]',
  'a[class="mw-selflink selflink"]',
  'a[class="image"]',
  'a[class="internal"]',
  "sup",
];

// links patterns to remove
const rem_links = [
  /(\/wiki\/File:\w+)/,
  /(\/wiki\/Special:\w+)/,
  /(\/wiki\/Template:\w+)/,
  /(\/wiki\/Category:\w+)/,
  /(\/wiki\/Portal:\w+)/,
  /(\/wiki\/Template_talk:\w+)/,
  /(\/wiki\/Help:\w+)/,
  /(\/wiki\/Wikipedia:\w+)/,
  /(^#\w+)/,
];

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
  const content = $("div#content");
  const visualPage = content.html();

  // clean up processing page

  // remove all the crap
  for (const c of clean) $(`div#content ${c}`).remove();

  // format every link
  $("div#content a").each((_, a) => {
    const href = $(a)
      .attr("href")
      .replace(/\/wiki\//g, "");
    const text = $(a)
      .text()
      .replace(/[\,\.\:\!\?]/g, "");

    // remove all the crap links
    if (rem_links.some((rx) => rx.test(href)) || !/^\/wiki\/\w+/.test(href))
      $(a).remove();
    else {
      $(a).replaceWith($("<a>" + `{{${text}|${href}}}` + "</a>"));
    }
  });

  const parsedPage = $("div#content")
    .text()
    .replace(/ {2,}|\t+|\n+/g, " ")
    .trim();
  // const parsedPageHTML = $("div#content").html();

  // fs.writeFileSync(`./CleanPages/${req.query.page}.txt`, parsedPage);

  res.status(200).json({ visualPage, parsedPage });
}
