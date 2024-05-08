import { iVerificador } from "@/interfaces/services/iVerificador";
import axiosInstance from "../axiosInstance";

class VerificadorService {
  async criaVerificador(data: iVerificador) {
    const response = await axiosInstance.post(`/verificadores/`, data);
    return response;
  }
  async consultaTesteVerificador(id: number) {
    const response = await axiosInstance.get(`/verificadores/${id}/testes`);
    return response.data;
  }
}

export default new VerificadorService();
