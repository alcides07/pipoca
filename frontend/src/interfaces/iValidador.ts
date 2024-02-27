export interface iValidador {
  nome: string;
  linguagem: string;
  problema_id: number;
  id: number;
  testes: iTestesValidador[];
}

interface iTestesValidador {
  numero: number;
  veredito: string;
  validador_id: number;
  id: number;
}
