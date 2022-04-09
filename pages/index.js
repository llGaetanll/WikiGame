import Wiki from "../components/wiki";

const frame = { borderRadius: 5, margin: 10 };

const Index = () => {
  return (
    <div css={{ display: "flex", flex: 1, background: "#f6f6f6" }}>
      <Wiki page="Meenakshi_Arora" css={frame} />
      <Wiki page="The_Great_Kai_%26_J._J." css={[frame, { marginLeft: 0 }]} />
    </div>
  );
};

export default Index;
