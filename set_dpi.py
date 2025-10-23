Pillow
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DPI Converter App (Phase 2 - Backend)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007bff;
            text-align: center;
            margin-bottom: 30px;
        }
        .step {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-left: 5px solid #007bff;
            border-radius: 4px;
            background-color: #f9f9ff;
        }
        label, button {
            display: block;
            margin-top: 10px;
        }
        input[type="file"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
            background-color: #fff;
        }
        button {
            background-color: #28a745;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #218838;
        }
        #statusMessage {
            margin-top: 20px;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
            display: none; /* Hidden by default */
        }
        .status-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>DPI Converter App (Phase 2 - Python Backend)</h1>

        <div class="step">
            <p><strong>Step 1: Upload Image</strong></p>
            <label for="imageUpload">Choose an image file (JPG, PNG, TIFF):</label>
            <input type="file" id="imageUpload" accept="image/*">
        </div>

        <div class="step">
            <p><strong>Step 2: Convert to 300 DPI</strong></p>
            <button onclick="processImage()" id="convertButton" disabled>Convert & Download 300 DPI Image</button>
        </div>

        <div id="statusMessage"></div>

    </div>

    <script>
        const uploadInput = document.getElementById('imageUpload');
        const convertButton = document.getElementById('convertButton');
        const statusMessage = document.getElementById('statusMessage');

        // Enable button when a file is selected
        uploadInput.addEventListener('change', function() {
            convertButton.disabled = !uploadInput.files.length;
            hideStatus();
        });

        // Function to show status message
        function showStatus(message, isError = false) {
            statusMessage.textContent = message;
            statusMessage.className = isError ? 'status-error' : 'status-success';
            statusMessage.style.display = 'block';
        }

        // Function to hide status message
        function hideStatus() {
            statusMessage.style.display = 'none';
        }


        // *** PHASE 2 CHANGE: Send image to Python API ***
        async function processImage() {
            const file = uploadInput.files[0];
            if (!file) {
                showStatus("Please select a file first.", true);
                return;
            }

            convertButton.disabled = true;
            convertButton.textContent = "Processing... Please Wait...";
            hideStatus();

            try {
                // Prepare the data to send to the server
                const formData = new FormData();
                formData.append('image_file', file);

                // The Vercel route for our Python file is /api/set_dpi
                const response = await fetch('/api/set_dpi', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    // Get the file contents and download it
                    const blob = await response.blob();
                    const filename = response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '');
                    
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = filename; // Use the filename provided by the server
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    
                    showStatus("Success! Your 300 DPI image has downloaded.", false);
                } else {
                    const errorText = await response.text();
                    showStatus(`Conversion Failed. Server error: ${response.status} - ${errorText.substring(0, 100)}`, true);
                }

            } catch (error) {
                console.error('Fetch error:', error);
                showStatus("An unexpected error occurred during upload.", true);
            } finally {
                convertButton.disabled = false;
                convertButton.textContent = "Convert & Download 300 DPI Image";
            }
        }
    </script>
</body>
</html>