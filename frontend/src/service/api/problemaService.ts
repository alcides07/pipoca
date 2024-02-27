import axiosInstance from "../axiosInstance";

class ProblemaService {
  async getProblemas() {
    const response = await axiosInstance.get("/problemas/");
    console.log(response.data);
    return response.data;
  }
  async getProblemaById(id: string) {
    const response = await axiosInstance.get(`/problemas/${id}`);
    return response.data;
  }
}

export default new ProblemaService();
