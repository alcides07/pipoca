import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import ListarProblema from "./pages/listarProblema";
import Header from "./components/header";
import Login from "./pages/login";

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
          <Route path="/" element={<Dashboard />} />
          <Route path="/problemas" element={<ListarProblema />} />
          <Route path="/Login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
