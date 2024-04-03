import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import ListarProblemas from "./pages/Problemas/listarProblemas";
import Header from "./components/header";
import Login from "./pages/login";
import CadastroProblema from "./pages/Problemas/CadastroProblema";
import EditaProblema from "./pages/Problemas/CadastroProblema/tabsProblema";
import TabsProblema from "./pages/Problemas/CadastroProblema/tabsProblema";

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
          <Route path="/problemas" element={<ListarProblemas />} />
          <Route path="/problema/cadastro" element={<CadastroProblema />} />
          <Route path="/problema/:id" element={<TabsProblema />} />
          <Route path="/" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
