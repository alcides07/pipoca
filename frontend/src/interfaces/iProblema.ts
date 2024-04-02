import { iTag } from "./iTag";

interface Declaracoes {
  titulo: string;
  idioma: string;
  contextualizacao: string;
  formatacao_entrada: string;
  formatacao_saida: string;
  observacao: string;
  tutorial: string;
  id: number;
  problema_id: number;
}

export interface iProblema {
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
  criado_em: string;
  declaracoes: Declaracoes[];
}
