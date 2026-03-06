const isLocal = window.location.hostname === '127.0.0.1' ||
    window.location.hostname === 'localhost' ||
    window.location.hostname === '' ||
    window.location.protocol === 'file:';

const API_URL = isLocal
    ? 'http://127.0.0.1:5000/api'
    : 'https://your-backend-url.onrender.com/api'; // Replace with your actual Render URL after deployment

const API = {
    // Accepts: API.login({email, password, institution_id}) OR API.login(email, password, institution_id)
    async login(emailOrObj, password, institution_id) {
        try {
            let email;
            if (typeof emailOrObj === 'object') {
                email = emailOrObj.email;
                password = emailOrObj.password;
                institution_id = emailOrObj.institution_id;
            } else {
                email = emailOrObj;
            }
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, institution_id })
            });
            const result = await response.json();
            if (result.status === 'success' && result.user && !result.data) {
                result.data = result.user;
                // Store institution_id if returned
                if (result.user.institution_id) {
                    localStorage.setItem('institution_id', result.user.institution_id);
                }
            }
            return result;
        } catch (error) {
            return { status: 'error', message: 'Failed to connect to server. Make sure backend is running.' };
        }
    },

    async register(data) {
        try {
            // Ensure institution_id is in data
            if (!data.institution_id) {
                data.institution_id = localStorage.getItem('institution_id');
            }
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Registration failed' };
        }
    },

    async registerInstitution(data) {
        try {
            const response = await fetch(`${API_URL}/institutions/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Institution registration failed' };
        }
    },

    async submitFeedback(data) {
        try {
            if (!data.institution_id) {
                data.institution_id = localStorage.getItem('institution_id');
            }
            const response = await fetch(`${API_URL}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to submit feedback' };
        }
    },

    async getStats() {
        try {
            const instId = localStorage.getItem('institution_id');
            const response = await fetch(`${API_URL}/admin/stats?institution_id=${instId}`);
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to fetch stats' };
        }
    },

    async respondToFeedback(id, response) {
        try {
            const res = await fetch(`${API_URL}/admin/response`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, response })
            });
            return await res.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to save response' };
        }
    },

    // --- Faculty Management ---
    async getFaculties() {
        try {
            const instId = localStorage.getItem('institution_id');
            const response = await fetch(`${API_URL}/faculties?institution_id=${instId}`);
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to fetch faculties' };
        }
    },
    async addFaculty(name) {
        try {
            const instId = localStorage.getItem('institution_id');
            const response = await fetch(`${API_URL}/faculties`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, institution_id: parseInt(instId) })
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to add faculty' };
        }
    },
    async updateFaculty(id, name) {
        try {
            const response = await fetch(`${API_URL}/faculties/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to update faculty' };
        }
    },
    async deleteFaculty(id) {
        try {
            const response = await fetch(`${API_URL}/faculties/${id}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to delete faculty' };
        }
    },

    // --- Subject Management ---
    async getSubjects() {
        try {
            const instId = localStorage.getItem('institution_id');
            const response = await fetch(`${API_URL}/subjects?institution_id=${instId}`);
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to fetch subjects' };
        }
    },
    async addSubject(name) {
        try {
            const instId = localStorage.getItem('institution_id');
            const response = await fetch(`${API_URL}/subjects`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, institution_id: parseInt(instId) })
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to add subject' };
        }
    },
    async updateSubject(id, name) {
        try {
            const response = await fetch(`${API_URL}/subjects/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to update subject' };
        }
    },
    async deleteSubject(id) {
        try {
            const response = await fetch(`${API_URL}/subjects/${id}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            return { status: 'error', message: 'Failed to delete subject' };
        }
    }
};
