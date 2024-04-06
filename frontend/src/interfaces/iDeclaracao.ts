export interface iDeclaracoesProblema {
  titulo: string;
  idioma: string;
  id: number;
  problema_id: number;
}

export interface iDeclaracao {
  titulo: string;
  idioma: string;
  contextualizacao: string;
  formatacao_entrada: string;
  formatacao_saida: string;
  observacao: string;
  tutorial: string;
  id?: number;
  problema_id: number;
}
