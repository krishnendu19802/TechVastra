import React, { useState } from 'react';
import axios from 'axios';
import ImageShow from './ImageShow';
import Loader from './Loader';

const ImageUpload = () => {
    const [personFile, setPersonFile] = useState(null);
    const [fabricFile, setFabricFile] = useState(null);
    const [personImageSrc, setPersonImageSrc] = useState('');
    const [fabricImageSrc, setFabricImageSrc] = useState('');
    const [loading, setLoading] = useState(false)
    const [status, setStatus] = useState([false])

    const [imageSrc, setImageSrc] = useState('');

    const handleFileChange = (e) => {
        if (imageSrc !== '')
            setImageSrc('')
        const file = e.target.files[0];
        if (e.target.name === 'person') {
            setPersonFile(file);
            const personUrl = URL.createObjectURL(file);
            setPersonImageSrc(personUrl);
        } else if (e.target.name === 'fabric') {
            setFabricFile(file);
            const fabricUrl = URL.createObjectURL(file);
            setFabricImageSrc(fabricUrl);
        }
    };

    const handleUpload = async () => {
        try {
            if (personFile === null || fabricFile === null) {
                console.log('Please select both files');
                setStatus([true, 'Please select both the files'])
                return;
            }
            if (status[0])
                setStatus([false])
            setLoading(true)
            const formData = new FormData();
            formData.append('person', personFile);
            formData.append('fabric', fabricFile);

            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob'
            });
            console.log('received image');
            // Assuming response.data is a Blob object (binary data like an image)
            const imageUrl = URL.createObjectURL(response.data);
            setLoading(false)
            setImageSrc(imageUrl);


        } catch (error) {
            console.error('Error uploading image', error);
            // Handle error (e.g., show error message)
        }
    };

    return (
        <div className={` mx-auto flex flex-col w-full justify-center min-h-screen items-center ${imageSrc !== '' ? 'mt-8' : ''} p-4 md:p-0`}>
            <div className="image-form p-8 shadow-xl w-4/5 md:w-1/3 rounded-md flex flex-col justify-center">
                
            <div className="flex flex-col md:flex-row w-full md:justify-between my-4 items-center">
                    <div className="flex flex-col items-center md:items-center md:mr-4">
                        <label className="block mb-2 text-start text-sm font-medium text-gray-700" htmlFor="person">
                            Upload Your Image
                        </label>
                        <input
                            type="file"
                            name="person"
                            id="person"
                            onChange={handleFileChange}
                            className="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:border-blue-500 p-2"
                        />
                    </div>
                    {personImageSrc && <ImageShow source={personImageSrc} altText={'Original Image'} size={12} />}
                </div>

                <div className="flex flex-col md:flex-row w-full md:justify-between my-4 items-center">
                    <div className="flex flex-col items-center md:items-center md:mr-4">
                        <label className="block mb-2 text-start text-sm font-medium text-gray-700" htmlFor="fabric">
                            Upload Fabric Image
                        </label>
                        <input
                            type="file"
                            name="fabric"
                            id="fabric"
                            onChange={handleFileChange}
                            className="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:border-blue-500 p-2"
                        />
                    </div>
                    {fabricImageSrc && <ImageShow source={fabricImageSrc} altText={'Original Image'} size={12} />}
                </div>

                <div className="flex justify-center my-4">
                    <button onClick={handleUpload} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Upload Image
                    </button>
                </div>
                <div className="my-2 text-center text-red-700">
                    {status[0] && status[1]}
                </div>

            </div>

            {!loading && imageSrc && <div className="image my-4 flex flex-col md:flex-row md:justify-between ">
                <div className="text-xl font-bold md:mr-4">
                    <h1 className='text-center '>Original Image</h1>
                    {personImageSrc && <ImageShow source={personImageSrc} altText={'Original Image'} size={64} />
                    }
                </div>
                <div className="text-xl font-bold md:ml-4">
                    <h1 className='text-center '>Result Image</h1>

                    {imageSrc && <ImageShow source={imageSrc} altText={'Result Image'} size={64} />
                    }
                </div>


            </div>}

            {loading && <div className="p-4 flex justify-center">
                <Loader size={96} />

            </div>}



        </div>
    );
};

export default ImageUpload;
