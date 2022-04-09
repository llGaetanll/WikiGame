import { useState, useRef, useEffect } from "react";
import fetch from "isomorphic-unfetch";
import cheerio from "cheerio";

import CircularProgress from "@mui/material/CircularProgress";

const parsePage = (html) => {
  const $ = cheerio.load(html);

  $("a").each((i, el) => {
    // console.log(el);
    const e = $(el);

    const href = e.attr("href");
    const title = e.attr("title");

    if (!/(\/wiki\/\w+)|(^#\w+)/.test(href)) {
      // if the link doesn't go to wikipedia, replace it with a b tag
      e.replaceWith($("<b>" + e.html() + "</b>"));
    } else {
      // if it does go to wikipedia, change the link slightly
      e.attr("href", title);
    }
  });

  return $.html();
};

const Wiki = ({ page, ...props }) => {
  const [pageName, setPageName] = useState(page);
  const [pageHTML, setPage] = useState(null);

  const ref = useRef(null);

  useEffect(() => {
    // fetch(`https://en.wikipedia.org/wiki/${page}`).then((res) =>
    fetch(`/api/proxy?page=${pageName}`)
      .then((res) => res.json())
      .then(({ visualPage, parsedPage }) => {
        setPage(parsePage(visualPage));
      })
      .catch((err) => err);
  }, [pageName]);

  useEffect(() => {
    if (pageHTML && ref.current) {
      const as = [...ref.current.querySelectorAll("a")];

      as.forEach((a) => {
        a.addEventListener("click", (e) => {
          e.preventDefault();

          setPageName(a.title.replace(/ /g, "_"));

          return false;
        });
      });
    }
  }, [pageHTML]);

  if (!pageHTML)
    return (
      <div
        css={{
          display: "flex",
          flex: 1,
          overflow: "auto",
          background: "white",
          boxSizing: "border-box",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CircularProgress />
      </div>
    );

  return (
    <div
      ref={ref}
      css={{
        flex: 1,
        overflow: "auto",
        background: "white",
        boxSizing: "border-box",
      }}
      {...props}
      dangerouslySetInnerHTML={{ __html: pageHTML }}
    />
  );
};

export default Wiki;
