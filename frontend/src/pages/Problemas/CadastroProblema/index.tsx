// import { Card, CardContent } from "@/components/ui/card";
// import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// import FormLogin from "../login/components/formLogin";
// import FormRegister from "../login/components/formRegister";
// import { Toaster } from "@/components/ui/toaster";
import FormCadastro from "./components/formCadastro";

function CadastroProblema() {
  return (
    <div className="mx-28 my-5">
      {/* <div className="py-4">
        <p className="text-2xl font-bold">Cadastro de problema</p>
      </div>
      <Tabs className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="problema">Problema</TabsTrigger>
          <TabsTrigger value="declaracao">Declaração</TabsTrigger>
          <TabsTrigger value="arquivos">Arquivos</TabsTrigger>
          <TabsTrigger value="validador">Validador</TabsTrigger>
          <TabsTrigger value="validador">Verificador</TabsTrigger>
          <TabsTrigger value="testes">Testes</TabsTrigger>
        </TabsList>
        <Card className="h-[80vh] flex justify-center items-center my-5">
          <CardContent className="flex flex-col justify-center items-center">
            <div className="w-[50vw] flex justify-center">
              <TabsContent value="problema">
                <FormLogin />
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
              <TabsContent value="validador">
                <FormLogin />
              </TabsContent>
              <TabsContent value="testes">
                <FormRegister />
              </TabsContent>
            </div>
          </CardContent>
        </Card>
      </Tabs>
      <Toaster /> */}
      <FormCadastro />
    </div>
  );
}

export default CadastroProblema;
