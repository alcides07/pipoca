import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import AutenticacaoService from "@/services/models/autenticacaoService";
import { useNavigate } from "react-router-dom";

const formSchema = z.object({
	username: z.string().min(2, {
		message: "Username must be at least 2 characters.",
	}),
	password: z.string().min(3, {
		message: "Password must be at least 3 characters.",
	}),
});

function FormLogin({ onLogin }: any) {
	const navigate = useNavigate();

	const form = useForm<z.infer<typeof formSchema>>({
		resolver: zodResolver(formSchema),
		defaultValues: {
			username: "",
			password: "",
		},
	});

	function onSubmit(values: z.infer<typeof formSchema>) {
		const data = {
			username: values.username,
			password: values.password,
		};
		AutenticacaoService.login(data)
			.then((response) => {
				if (response.status === 200) {
					localStorage.setItem(
						"access_token",
						response.data.access_token
					);
					navigate("/dashboard");
					onLogin();
				}
			})
			.catch((error) => {
				console.error("Login erro:", error);
			});
	}
	return (
		<Card className="w-full">
			<CardHeader>
				<CardTitle>Login</CardTitle>
				<CardDescription>
					Realize login para ter acesso ao sistema Pipoca!
				</CardDescription>
			</CardHeader>
			<CardContent>
				<Form {...form}>
					<form
						onSubmit={form.handleSubmit(onSubmit)}
						className="space-y-4">
						<FormField
							control={form.control}
							name="username"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Nome</FormLabel>
									<FormControl>
										<Input
											placeholder=""
											{...field}
											autoComplete="username"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="password"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Senha</FormLabel>
									<FormControl>
										<Input
											type="password"
											{...field}
											autoComplete="current-password"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>

						<Button type="submit" className="w-full my-8">
							Entrar
						</Button>
					</form>
				</Form>
			</CardContent>
		</Card>
	);
}

export default FormLogin;
