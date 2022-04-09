import fetch from "isomorphic-unfetch";

const Wiki = ({ page, ...props }) => {
  fetch(`https://en.wikipedia.org/wiki/${page}`).then((res) =>
    console.log(res)
  );

  return <div {...props}>this is a wiki frame</div>;
};

export default Wiki;
