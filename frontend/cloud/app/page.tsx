"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import Navbar from "./components/Navbar";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [videoURL, setVideoURL] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    uploadFile(acceptedFiles[0]);
  }, []);

  const uploadFile = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    // formData.append("video", file);
    formData.append("file", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setVideoURL(`/api/${data.video_path}`);
    } catch (error) {
      console.error("Error uploading video:", error);
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop, 
    accept: { "video/*": [] } 
  });

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
        <div {...getRootProps()} className="w-96">
          <motion.div
            className="border-4 border-dashed border-gray-600 p-10 rounded-lg cursor-pointer text-center"
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
        </div>

        {/* Uploading Indicator */}
        {uploading && <p className="text-gray-300 mt-4">Uploading...</p>}

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

        {/* Display processed video */}
        {videoURL && (
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-2">Processed Video:</h3>
            <video controls className="w-96">
              <source src={videoURL} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </section>
    </div>
  );
}
