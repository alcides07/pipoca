import axiosInstance from "../axiosInstance";
import { iProblema } from "@/interfaces/services/iProblema";

class ProblemaService {
  async getProblemas() {
    const response = await axiosInstance.get("/problemas/");
    return response.data;
  }
  async cadastroProblema(data: iProblema) {
    const response = await axiosInstance.post(`/problemas/`, data);
    return response;
  }
  async getProblemaById(id: number) {
    const response = await axiosInstance.get(`/problemas/${id}/`);
    return response.data;
  }

  async updateProblema(id: number, data: any) {
    const response = await axiosInstance.put(`/problemas/${id}/`, data);
    return response.data;
  }

  async integridadeProblema(id: number) {
    const response = await axiosInstance.get(`/problemas/${id}/integridade/`);
    return response.data;
  }

  async declaracoesProblema(id: number) {
    const response = await axiosInstance.get(`/problemas/${id}/declaracoes/`);
    return response.data;
  }

  async verificadorProblema(id: number) {
    const response = await axiosInstance.get(`/problemas/${id}/verificadores/`);
    return response.data;
  }

  async testesExemplosProblema(id: number) {
    const response = await axiosInstance.get(
      `/problemas/${id}/testesExemplosExecutados/`
    );
    return response.data;
  }

  async respostasProblema(id: number) {
    const response = await axiosInstance.get(
      `/problemas/${id}/respostas/`
    );
    return response.data;
  }

  async uploadFile(formData: FormData) {
    const response = await axiosInstance.post(`/problemas/pacotes/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  }
}

export default new ProblemaService();
