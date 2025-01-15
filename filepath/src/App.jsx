import React, { useState, useEffect } from 'react';
import { FileSpreadsheet } from 'lucide-react';

const App = () => {
  const [showWelcome, setShowWelcome] = useState(true);
  const [file, setFile] = useState(null);
  const [name, setName] = useState('ubaid'); // Adding name to send with the file
  const [responseMessage, setResponseMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Handle the welcome message timeout
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 5000);

    // Cleanup the timer on component unmount
    return () => clearTimeout(timer);
  }, []);

  // Handle file change (input event)
  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    setFile(uploadedFile);
    setResponseMessage(""); // Reset any previous response message
  };

  // Handle the file upload
  const handleFileUpload = async (e) => {
    e.preventDefault(); // Prevent default form submission

    if (!file) {
      setResponseMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append('content', file);
    formData.append('name', name); // Append the name to the form data

    setIsLoading(true);

    try {
      // Send the file and name to the backend using a POST request
      const response = await fetch("http://127.0.0.1:8000/excel/upload-file/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResponseMessage("File uploaded successfully!");
        console.log(data); // You can log the returned data for further processing
      } else {
        setResponseMessage(`Error: ${data.message || 'Something went wrong'}`);
      }
    } catch (error) {
      setResponseMessage(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Welcome Screen
  if (showWelcome) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-white mb-4 animate-fade-in">
            Welcome to University Dashboard
          </h1>
          <p className="text-blue-100 text-xl">Loading your experience...</p>
        </div>
      </div>
    );
  }

  // Main Application Screen
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          University Resources
        </h2>

        <div className="flex flex-col items-center">
          <label
            htmlFor="fileUpload"
            className="flex items-center gap-3 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 cursor-pointer"
          >
            <FileSpreadsheet className="w-5 h-5" />
            <span>Attach Excel File</span>
          </label>
          <input
            type="file"
            id="fileUpload"
            name="file"
            accept=".xlsx, .xls"
            required
            onChange={handleFileChange}
            className="mt-4 hidden"
          />

          <button
            onClick={handleFileUpload}
            className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
            disabled={isLoading}
          >
            {isLoading ? "Uploading..." : "Upload File"}
          </button>

          {responseMessage && (
            <p className={`mt-4 text-sm ${responseMessage.includes('Error') ? 'text-red-500' : 'text-green-500'} text-center`}>
              {responseMessage}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
