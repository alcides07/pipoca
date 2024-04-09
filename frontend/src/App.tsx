import { BrowserRouter } from "react-router-dom";
import React from "react";
import Rotas from "./routes";

function App() {
  return (
    <BrowserRouter>
      <Rotas />
    </BrowserRouter>
  );
}

export default App;
