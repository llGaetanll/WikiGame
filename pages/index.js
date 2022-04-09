import Wiki from "../components/wiki";

const frame = { borderRadius: 5, margin: 10 };

const Index = () => {
  return (
    <div
      css={{ display: "flex", flex: 1, width: "100%", background: "#f6f6f6" }}
    >
      {/* <Wiki page="Meenakshi_Arora" css={frame} /> */}
      <Wiki page="Michael_Jackson" css={[frame, { marginLeft: 0 }]} />
      <Wiki page="United_Kingdom" css={[frame, { marginLeft: 0 }]} />
    </div>
  );
};

export default Index;
