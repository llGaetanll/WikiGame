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
    // proxy wikipedia page given the underscored pagename
    fetch(`/api/proxy?page=${pageName}`)
      .then((res) => res.json())
      .then(({ visualPage, parsedPage }) => {
        setPage(parsePage(visualPage));
      })
      .catch((err) => err);
  }, [pageName]);

  // when the pagehtml changes, add an onclick event to all <a></a>
  // tags as to not let them redirect us to the real wikipedia
  useEffect(() => {
    if (pageHTML && ref.current) {
      // make an array copy of all links on the page
      const as = [...ref.current.querySelectorAll("a")];

      as.forEach((a) => {
        // add event listener to prevent redirect
        a.addEventListener("click", (e) => {
          e.preventDefault();

          // here we can access state!
          setPageName(a.title.replace(/ /g, "_"));

          // return false;
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
