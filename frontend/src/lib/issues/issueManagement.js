import {PUBLIC_BACKEND_API_URL} from '$env/static/public';
import axios from 'axios';

export async function addAttachment(event, token) {
    try {
        const file = event.target?.files[0];
        
        const formData = new FormData();
        formData.append('attachment', file);
        
        const response = await axios.post(`${PUBLIC_BACKEND_API_URL}/attachment/upload`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data'
            }
        });
        
        console.log('Upload successful:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error uploading attachment:', error);
        throw error;
    }
}