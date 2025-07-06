import {PUBLIC_BACKEND_API_URL} from '$env/static/public';
import axios from 'axios';

export async function addAttachmentAPI(event, token) {
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
        
        let filename = response.data.data.filename
        console.log('Upload successful:', filename);
        return filename; 
        
    } catch (error) {
        console.error('Error uploading attachment:', error);
        return 500;
    }
}

export async function addIssueAPI(data, token){
    try {

        const response = await axios.post(`${PUBLIC_BACKEND_API_URL}/issue/add`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('Successful: ', response.data);
        return response.data; 
        
    } catch (error) {
        console.error('Error uploading attachment:', error);
        return 500;
    }
}

export async function updateIssueAPI(data, token){    
    try {

    const response = await axios.put(`${PUBLIC_BACKEND_API_URL}/issue/${data.issue_id}`, data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    console.log('Successful: ', response.data);
    return response.data; 
    
} catch (error) {
    console.error('Error uploading attachment:', error);
    return 500;
}}

export async function getAllIssuesAPI(token){
    try {

        const response = await axios.get(`${PUBLIC_BACKEND_API_URL}/issue/all`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('Successful: ', response.data);
        return response.data.data; 
        
    } catch (error) {
        console.error('Error uploading attachment:', error);
        return 500;
    }}

    export async function deleteIssueAPI(issueId, token){
        try {
    
            const response = await axios.delete(`${PUBLIC_BACKEND_API_URL}/issue/${issueId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            console.log('Successful: ', response.data);
            return response.data.code; 
            
        } catch (error) {
            console.error('Error uploading attachment:', error);
            return 500;
        }}

    export async function getUserRoleAPI(token){
        try {

            const response = await axios.get(`${PUBLIC_BACKEND_API_URL}/user/role`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            console.log('Successful: ', response.data);
            return response.data.data; 
            
        } catch (error) {
            console.error('Error uploading attachment:', error);
            return 500;
        }} 