import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import Header from "./components/header";
import Login from "./pages/login";
import Listar from "./pages/Problema/Listar";
import Responder from "./pages/Problema/Responder";

const linksHeader = [
  { nome: "Dashboard", link: "/" },
  { nome: "Problemas", link: "/problemas" },
  { nome: "Turmas", link: "#" },
  { nome: "Torneios", link: "#" },
];

function App() {
  return (
    <>
      <BrowserRouter>
        <Header options={linksHeader} />
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/problemas" element={<Listar />} />
          <Route path="/problemas" element={<Responder />} />
          <Route path="/problema/:id/responde" element={<Responder />} />
          <Route path="/" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
