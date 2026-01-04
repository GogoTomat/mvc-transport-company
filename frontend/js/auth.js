// Authentication helpers
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPage = window.location.pathname.split('/').pop();
    
    if (!token && currentPage !== 'login.html' && currentPage !== '') {
        window.location.href = 'login.html';
        return false;
    }
    
    if (token && currentPage === 'login.html') {
        window.location.href = 'index.html';
        return false;
    }
    
    return true;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function isAdmin() {
    const user = getCurrentUser();
    return user && user.role === 'admin';
}

async function loadUserInfo() {
    try {
        const user = await api.getCurrentUser();
        localStorage.setItem('user', JSON.stringify(user));
        updateUserDisplay(user);
    } catch (error) {
        console.error('Failed to load user info:', error);
        logout();
    }
}

function updateUserDisplay(user) {
    const userNameElement = document.getElementById('userName');
    const userRoleElement = document.getElementById('userRole');
    
    if (userNameElement) {
        userNameElement.textContent = user.username;
    }
    
    if (userRoleElement) {
        const roleNames = {
            'admin': 'Администратор',
            'manager': 'Менеджер',
            'dispatcher': 'Диспетчер'
        };
        userRoleElement.textContent = roleNames[user.role] || user.role;
    }
    
    // Hide admin links if not admin
    if (!isAdmin()) {
        const adminLinks = document.querySelectorAll('.admin-only');
        adminLinks.forEach(link => link.style.display = 'none');
    }
}

// Set active navigation link
function setActiveNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (checkAuth()) {
        const user = getCurrentUser();
        if (user) {
            updateUserDisplay(user);
        } else {
            loadUserInfo();
        }
        setActiveNav();
    }
});
