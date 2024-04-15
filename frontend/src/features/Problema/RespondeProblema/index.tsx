import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
	ResizableHandle,
	ResizablePanel,
	ResizablePanelGroup,
} from "@/components/ui/resizable";
import problemaService from "@/services/models/problemaService";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/components/ui/use-toast";
import {
	Select,
	SelectContent,
	SelectGroup,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import linguagens from "../../../utils/linguagem";
import { iRespondeProblema } from "@/interfaces/services/iRespondeProblema";
import { Toaster } from "@/components/ui/toaster";
import { iDataProblema } from "@/interfaces/models/iProblema";
import { Badge } from "@/components/ui/badge";
import Loading from "@/components/loading";
import { iTestesExemplos } from "@/interfaces/models/iTeste";

import {
	Table,
	TableBody,
	TableCaption,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";

const FormSchema = z.object({
	linguagem: z.string().nonempty("Selecione uma linguagem de programação!"),
	resposta: z
		.string()
		.nonempty("Informe o seu código!")
		.refine(
			(val: string) => val.length >= 10,
			"A resposta deve ter pelo menos 10 caracteres!"
		),
});

interface RespondeProblemaProps {
	children?: React.ReactNode;
}

function RespondeProblema({ children }: RespondeProblemaProps) {
	const { id } = useParams();
	const [problema, setProblema] = useState<iDataProblema>();
	const [rows, setRows] = useState(1);
	const [isLoading, setIsLoading] = useState(false);
	const [testesExemplos, setTestesExemplos] = useState<iTestesExemplos[]>();
	const [loadingProblema, setLoadingProblema] = useState(true);
	const [loadingProblemaExemplos, setLoadingProblemaExemplos] =
		useState(true);

	const form = useForm<z.infer<typeof FormSchema>>({
		resolver: zodResolver(FormSchema),
		defaultValues: {
			linguagem: "",
			resposta: "",
		},
	});

	async function onSubmit(values: z.infer<typeof FormSchema>) {
		setIsLoading(true);
		const data: iRespondeProblema = {
			resposta: values.resposta,
			linguagem: values.linguagem,
			problema_id: id,
		};

		await problemaService
			.respondeProblema(data)
			.then((response) => {
				if (response.data.erro) {
					toast({
						title: "Erro.",
						description: response.data.erro,
						variant: "destructive",
						duration: 5000,
					});
				} else {
					toast({
						title: "Sucesso.",
						description: "Resposta correta!",
						variant: "success",
						duration: 5000,
					});
				}
			})
			.catch((error) => {
				toast({
					title: "Erro.",
					description: error.message,
					variant: "destructive",
					duration: 5000,
				});
			})
			.finally(() => {
				setIsLoading(false);
			});
	}

	useEffect(() => {
		obtemProblema();
	}, []);

	useEffect(() => {
		if (problema != undefined) obtemTestesExemplos();
	}, [problema]);

	async function obtemProblema() {
		setLoadingProblema(true);

		await problemaService.getProblemaById(id).then((response) => {
			setProblema(response.data);
		});
		setLoadingProblema(false);
	}

	async function obtemTestesExemplos() {
		setLoadingProblemaExemplos(true);
		await problemaService.testesExemplosProblema(id).then((response) => {
			console.log("testes:", response.data);
			setTestesExemplos(response.data);
		});
		setLoadingProblemaExemplos(false);
	}

	return (
		<div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
			<ResizablePanelGroup direction="vertical" className="min-h-[80vh]">
				<ResizablePanel defaultSize={8}>
					<ResizablePanelGroup direction="horizontal">
						<ResizablePanel
							defaultSize={30}
							className="m-1 flex justify-center items-center">
							<span className="text-xs font-bold flex justify-center">
								Memória Limite
							</span>
							<span className="p-3">|</span>
							<Badge className="py-0" variant="secondary">
								{problema?.memoria_limite} MB
							</Badge>
						</ResizablePanel>
						<ResizableHandle disabled className="bg-white" />
						<ResizablePanel
							defaultSize={30}
							className="m-1 flex justify-center items-center">
							<span className="text-xs font-bold flex justify-center">
								Tempo Limite
							</span>
							<span className="p-3">|</span>
							<Badge className=" py-0" variant="secondary">
								{problema?.tempo_limite} ms
							</Badge>
						</ResizablePanel>
						<ResizableHandle disabled className="bg-white" />
						<ResizablePanel
							defaultSize={40}
							className="m-1 px-0 h-full flex justify-center items-center">
							<span className="text-xs font-bold flex justify-center">
								Tags
							</span>
							<span className="p-3">|</span>
							<span className="">
								{problema?.tags?.map((tag) => (
									<Badge
										variant="secondary"
										key={tag.id}
										className="py-0 m-1">
										{tag?.nome}{" "}
									</Badge>
								))}
							</span>
						</ResizablePanel>
					</ResizablePanelGroup>
				</ResizablePanel>
				<ResizableHandle />
				<ResizablePanel defaultSize={92}>
					<ResizablePanelGroup
						direction="horizontal"
						className="min-h-[200px]">
						<ResizablePanel defaultSize={60}>
							{problema != undefined && problema != null ? (
								<ScrollArea className="h-full w-full">
									<div className="flex h-full w-full px-10">
										{problema &&
											problema.declaracoes[0] && (
												<div className="w-full">
													<h2 className="text-3xl font-bold my-5">
														{
															problema
																.declaracoes[0]
																.titulo
														}
													</h2>
													<Separator className="my-4" />

													<p className="pb-5 text-justify">
														{
															problema
																.declaracoes[0]
																.contextualizacao
														}
													</p>
													<div className="pb-5">
														<span className="text-ms font-bold">
															Entrada
														</span>
														<p>
															{
																problema
																	.declaracoes[0]
																	.formatacao_entrada
															}
														</p>
													</div>
													<div>
														<span className="text-ms font-bold">
															Saída
														</span>
														<p>
															{
																problema
																	.declaracoes[0]
																	.formatacao_saida
															}
														</p>
													</div>
													<Separator className="my-4" />
													{testesExemplos !=
													undefined ? (
														<Table className="border rounded mb-8">
															<TableHeader>
																<TableRow className="divide-y divide-slate-200">
																	<TableHead className="text-center">
																		Exemplos
																		de
																		Entrada
																	</TableHead>
																	<TableHead className="text-center">
																		Exemplos
																		de Saída
																	</TableHead>
																</TableRow>
															</TableHeader>
															<TableBody>
																{testesExemplos.map(
																	(
																		teste,
																		index
																	) => (
																		<TableRow
																			key={
																				index
																			}>
																			<TableCell className="border rounded">
																				{
																					teste.entrada
																				}
																			</TableCell>
																			<TableCell className="">
																				{
																					teste.saida
																				}
																			</TableCell>
																		</TableRow>
																	)
																)}
															</TableBody>
														</Table>
													) : (
														<Loading
															isLoading={
																loadingProblemaExemplos
															}
															className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
														/>
													)}
												</div>
											)}
									</div>
								</ScrollArea>
							) : (
								<Loading
									className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
									isLoading={loadingProblema}
									divHeight="h-full"
								/>
							)}
						</ResizablePanel>
						<ResizableHandle withHandle />
						<ResizablePanel defaultSize={40}>
							<ScrollArea className="h-full w-full">
								<div className="flex h-full justify-center p-6">
									<Form {...form}>
										<form
											onSubmit={form.handleSubmit(
												onSubmit
											)}
											className="w-full space-y-6">
											<FormField
												control={form.control}
												name="linguagem"
												render={({ field }) => (
													<FormItem>
														<FormControl>
															<Select
																onValueChange={
																	field.onChange
																}>
																<SelectTrigger className="w-full">
																	<SelectValue placeholder="Selecione uma linguagem" />
																</SelectTrigger>
																<SelectContent>
																	<SelectGroup>
																		{linguagens.map(
																			(
																				linguagem: string
																			) => (
																				<SelectItem
																					key={
																						linguagem
																					}
																					value={
																						linguagem
																					}>
																					{
																						linguagem
																					}
																				</SelectItem>
																			)
																		)}
																	</SelectGroup>
																</SelectContent>
																<FormMessage />
															</Select>
														</FormControl>
													</FormItem>
												)}
											/>
											<FormField
												control={form.control}
												name="resposta"
												render={({ field }) => (
													<FormItem>
														<FormControl>
															<Textarea
																placeholder="Informe seu código!"
																className="min-h-[17rem] text-ms"
																rows={rows}
																onInput={(
																	e: any
																) => {
																	setRows(
																		e.target
																			.scrollHeight /
																			20
																	);
																}}
																{...field}
															/>
														</FormControl>
														<FormMessage />
													</FormItem>
												)}
											/>
											<Button
												type="submit"
												className="w-full text-white"
												disabled={isLoading}>
												{isLoading ? (
													<Loading
														isLoading={isLoading}
													/>
												) : (
													"Enviar"
												)}
											</Button>
										</form>
									</Form>
								</div>
							</ScrollArea>
						</ResizablePanel>
					</ResizablePanelGroup>
				</ResizablePanel>
			</ResizablePanelGroup>
			<Toaster />
		</div>
	);
}

export default RespondeProblema;
