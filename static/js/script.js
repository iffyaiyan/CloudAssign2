// Handle image preview in add product form
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image');
    
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                const previewDiv = document.getElementById('imagePreview') || createPreviewElement();
                
                reader.addEventListener('load', function() {
                    previewDiv.src = this.result;
                    previewDiv.style.display = 'block';
                });
                
                reader.readAsDataURL(file);
            }
        });
    }
    
    function createPreviewElement() {
        const previewDiv = document.createElement('img');
        previewDiv.id = 'imagePreview';
        previewDiv.className = 'img-thumbnail mt-2';
        previewDiv.alt = 'Image Preview';
        
        const formGroup = imageInput.closest('.mb-3');
        formGroup.appendChild(previewDiv);
        
        return previewDiv;
    }
});