"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import Navbar from "./components/Navbar";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'video/*': [] } });

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      
      {/* Hero Section */}
      <section className="h-screen flex flex-col items-center justify-center text-center px-6 pt-20">
        <h1 className="text-5xl font-bold mb-4">Watchman</h1>
        <p className="text-lg text-gray-300 max-w-2xl">
          Securely upload your CCTV footage and get AI-processed videos with detected objects.
        </p>
      </section>

      {/* Upload Section */}
      <section className="py-20 bg-gray-800 flex flex-col items-center">
        <motion.div
          className="border-4 border-dashed border-gray-600 p-10 rounded-lg cursor-pointer w-96 text-center"
          {...getRootProps()}
          initial={{ scale: 0.9 }}
          whileHover={{ scale: 1 }}
        >
          <input {...getInputProps()} />
          <UploadCloud size={48} className="text-gray-400 mx-auto mb-4" />
          {isDragActive ? (
            <p className="text-gray-300">Drop the video here...</p>
          ) : (
            <p className="text-gray-300">Drag & drop a video file here, or click to select one</p>
          )}
        </motion.div>

        {/* Display selected files */}
        {files.length > 0 && (
          <div className="mt-6 text-gray-300">
            <h3 className="text-lg font-medium mb-2">Selected Files:</h3>
            <ul>
              {files.map((file) => (
                <li key={file.name} className="text-sm">{file.name}</li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </div>
  );
}