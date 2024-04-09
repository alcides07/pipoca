import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/toaster";
import EditaProblema from "./EditaProblema";
import FormLogin from "../Login/components/formLogin";

function TabsProblema() {
  return (
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
          <EditaProblema />
        </TabsContent>
        <TabsContent value="declaracao">
          <FormLogin />
        </TabsContent>
        <TabsContent value="arquivos">
          <FormLogin />
        </TabsContent>
        <TabsContent value="validador">
          <FormLogin />
        </TabsContent>
        <TabsContent value="verificador">
          <FormLogin />
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
