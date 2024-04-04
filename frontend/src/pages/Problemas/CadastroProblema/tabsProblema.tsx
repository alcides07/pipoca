import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { Toaster } from "@/components/ui/toaster";
import FormLogin from "@/pages/login/components/formLogin";
import FormRegister from "@/pages/login/components/formRegister";
import FormCadastroTabs from "@/pages/Problemas/CadastroProblema/components/formCadastroTabs";
function TabsProblema() {
  console.log("Entrei aqui em TabsProblema");
  return (
    // <div className="px-28 h-[90vh]">
    // <div className="py-4">
    //   <p className="text-2xl font-bold">Cadastro de problema</p>
    // </div>
    <div>
      <Tabs defaultValue="problema" className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="problema">Problema</TabsTrigger>
          <TabsTrigger value="declaracao">Declaração</TabsTrigger>
          <TabsTrigger value="arquivos">Arquivos</TabsTrigger>
          <TabsTrigger value="validador">Validador</TabsTrigger>
          <TabsTrigger value="verificador">Verificador</TabsTrigger>
          <TabsTrigger value="testes">Testes</TabsTrigger>
        </TabsList>
        <TabsContent value="problema">
          <FormCadastroTabs />
        </TabsContent>
        <TabsContent value="declaracao">
          <FormLogin />
        </TabsContent>
        <TabsContent value="arquivos">
          <FormRegister />
        </TabsContent>
        <TabsContent value="validador">
          <FormRegister />
        </TabsContent>
        <TabsContent value="verificador">
          <FormLogin />
        </TabsContent>
        <TabsContent value="testes">
          <FormRegister />
        </TabsContent>
        {/* </div> */}
      </Tabs>
      <Toaster />
    </div>
  );
}

export default TabsProblema;