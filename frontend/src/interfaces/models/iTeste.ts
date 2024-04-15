export interface iTestes {
  numero: number;
  tipo: string;
  exemplo: boolean;
  entrada: string;
  descrição: string | null;
  problema_id: number;
  id: number;
}

export interface iTestesExemplos {
  entrada: string;
  saida: string;
}
