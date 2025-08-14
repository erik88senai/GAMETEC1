// Game Tec Edition Modern JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modern features
    initializeModernFeatures();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add modern visual effects
    addModernEffects();
    
    // Initialize form validations with modern styling
    initializeFormValidation();
    
    // Add particle background
    createParticleBackground();
    
    // Initialize smooth animations
    initializeAnimations();
    
    // Auto-refresh rankings every 30 seconds
    setInterval(function() {
        if (!document.activeElement || document.activeElement.tagName !== 'INPUT') {
            refreshAllRankings();
        }
    }, 30000);
    
    // Performance optimization
    optimizePerformance();
});

function initializeModernFeatures() {
    // Add modern classes to elements
    document.querySelectorAll('.card').forEach((card, index) => {
        card.classList.add('fade-in-scale');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add hover effects to interactive elements
    document.querySelectorAll('.btn, .nav-link, .form-control').forEach(element => {
        element.classList.add('hover-lift');
    });
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            boundary: 'viewport',
            customClass: 'modern-tooltip'
        });
    });
}

function createParticleBackground() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-bg';
    document.body.appendChild(particleContainer);
    
    // Create floating particles
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            createParticle(particleContainer);
        }, Math.random() * 5000);
    }
    
    // Continuously create new particles
    setInterval(() => {
        if (particleContainer.children.length < 20) {
            createParticle(particleContainer);
        }
    }, 2000);
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    const size = Math.random() * 4 + 2;
    const left = Math.random() * 100;
    const animationDuration = Math.random() * 10 + 15;
    
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${left}%`;
    particle.style.animationDuration = `${animationDuration}s`;
    particle.style.animationDelay = `${Math.random() * 5}s`;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.remove();
        }
    }, animationDuration * 1000);
}

function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-in-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements for animation
    document.querySelectorAll('.card, .table-responsive').forEach(el => {
        observer.observe(el);
    });
}

// Add modern visual effects to gaming elements
function addModernEffects() {
    const title = document.querySelector('.display-4');
    if (title) {
        title.classList.add('glow', 'gradient-text');
    }
    
    // Add enhanced effects to top 3 ranking positions
    document.querySelectorAll('.badge.bg-warning, .badge.bg-secondary, .badge.bg-info').forEach(badge => {
        if (badge.textContent.includes('🥇')) {
            badge.classList.add('trophy-gold');
        } else if (badge.textContent.includes('🥈')) {
            badge.classList.add('trophy-silver');
        } else if (badge.textContent.includes('🥉')) {
            badge.classList.add('trophy-bronze');
        }
    });
    
    // Add modern glow to navigation
    const navbar = document.querySelector('.navbar-brand');
    if (navbar) {
        navbar.classList.add('float');
    }
    
    // Add glass effect to cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('glass-effect');
    });
}

function optimizePerformance() {
    // Preload critical resources
    const criticalImages = document.querySelectorAll('img[data-src]');
    criticalImages.forEach(img => {
        img.src = img.dataset.src;
    });
    
    // Optimize animations for performance
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
        document.body.classList.add('reduced-motion');
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredInputs = form.querySelectorAll('input[required], select[required]');
    
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('input-error');
            isValid = false;
        } else {
            input.classList.remove('input-error');
            input.classList.add('input-success');
        }
    });
    
    return isValid;
}

// Enhanced delete student function
function deleteStudent(modalidade) {
    const tabPane = document.querySelector(`#${modalidade.replace(' ', '_')}-pane`);
    const form = tabPane.querySelector('form[action*="add_points"]');
    const selectElement = form.querySelector('select[name="aluno"]');
    const aluno = selectElement.value;
    
    if (!aluno) {
        showAlert('Selecione um aluno para excluir.', 'warning');
        return;
    }
    
    // Update modal content
    document.getElementById('deleteModalidade').value = modalidade;
    document.getElementById('deleteAluno').value = aluno;
    document.querySelector('#deleteModal .modal-body p').textContent = 
        `Tem certeza que deseja excluir o aluno "${aluno}" da modalidade "${modalidade}"?`;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

