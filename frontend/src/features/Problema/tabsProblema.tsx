import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/toaster";
import EditaProblema from "./EditaProblema";
import FormLogin from "../Login/components/formLogin";
import FormDeclaracao from "./CadastraProblema/components/formDeclaracao";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { iIntegridade } from "@/interfaces/models/iProblema";
import problemaService from "@/services/models/problemaService";

function TabsProblema() {
	const { id } = useParams();
	const [integridade, setIntegridade] = useState<iIntegridade>();

	console.log("id", id);

	useEffect(() => {
		integridadeProblem();
	}, [id]);

	async function integridadeProblem() {
		await problemaService.getProblemas().then((response) => {
			console.log("response.data", response.data);

			setIntegridade(response.data);
			console.log(response);
		});
	}

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
					<FormDeclaracao problemaId={parseInt(id)} />
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
