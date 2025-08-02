document.addEventListener('DOMContentLoaded', function() {
    // Image upload preview functionality
    const fileInput = document.querySelector('input[type="file"]');
    const previewContainer = document.getElementById('image-preview');
    
    if (fileInput && previewContainer) {
        fileInput.addEventListener('change', function(e) {
            previewContainer.innerHTML = '';
            
            const files = e.target.files;
            if (files.length > 0) {
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.type.match('image.*')) {
                        const reader = new FileReader();
                        
                        reader.onload = function(e) {
                            const previewItem = document.createElement('div');
                            previewItem.className = 'preview-item';
                            
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.alt = 'Preview';
                            
                            const removeBtn = document.createElement('button');
                            removeBtn.className = 'remove-btn';
                            removeBtn.innerHTML = '×';
                            removeBtn.addEventListener('click', function() {
                                previewItem.remove();
                                removeFileFromInput(fileInput, file);
                            });
                            
                            previewItem.appendChild(img);
                            previewItem.appendChild(removeBtn);
                            previewContainer.appendChild(previewItem);
                        }
                        
                        reader.readAsDataURL(file);
                    }
                }
            }
        });
    }

    // Function to remove file from input
    function removeFileFromInput(input, fileToRemove) {
        const files = Array.from(input.files);
        const remainingFiles = files.filter(file => file.name !== fileToRemove.name);
        
        const dataTransfer = new DataTransfer();
        remainingFiles.forEach(file => dataTransfer.items.add(file));
        input.files = dataTransfer.files;
    }

    // Drag and drop functionality
    const dropArea = document.querySelector('.file-upload-preview');
    
    if (dropArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight() {
            dropArea.classList.add('highlight');
        }

        function unhighlight() {
            dropArea.classList.remove('highlight');
        }

        dropArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            
            // Trigger change event manually
            const event = new Event('change');
            fileInput.dispatchEvent(event);
        }
    }

    // Price formatting
    const priceInput = document.getElementById('id_price');
    if (priceInput) {
        priceInput.addEventListener('blur', function() {
            const value = parseFloat(this.value.replace(/,/g, ''));
            if (!isNaN(value)) {
                this.value = value.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
            }
        });
    }
});