import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [personFile, setPersonFile] = useState(null);
    const [fabricFile, setFabricFile] = useState(null);
    const [imageSrc, setImageSrc] = useState('');

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (e.target.name === 'person') {
            setPersonFile(file);
        } else if (e.target.name === 'fabric') {
            setFabricFile(file);
        }
    };

    const handleUpload = async () => {
        try {
            if (personFile === null || fabricFile === null) {
                console.log('Please select both files');
                return;
            }

            const formData = new FormData();
            formData.append('person', personFile);
            formData.append('fabric', fabricFile);

            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob' 
            });
            console.log('received image')
            // Assuming response.data is a Blob object (binary data like an image)
            const imageUrl = URL.createObjectURL(response.data);
            setImageSrc(imageUrl);

        } catch (error) {
            console.error('Error uploading image', error);
            // Handle error (e.g., show error message)
        }
    };

    return (
        <div className="max-w-xs mx-auto mt-8">
            <input type="file" name='person' onChange={handleFileChange} className="mb-4" />
            <input type="file" name='fabric' onChange={handleFileChange} className="mb-4" />

            <button onClick={handleUpload} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Upload Image
            </button>

            {imageSrc && (
                <div className="mt-4">
                    <img src={imageSrc} alt="Uploaded Image" className="max-w-xs mx-auto" />
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
