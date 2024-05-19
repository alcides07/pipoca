export interface iVerificador {
  nome: string;
  linguagem: string;
  corpo: string;
  id: number;
  problema_id: string;
  testes: iTesteVerificador[];
}

export interface iTesteVerificador {
  numero: number;
  veredito: string;
  entrada: string;
  id: number;
  verificador_id: number;
}
