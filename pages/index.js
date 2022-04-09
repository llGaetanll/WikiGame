import Wiki from "../components/wiki";

const Index = () => {
  return (
    <div css={{ display: "flex", flex: 1 }}>
      <Wiki page="Philosophy" css={{ flex: 1 }} />
      {/* <Wiki page="Philosophy" css={{ flex: 1 }} /> */}
    </div>
  );
};

export default Index;
