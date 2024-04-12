import axiosInstance from "../axiosInstance";

class ProblemaService {
  async getProblemas() {
    const response = await axiosInstance.get("/problemas/");
    return response.data;
  }
  async createProblema(data: any) {
    const response = await axiosInstance.post(`/problemas/`, data);
    return response;
  }
  async getProblemaById(id: number) {
    const response = await axiosInstance.get(`/problemas/${id}`);
    return response.data;
  }

  async updateProblema(id: number, data: any) {
    const response = await axiosInstance.put(`/problemas/${id}`, data);
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
