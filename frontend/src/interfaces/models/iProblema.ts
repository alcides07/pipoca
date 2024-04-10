import { iTag } from "./iTag";
import { iTestes } from "./iTeste";
import { iDeclaracao } from "./iDeclaracao";

export interface iProblemas {
	metadata: iMetadataProblemas;
	data: iDataProblema[];
}

interface iMetadataProblemas {
	count: number;
	limit: number;
	offset: number;
	total: number;
	search_fields: string[];
}

export interface iDataProblema {
	nome: string;
	privado: boolean;
	nome_arquivo_entrada: string;
	nome_arquivo_saida: string;
	tempo_limite: number;
	memoria_limite: number;
	id: number;
	usuario: {
		username: string;
		id: number;
	};
	tags: iTag[];
	declaracoes: iDeclaracao[];
	criado_em: string;
	testes: iTestes[];
}
