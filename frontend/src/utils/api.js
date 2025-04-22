// api.js

import axios from 'axios'

let BASE_URL = ' http://worldofqj.com:8000'

if (process.env.NODE_ENV == 'production') {
  console.log('Running in Production Mode')
  BASE_URL = 'http://worldofqj.com:8000'
} else {
  console.log("Running in Development Mode")
}

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Middleware - Request Interceptor
axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Middleware - Response Interceptor (Optional)
axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response.status == 401) {
      localStorage.clear()
      window.location.href = '/'
    }
    return Promise.reject(error);
  }
);

export const get = async (url, params) => {
  return await axiosInstance.get(url, { params })
    .then(response => response)
    .catch(error => {
      throw error
    })
}

export const post = async (url, data) => {
  return await axiosInstance.post(url, data)
    .then(response => response)
    .catch(error => {
      throw error
    })
}

export const put = async (url, data) => {
  return await axiosInstance.put(url, data)
    .then(response => response)
    .catch(error => {
      throw error
    })
}


export const patch = async (url, data) => {
  return await axiosInstance.patch(url, data)
    .then(response => response)
    .catch(error => {
      throw error
    })
}

export const _delete = async (url, data) => {
  return await axiosInstance.delete(url, data)
    .then(response => response)
    .catch(error => {
      throw error
    })
}