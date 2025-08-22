// script.js - Versão única, limpa e modular

document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const loading = document.getElementById('loading');
    const themeToggle = document.getElementById('theme-toggle');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const contactForm = document.getElementById('contact-form');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const codeLine = document.getElementById('code-line');
    const scrollProgress = document.getElementById('scroll-progress');

    // ==================== LOADING SCREEN ====================
    if (loading) {
        loading.style.opacity = '0';
        setTimeout(() => loading.style.display = 'none', 500);
    }

    // ==================== MODO ESCURO ====================
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function updateThemeIcon(theme) {
        const icon = themeToggle?.querySelector('i');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    // ==================== MOBILE MENU ====================
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('show');
        });
    }

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu) navMenu.classList.remove('show');
        });
    });

    // ==================== SMOOTH SCROLL ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // ==================== FORMULÁRIO ====================
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(contactForm);
            try {
                const res = await fetch('/contact', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                if (result.success) {
                    document.getElementById('success-modal').style.display = 'flex';
                    contactForm.reset();
                } else {
                    alert('Erro ao enviar. Tente novamente.');
                }
            } catch (err) {
                console.error(err);
                alert('Falha na conexão.');
            }
        });
    }

    function closeModal() {
        document.getElementById('success-modal').style.display = 'none';
    }

    // ==================== ANIMAÇÕES ====================
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.section-title, .hero-text, .about-text, .project-card, .skill-card, .timeline-item').forEach(el => {
        el.classList.add('hidden');
        observer.observe(el);
    });

    // ==================== CHATBOT ====================
    if (chatbotToggle && chatbotContainer && chatbotClose) {
        chatbotToggle.addEventListener('click', () => {
            chatbotContainer.style.display = 'block';
            chatbotToggle.style.display = 'none';
        });

        chatbotClose.addEventListener('click', () => {
            chatbotContainer.style.display = 'none';
            chatbotToggle.style.display = 'flex';
        });
    }

    if (chatbotSend && chatbotInput) {
        chatbotSend.addEventListener('click', sendMessage);
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    function sendMessage() {
        const text = chatbotInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        addMessage("Processando...", 'bot');

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            const loadingMsg = document.querySelector('.message.bot:last-child');
            if (loadingMsg) loadingMsg.remove();
            addMessage(data.response || "Desculpe, não consegui responder.", 'bot');
        })
        .catch(() => {
            const loadingMsg = document.querySelector('.message.bot:last-child');
            if (loadingMsg) loadingMsg.remove();
            addMessage("Erro ao conectar com o assistente.", 'bot');
        });

        chatbotInput.value = '';
    }

    function addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.className = `message ${sender}`;
        msg.textContent = text;
        chatbotMessages.appendChild(msg);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // ==================== TERMINAL ====================
    document.querySelector('.terminal-bar')?.addEventListener('click', () => {
        const terminal = document.querySelector('.terminal-text');
        const options = [
            "~$ whoami",
            "~$ echo 'Full Stack Developer'",
            "~$ ls projetos/",
            "~$ cat sobre.txt",
            "~$ node --version",
            "~$ python --version"
        ];
        if (terminal) {
            terminal.textContent = options[Math.floor(Math.random() * options.length)];
        }
    });

    // ==================== CÓDIGO ANIMADO ====================
    if (codeLine) {
        setTimeout(() => {
            codeLine.classList.add('visible');
        }, 1500);
    }

    // ==================== PROGRESSO DE SCROLL ====================
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        if (scrollProgress) {
            scrollProgress.style.width = scrollPercent + '%';
        }
    });
});

// No final do script.js
console.log("Carrossel:", document.getElementById('skills-carousel'));
console.log("Cards:", document.querySelectorAll('.skill-card').length);

