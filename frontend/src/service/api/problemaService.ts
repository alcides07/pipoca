import axios from "axios";
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
	async uploadFile(formData: FormData) {
		const response = await axios.post(`/problemas/upload/`, formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		});
		return response.data;
	}
}

export default new ProblemaService();
