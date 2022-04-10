import { useRef, useEffect } from "react";

import CircularProgress from "@mui/material/CircularProgress";

const Wiki = ({ pageHTML, botControlled, clickCallback, ...props }) => {
  const ref = useRef(null);

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

          // callback
          !botControlled && clickCallback(a.title);
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
