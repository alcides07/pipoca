import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/toaster";
import EditaProblema from "./EditaProblema";
import FormLogin from "../Login/components/formLogin";
import FormDeclaracao from "./CadastraProblema/components/formDeclaracao";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { iIntegridade } from "@/interfaces/models/iProblema";
import problemaService from "@/services/models/problemaService";
import EditaDeclaracao from "./EditaProblema/componentes/editaDeclaracao";
import EditaVerificador from "./EditaProblema/componentes/editaVerificador";
import VerificadorProblema from "../Problema/CadastraProblema/components/verificadorProblema";
import { toast } from "react-toastify";

function TabsProblema() {
  const { id } = useParams();
  const [integridade, setIntegridade] = useState<iIntegridade>();
  const [tabValor, setTabValor] = useState<string>(localStorage.getItem("aba"));
  const [verificadorImporte, setVerificadorImporte] = useState<boolean>(
    JSON.parse(localStorage.getItem("V") || "false")
  );
  useEffect(() => {
    integridadeProblem();
  }, []);

  useEffect(() => {
    if (verificadorImporte === true) {
      mensagemImporteVerificador();
      localStorage.removeItem("V");
      setVerificadorImporte(false);
    }
  }, [verificadorImporte]);

  useEffect(() => {
    if (tabValor !== null) {
      localStorage.setItem("aba", tabValor);
    }
  }, [tabValor]);

  async function integridadeProblem() {
    if (id !== undefined) {
      await problemaService
        .integridadeProblema(parseInt(id))
        .then((response) => {
          setIntegridade(response.data);
        });
    }
  }

  function mensagemImporteVerificador() {
    toast.success("Verificador importado com sucesso!", {
      autoClose: 5000,
      style: {
        border: "1px solid #07bc0c",
      },
    });
  }

  return (
    <div>
      <Tabs
        value={tabValor !== null ? tabValor : "problema"}
        onValueChange={setTabValor}
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="problema">Problema</TabsTrigger>
          <TabsTrigger value="declaracao">Declaração</TabsTrigger>
          <TabsTrigger value="arquivos">Arquivos</TabsTrigger>
          <TabsTrigger value="validador">Validador</TabsTrigger>
          <TabsTrigger value="verificador">Verificador</TabsTrigger>
          <TabsTrigger value="testes">Testes</TabsTrigger>
        </TabsList>
        <TabsContent value="problema">
          <EditaProblema />
        </TabsContent>
        <TabsContent value="declaracao">
          {integridade?.declaracoes ? (
            id ? (
              <EditaDeclaracao problemaId={parseInt(id)} />
            ) : null
          ) : id ? (
            <FormDeclaracao problemaId={parseInt(id)} />
          ) : null}
        </TabsContent>
        <TabsContent value="arquivos">
          <FormLogin />
        </TabsContent>
        <TabsContent value="validador">
          <FormLogin />
        </TabsContent>
        <TabsContent value="verificador">
          {integridade?.verificador ? (
            id ? (
              <EditaVerificador problemaId={parseInt(id)} />
            ) : null
          ) : id ? (
            <VerificadorProblema problemaId={parseInt(id)} />
          ) : null}
        </TabsContent>
        <TabsContent value="testes">
          <FormLogin />
        </TabsContent>
      </Tabs>
      <Toaster />
    </div>
  );
}

export default TabsProblema;
