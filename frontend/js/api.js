const API_BASE_URL = 'http://localhost/api';

class ApiClient {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        return {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...options,
            headers: this.getAuthHeaders()
        };

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
                window.location.href = 'login.html';
                throw new Error('Unauthorized');
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Request failed');
            }

            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth
    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${this.baseUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        return await response.json();
    }

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getCurrentUser() {
        return this.request('/users/me');
    }

    // Transport
    async getTransport(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/transport/?${params}`);
    }

    async getTransportById(id) {
        return this.request(`/transport/${id}`);
    }

    async createTransport(data) {
        return this.request('/transport/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateTransport(id, data) {
        return this.request(`/transport/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteTransport(id) {
        return this.request(`/transport/${id}`, {
            method: 'DELETE'
        });
    }

    // Routes
    async getRoutes(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/routes/?${params}`);
    }

    async getRouteById(id) {
        return this.request(`/routes/${id}`);
    }

    async createRoute(data) {
        return this.request('/routes/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateRoute(id, data) {
        return this.request(`/routes/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteRoute(id) {
        return this.request(`/routes/${id}`, {
            method: 'DELETE'
        });
    }

    // Trips
    async getTrips(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/trips/?${params}`);
    }

    async getTripById(id) {
        return this.request(`/trips/${id}`);
    }

    async createTrip(data) {
        return this.request('/trips/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateTrip(id, data) {
        return this.request(`/trips/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteTrip(id) {
        return this.request(`/trips/${id}`, {
            method: 'DELETE'
        });
    }

    // Cargo
    async getCargo(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/cargo/?${params}`);
    }

    async getCargoById(id) {
        return this.request(`/cargo/${id}`);
    }

    async createCargo(data) {
        return this.request('/cargo/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateCargo(id, data) {
        return this.request(`/cargo/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteCargo(id) {
        return this.request(`/cargo/${id}`, {
            method: 'DELETE'
        });
    }

    // Users
    async getUsers() {
        return this.request('/users/');
    }

    async getUserById(id) {
        return this.request(`/users/${id}`);
    }

    async updateUser(id, data) {
        return this.request(`/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteUser(id) {
        return this.request(`/users/${id}`, {
            method: 'DELETE'
        });
    }

    // Utils
    async calculateCost(routeId, weight) {
        return this.request('/utils/calculate-cost', {
            method: 'POST',
            body: JSON.stringify({
                route_id: routeId,
                weight: parseFloat(weight)
            })
        });
    }

    async getStatistics() {
        return this.request('/utils/statistics');
    }
}

const api = new ApiClient();
