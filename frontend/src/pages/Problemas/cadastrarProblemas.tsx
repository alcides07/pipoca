import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import FormLogin from "../login/components/formLogin";
import FormRegister from "../login/components/formRegister";
import { Toaster } from "@/components/ui/toaster";

function CadastrarProblemas() {
  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Cadastro de problema</p>
      </div>
      <Tabs className="w-full">
        <TabsList className="grid w-full grid-cols-8">
          <TabsTrigger value="login">Login</TabsTrigger>
          <TabsTrigger value="login1">Login1</TabsTrigger>
          <TabsTrigger value="login2">Login2</TabsTrigger>
          <TabsTrigger value="login3">Login3</TabsTrigger>
          <TabsTrigger value="login4">Login4</TabsTrigger>
          <TabsTrigger value="login5">Login5</TabsTrigger>
          <TabsTrigger value="login6">Login6</TabsTrigger>
          <TabsTrigger value="login7">Login7</TabsTrigger>
        </TabsList>
        <Card className="h-[80vh] flex justify-center items-center my-5">
          <CardContent className="flex flex-col justify-center items-center">
            <div className="w-[50vw] flex justify-center">
              <TabsContent value="login">
                <FormLogin />
              </TabsContent>
              <TabsContent value="login1">
                <FormLogin />
              </TabsContent>
              <TabsContent value="login2">
                <FormRegister />
              </TabsContent>
              <TabsContent value="Login3">
                <FormRegister />
              </TabsContent>
              <TabsContent value="login4">
                <FormLogin />
              </TabsContent>
              <TabsContent value="login5">
                <FormRegister />
              </TabsContent>
              <TabsContent value="Login6">
                <FormRegister />
              </TabsContent>
              <TabsContent value="Login7">
                <FormRegister />
              </TabsContent>
            </div>
          </CardContent>
        </Card>
      </Tabs>
      <Toaster />
    </div>
  );
}

export default CadastrarProblemas;
