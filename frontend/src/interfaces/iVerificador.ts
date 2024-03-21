export interface iVerificador {
  nome: string;
  linguagem: string;
  id: number;
  problema_id: number;
  testes: iTestesVerificador[];
}

interface iTestesVerificador {
  numero: number;
  veredito: string;
  id: number;
  verificador_id: number;
}
