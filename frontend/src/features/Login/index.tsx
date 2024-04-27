import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import FormLogin from "./components/formLogin";
import FormRegister from "./components/formRegister";
import { Toaster } from "@/components/ui/toaster";

function Login({ onLogin }: any) {
	const [activeTab, setActiveTab] = useState("login");

	const handleRegisterSuccess = () => {
		setActiveTab("login");
	};

	return (
		<div className="h-auto min-h-[93vh] w-full flex  justify-center  items-center">
			<Tabs value={activeTab} className="w-[400px] min-h-auto">
				<TabsList className="grid w-full grid-cols-2">
					<TabsTrigger
						value="login"
						onClick={() => setActiveTab("login")}>
						Login
					</TabsTrigger>
					<TabsTrigger
						value="cadastro"
						onClick={() => setActiveTab("cadastro")}>
						Cadastro
					</TabsTrigger>
				</TabsList>
				<TabsContent value="login">
					<FormLogin onLogin={onLogin} />
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
