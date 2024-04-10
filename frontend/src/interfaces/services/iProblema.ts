export interface iProblema {
  nome: string;
  privado: boolean;
  nome_arquivo_entrada: string;
  nome_arquivo_saida: string;
  tempo_limite: number;
  memoria_limite: number;
  id?: number;
}
