import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import ListarProblemas from "./pages/Problemas/listarProblemas";
import Header from "./components/header";
import Login from "./pages/login";
import CadastroProblema from "./pages/Problemas/CadastroProblema";
import TabsProblema from "./pages/Problemas/CadastroProblema/tabsProblema";
import React, { useState, useEffect, useRef } from "react";
const linksHeader = [
  { nome: "Dashboard", link: "/" },
  { nome: "Problemas", link: "/problemas" },
  { nome: "Turmas", link: "#" },
  { nome: "Torneios", link: "#" },
];

function Container({ children }) {
  const ref = useRef(null);
  const [isOverflowing, setIsOverflowing] = useState(false);

  useEffect(() => {
    if (ref.current.scrollHeight > ref.current.clientHeight) {
      setIsOverflowing(true);
    }
  }, [children]);

  return (
    <div
      ref={ref}
      className={`my-8 px-28 
       ${
         isOverflowing
           ? "min-h-screen"
           : "h-[89vh] flex justify-center items-center"
       }
      `}
    >
      {children}
    </div>
  );
}

function RoutesWithHeader() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const location = useLocation();
  const showHeader = isLoggedIn || location.pathname !== "/";

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <>
      {showHeader && <Header options={linksHeader} />}
      <Container>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/problemas" element={<ListarProblemas />} />
          <Route path="/problema/cadastro" element={<CadastroProblema />} />
          <Route path="/problema/:id" element={<TabsProblema />} />
          <Route path="/" element={<Login onLogin={handleLogin} />} />
        </Routes>
      </Container>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <RoutesWithHeader />
    </BrowserRouter>
  );
}

export default App;
