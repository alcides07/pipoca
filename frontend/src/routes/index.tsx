import { Routes, Route, useLocation } from "react-router-dom";
import Dashboard from "@/features/Dashboard";
import Header from "@/components/header";
import Login from "@/features/Login";
import Problema from "@/features/Problema";
import CadastraProblema from "@/features/Problema/CadastraProblema";
import RespondeProblema from "@/features/Problema/RespondeProblema";
import EditaProblema from "@/features/Problema/EditaProblema";
import TabsProblema from "@/features/Problema/tabsProblema.tsx";
import Conteiner from "../components/conteiner";
import { useState } from "react";
import ResultadoProblema from "@/features/Problema/RespondeProblema/components/resultadoResposta";

const linksHeader = [
  { nome: "Dashboard", link: "#" },
  { nome: "Problemas", link: "/problemas" },
  { nome: "Turmas", link: "#" },
  { nome: "Torneios", link: "#" },
];

function Rotas() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const location = useLocation();
  const showHeader = isLoggedIn || location.pathname !== "/";

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <>
      {showHeader && <Header options={linksHeader} />}
      <Conteiner>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/problemas" element={<Problema />} />
          <Route path="/problema/cadastro" element={<CadastraProblema />} />
          <Route path="/problema/:id" element={<TabsProblema />} />
          <Route path="/problema/:id/responde" element={<RespondeProblema />} />
          <Route
            path="/problema/:id/responde/resultados"
            element={<ResultadoProblema />}
          />
          <Route path="/problema/editar/:id" element={<EditaProblema />} />
          <Route path="/" element={<Login onLogin={handleLogin} />} />
        </Routes>
      </Conteiner>
    </>
  );
}

export default Rotas;
