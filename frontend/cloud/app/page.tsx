"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import Navbar from "./components/Navbar";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    uploadFile(acceptedFiles[0]);
  }, []);

  const uploadFile = async (file: File) => {
    setUploading(true);
    setProcessing(false);
    setJobId(null);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload video. Please try again.");
      }

      const data = await response.json();
      setJobId(data.job_id);
      setProcessing(true);

      // Start polling for the processed video
      checkProcessingStatus(data.job_id);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An unknown error occurred.");
    } finally {
      setUploading(false);
    }
  };

  const checkProcessingStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`/api/status/${jobId}`);

        if (response.status === 404) {
          clearInterval(interval);
          setProcessing(false);
          setError("Processing failed. Please try again.");
          return;
        }

        if (response.ok) {
          clearInterval(interval);
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          
          // Auto-download processed video
          const a = document.createElement("a");
          a.href = downloadUrl;
          a.download = "processed_video.mp4";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);

          setProcessing(false);
        }
      } catch (error) {
        clearInterval(interval);
        setProcessing(false);
        setError("Error checking job status. Please refresh and try again.");
      }
    }, 5000);
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

        {/* Processing Indicator */}
        {processing && jobId && <p className="text-gray-300 mt-4">Processing video...</p>}

        {/* Error Message */}
        {error && (
          <div className="mt-6 bg-red-600 text-white p-3 rounded-md">
            ⚠️ {error}
          </div>
        )}
      </section>
    </div>
  );
}
