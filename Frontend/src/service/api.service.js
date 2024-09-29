import axios from 'axios';
import handleApiError from '../utils/Errorhandler';

class apiService {
  postInputData(data) {
    return axios.post(`http://127.0.0.1:5000/api/get_user_input`, data).catch(handleApiError);
  }

  getChatHistory(){
    return axios.get(`http://127.0.0.1:5000/api/chat_history`).catch(handleApiError);
  }
}
export default new apiService();
