document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Document upload preview
    document.getElementById('id_document')?.addEventListener('change', function(e) {
        var fileName = e.target.files[0].name;
        var nextSibling = e.target.nextElementSibling;
        if (nextSibling) {
            nextSibling.innerText = fileName;
        }
    });
    
    // Signature pad functionality
    if (document.getElementById('signature-pad')) {
        const canvas = document.getElementById('signature-pad');
        const signaturePad = new SignaturePad(canvas, {
            backgroundColor: 'rgb(255, 255, 255)',
            penColor: 'rgb(0, 0, 0)'
        });
        
        document.getElementById('clear-signature')?.addEventListener('click', function() {
            signaturePad.clear();
        });
        
        document.getElementById('save-signature')?.addEventListener('click', function() {
            if (signaturePad.isEmpty()) {
                alert('Please provide a signature first.');
            } else {
                const dataURL = signaturePad.toDataURL('image/png');
                document.getElementById('id_signature_image').value = dataURL;
                document.getElementById('signature-form').submit();
            }
        });
    }
    
    // Status update animation
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(badge => {
        badge.addEventListener('animationend', function() {
            this.classList.remove('pulse');
        });
        
        if (Math.random() > 0.7) {
            setTimeout(() => {
                badge.classList.add('pulse');
            }, 1000);
        }
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});