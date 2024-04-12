import { iDeclaracao } from "@/interfaces/models/iDeclaracao";
import axiosInstance from "../axiosInstance";

class DeclaracaoService {
  async getDeclaracao(id: number) {
    const response = await axiosInstance.get(`/declaracoes/${id}`);
    return response.data;
  }

  async atualizaDeclaracao(id: number, data: iDeclaracao) {
    const response = await axiosInstance.put(`/declaracoes/${id}`, data);
    return response.data;
  }

  async getDeclaracoes() {
    const response = await axiosInstance.get("/declaracoes/");
    return response.data;
  }
  async createDeclaracao(data: iDeclaracao) {
    const response = await axiosInstance.post(`/declaracoes/`, data);
    console.log(response);
    return response;
  }
}

export default new DeclaracaoService();
