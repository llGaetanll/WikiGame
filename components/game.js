import { useState, useEffect } from "react";
import Wiki from "../components/wiki";

const frame = { borderRadius: 5, margin: 10 };

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

const DEST = "Philosophy";

const Game = () => {
  // TODO: game wrapper component
  const [dest, setDest] = useState("Philosophy");
  const [scores, setScores] = useState({ player: 0, bot: 0 });

  const [player, setPlayer] = useState({
    name: null,
    page: null,
    parsedPage: null,
  });
  const [bot, setBot] = useState({
    name: null,
    page: null,
    parsedPage: null,
  });

  const setPage = async (pageName, setState) => {
    // proxy wikipedia page given the underscored pagename
    fetch(`/api/proxy?page=${pageName}`)
      .then((res) => res.json())
      .then(({ visualPage, parsedPage }) =>
        setState((s) => ({
          name: pageName,
          page: visualPage,
          parsedPage,
        }))
      )
      .catch((err) => err);
  };

  // bot makes a move
  const handleNextRound = async (playerNextPage) => {
    console.log("player clicked", playerNextPage);

    setPage(playerNextPage, setPlayer);
    setScores((s) => ({ ...s, player: s.player + 1 }));

    const botNextPage = await fetch("/bot/", {
      page: bot.parsedPage,
      dest,
    }).then((res) => res.text());
    setScores((s) => ({ ...s, bot: s.bot + 1 }));
  };

  // seet initial player page on load
  useEffect(() => {
    if (!player.name) setPage("United_States", setPlayer);
    if (!bot.name) setPage("United_Kingdom", setBot);
  });

  return (
    <div css={{ display: "flex", flexDirection: "column" }}>
      <div
        css={{ display: "flex", height: 30, padding: 25, background: "#ccc" }}
      >
        <span>human: {scores.player}</span>
        <span>bot: {scores.bot}</span>
      </div>
      <div
        css={{ display: "flex", flex: 1, width: "100%", background: "#f6f6f6" }}
      >
        <Wiki
          pageHTML={player.page}
          css={[frame, { marginLeft: 0 }]}
          clickCallback={handleNextRound}
        />
        <Wiki
          pageHTML={bot.page}
          css={[frame, { marginLeft: 0 }]}
          botControlled
        />
      </div>
    </div>
  );
};

export default Game;
