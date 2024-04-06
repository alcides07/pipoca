import { iTag } from "./iTag";
import { iTestes } from "./iTeste";
import { iValidador } from "./iValidador";
import { iVerificador } from "./iVerificador";
import { iDeclaracoesProblema } from "./iDeclaracao";

export interface iProblemas {
  metadata: iMetadataProblemas;
  data: iDataProblema[];
}

interface iMetadataProblemas {
  count: number;
  limit: number;
  offset: number;
  search_fields: string[];
  total: number;
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
  declaracoes: iDeclaracoesProblema[];
  criado_em: string;
  arquivos: iArquivosProblema[];
  validador: iValidador;
  verificador: iVerificador;
  testes: iTestes[];
}

interface iArquivosProblema {
  nome: string;
  secao: string;
  status: string;
  id: number;
  problema_id: number;
}
