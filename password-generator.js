class PasswordGenerator {
    constructor() {
        this.lengthSlider = document.getElementById('length');
        this.lengthValue = document.getElementById('lengthValue');
        this.uppercaseCheck = document.getElementById('uppercase');
        this.lowercaseCheck = document.getElementById('lowercase');
        this.numbersCheck = document.getElementById('numbers');
        this.symbolsCheck = document.getElementById('symbols');
        this.generateBtn = document.getElementById('generateBtn');
        this.passwordField = document.getElementById('generatedPassword');
        this.copyBtn = document.getElementById('copyBtn');
        this.strengthBar = document.getElementById('strengthBar');
        this.strengthText = document.getElementById('strengthText');
        
        this.characters = {
            uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            lowercase: 'abcdefghijklmnopqrstuvwxyz',
            numbers: '0123456789',
            symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
        };
        
        this.init();
    }
    
    init() {
        this.lengthSlider.addEventListener('input', () => this.updateLength());
        this.generateBtn.addEventListener('click', () => this.generatePassword());
        this.copyBtn.addEventListener('click', () => this.copyPassword());
        
        // Generate initial password
        this.generatePassword();
    }
    
    updateLength() {
        this.lengthValue.textContent = this.lengthSlider.value;
    }
    
    generatePassword() {
        const length = parseInt(this.lengthSlider.value);
        let charset = '';
        
        if (this.uppercaseCheck.checked) charset += this.characters.uppercase;
        if (this.lowercaseCheck.checked) charset += this.characters.lowercase;
        if (this.numbersCheck.checked) charset += this.characters.numbers;
        if (this.symbolsCheck.checked) charset += this.characters.symbols;
        
        if (charset === '') {
            alert('Please select at least one character type!');
            return;
        }
        
        let password = '';
        for (let i = 0; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        
        this.passwordField.value = password;
        this.updateStrengthIndicator(password);
    }
    
    updateStrengthIndicator(password) {
        let score = 0;
        let feedback = '';
        
        // Length check
        if (password.length >= 12) score += 25;
        else if (password.length >= 8) score += 15;
        else score += 5;
        
        // Character variety check
        if (/[a-z]/.test(password)) score += 15;
        if (/[A-Z]/.test(password)) score += 15;
        if (/[0-9]/.test(password)) score += 15;
        if (/[^a-zA-Z0-9]/.test(password)) score += 20;
        
        // Bonus for length
        if (password.length >= 16) score += 10;
        
        // Update visual indicator
        this.strengthBar.style.width = Math.min(score, 100) + '%';
        
        if (score < 40) {
            this.strengthBar.className = 'strength-fill strength-weak';
            this.strengthText.textContent = 'Weak';
            this.strengthText.className = 'strength-text strength-weak';
            feedback = 'Consider using more character types and increasing length';
        } else if (score < 70) {
            this.strengthBar.className = 'strength-fill strength-medium';
            this.strengthText.textContent = 'Medium';
            this.strengthText.className = 'strength-text strength-medium';
            feedback = 'Good password, but could be stronger';
        } else {
            this.strengthBar.className = 'strength-fill strength-strong';
            this.strengthText.textContent = 'Strong';
            this.strengthText.className = 'strength-text strength-strong';
            feedback = 'Excellent password strength!';
        }
    }
    
    async copyPassword() {
        if (!this.passwordField.value) {
            alert('Generate a password first!');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(this.passwordField.value);
            this.copyBtn.textContent = '✅ Copied!';
            this.copyBtn.classList.add('copied');
            
            setTimeout(() => {
                this.copyBtn.textContent = '📋 Copy';
                this.copyBtn.classList.remove('copied');
            }, 2000);
        } catch (err) {
            // Fallback for older browsers
            this.passwordField.select();
            document.execCommand('copy');
            alert('Password copied to clipboard!');
        }
    }
}

// Initialize the password generator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PasswordGenerator();
    console.log('🔐 Secure Password Generator loaded! Built with ULTIMA AI.');
});