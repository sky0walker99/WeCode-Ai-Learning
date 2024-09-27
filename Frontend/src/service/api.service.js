import axios from 'axios';
import handleApiError from '../utils/Errorhandler';

class apiService {
  postInputData(data) {
    return axios.post(`${process.env.REACT_APP_API_URL}/api/get_user_input`, data).catch(handleApiError);
  }
}
export default new apiService();