function confirmDelete() {
    const form = document.getElementById('deleteForm');
    const submitButton = document.querySelector('#deleteModal .btn-danger');
    
    // Add loading state
    const originalText = submitButton.textContent;
    submitButton.innerHTML = '<span class="loading me-2"></span>Excluindo...';
    submitButton.disabled = true;
    
    form.submit();
}

// Refresh rankings function
function refreshRanking(modalidade) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    // Add loading state
    button.innerHTML = '<span class="loading me-2"></span>Atualizando...';
    button.disabled = true;
    
    // Simulate loading time and refresh
    setTimeout(() => {
        location.reload();
    }, 1000);
}

function refreshAllRankings() {
    // This could be enhanced with AJAX calls to update rankings without full page reload
    // For now, we'll just refresh the page if there are any changes
    const currentTime = new Date().getTime();
    const lastRefresh = localStorage.getItem('lastRefresh');
    
    if (!lastRefresh || currentTime - lastRefresh > 60000) {
        localStorage.setItem('lastRefresh', currentTime);
        // Could implement AJAX refresh here
    }
}

// Update student select dynamically
function updateStudentSelect(selectElement, modalidade) {
    // This function could be enhanced to update student list in real-time
    // For now, it serves as a placeholder for future enhancements
    
    // Add visual feedback when student is selected
    if (selectElement.value) {
        selectElement.classList.add('input-success');
    } else {
        selectElement.classList.remove('input-success');
    }
}

// Show custom alerts
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Handle file upload preview
document.addEventListener('change', function(e) {
    if (e.target.type === 'file') {
        const fileInput = e.target;
        const fileName = fileInput.files[0]?.name || '';
        
        if (fileName) {
            const feedback = document.createElement('small');
            feedback.className = 'form-text text-success';
            feedback.textContent = `Arquivo selecionado: ${fileName}`;
            
            // Remove previous feedback
            const existingFeedback = fileInput.parentNode.querySelector('.form-text.text-success');
            if (existingFeedback) {
                existingFeedback.remove();
            }
            
            fileInput.parentNode.appendChild(feedback);
        }
    }
});

// Handle criteria checkbox changes with animations
document.addEventListener('change', function(e) {
    if (e.target.type === 'checkbox' && e.target.name === 'criterios') {
        const criterio = e.target.value;
        const form = e.target.closest('form');
        const pointsInput = form.querySelector(`input[name="points_${criterio}"]`);
        
        if (pointsInput) {
            if (e.target.checked) {
                pointsInput.style.display = 'block';
                pointsInput.style.animation = 'slideDown 0.3s ease-out';
                pointsInput.required = true;
                setTimeout(() => pointsInput.focus(), 300);
            } else {
                pointsInput.style.animation = 'slideUp 0.3s ease-out';
                pointsInput.required = false;
                pointsInput.value = '';
                setTimeout(() => {
                    pointsInput.style.display = 'none';
                }, 300);
            }
        }
        
        // Add visual feedback to the checkbox container
        const checkContainer = e.target.closest('.form-check');
        if (e.target.checked) {
            checkContainer.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
        } else {
            checkContainer.style.backgroundColor = 'transparent';
        }
    }
});

// Add CSS animations for slide effects
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R to refresh current ranking
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        const activeTab = document.querySelector('.nav-link.active');
        if (activeTab) {
            const modalidade = activeTab.textContent.trim().replace('🎮 ', '').replace('🏆 ', '');
            refreshRanking(modalidade);
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            modal.hide();
        }
    }
});

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Performance monitoring
let pageLoadTime = performance.now();
window.addEventListener('load', function() {
    const loadTime = performance.now() - pageLoadTime;
    console.log(`Game Tec Edition loaded in ${loadTime.toFixed(2)}ms`);
});
