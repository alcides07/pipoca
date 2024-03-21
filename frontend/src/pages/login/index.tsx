import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import FormLogin from "./components/formLogin";
import FormRegister from "./components/formRegister";
import { Toaster } from "@/components/ui/toaster";

function Login() {
  const [activeTab, setActiveTab] = useState("login");

  const handleRegisterSuccess = () => {
    setActiveTab("login");
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Tabs value={activeTab} className="w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="login" onClick={() => setActiveTab("login")}>
            Login
          </TabsTrigger>
          <TabsTrigger
            value="cadastro"
            onClick={() => setActiveTab("cadastro")}
          >
            Cadastro
          </TabsTrigger>
        </TabsList>
        <TabsContent value="login">
          <FormLogin />
        </TabsContent>
        <TabsContent value="cadastro">
          <FormRegister onSuccess={handleRegisterSuccess} />
        </TabsContent>
      </Tabs>
      <Toaster />
    </div>
  );
}

export default Login;
