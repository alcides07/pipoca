import type { iVerificadorService } from "@/interfaces/services/iVerificador";
import axiosInstance from "../axiosInstance";

class VerificadorService {
  async criaVerificador(data: iVerificadorService) {
    const response = await axiosInstance.post(`/verificadores/`, data);
    return response;
  }
  async atualizaVerificador(id: number, data: iVerificadorService) {
    const response = await axiosInstance.put(`/verificadores/${id}`, data);
    return response.data;
  }
  async consultaTesteVerificador(id: number) {
    const response = await axiosInstance.get(`/verificadores/${id}/testes`);
    return response.data;
  }
}

export default new VerificadorService();
