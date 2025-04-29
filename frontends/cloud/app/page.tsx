"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import Navbar from "./components/Navbar";

export default function Home() {
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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

      if (!response.ok) throw new Error("Failed to upload video. Please try again.");
      const data = await response.json();
      setJobId(data.job_id);
      setProcessing(true);
      checkProcessingStatus(data.job_id);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An unknown error occurred.");
      setProcessing(false);
    } finally {
      setUploading(false);
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (processing) return;
    uploadFile(acceptedFiles[0]);
  }, [processing, uploadFile]);

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
          const a = document.createElement("a");
          a.href = downloadUrl;
          a.download = "processed_video.mp4";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          setProcessing(false);
        }
      } catch {
        clearInterval(interval);
        setProcessing(false);
        setError("Error checking job status. Please refresh and try again.");
      }
    }, 5000);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "video/*": [] },
    disabled: processing,
  });

  return (
    <div className="bg-gray-900 text-white min-h-screen">
      <Navbar />

      {/* Hero */}
      <section className="pt-32 pb-20 text-center px-6">
        <h1 className="text-5xl font-bold mb-4">Watchman</h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          An AI-powered CCTV storage management system that detects humans and saves only the necessary footage. Optimized for Raspberry Pi using YOLOv8n, given the ability to detect objects on old CCTVs.
        </p>
      </section>

      {/* How it works */}
      <section className="bg-gray-800 py-20 px-6">
        <h2 className="text-3xl font-bold text-center mb-10">📽️ How it Works</h2>
        <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-8 text-center">
          <div>
            <h3 className="text-xl font-semibold mb-2">1. Upload or Stream</h3>
            <p className="text-gray-400">Send footage from a webcam or upload video files.</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-2">2. Detect with YOLOv8n</h3>
            <p className="text-gray-400">Our custom model detects only humans in real-time.</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-2">3. Save Smart</h3>
            <p className="text-gray-400">Only relevant footage is saved, converted, and available for download.</p>
          </div>
        </div>
      </section>

      {/* Sample Comparison */}
      <section className="py-20 px-6">
        <h2 className="text-3xl font-bold text-center mb-10">🎬 Sample Detection</h2>
        <div className="flex flex-col md:flex-row gap-10 justify-center items-center max-w-5xl mx-auto">
          <div className="w-full md:w-1/2">
            <p className="mb-2 text-center text-gray-400">Original Footage</p>
            <video
              autoPlay
              muted
              playsInline
              controls
              className="rounded-lg shadow-lg w-full"
            >
              <source src="/videos/sample_original.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
          <div className="w-full md:w-1/2">
            <p className="mb-2 text-center text-gray-400">Detected Output</p>
            <video
              autoPlay
              muted
              playsInline
              controls
              className="rounded-lg shadow-lg w-full"
            >
              <source src="/videos/sample_detected.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      </section>

      {/* Upload Area */}
      <section className="bg-gray-800 py-20 px-6 flex flex-col items-center">
        <h2 className="text-3xl font-bold mb-8">⬆️ Upload Your Footage</h2>
        <div {...getRootProps()} className={`w-96 ${processing ? "opacity-50 cursor-not-allowed" : ""}`}>
          <motion.div
            className="border-4 border-dashed border-gray-600 p-10 rounded-xl cursor-pointer text-center"
            initial={{ scale: 0.9 }}
            whileHover={{ scale: 1 }}
          >
            <input {...getInputProps()} />
            <UploadCloud size={48} className="text-gray-400 mx-auto mb-4" />
            <p className="text-gray-300">
              {processing
                ? "Processing in progress..."
                : isDragActive
                ? "Drop the video here..."
                : "Drag & drop or click to upload a video"}
            </p>
          </motion.div>
        </div>

        {uploading && <p className="text-gray-300 mt-4">Uploading...</p>}
        {processing && jobId && <p className="text-gray-300 mt-4">Processing your video...</p>}
        {error && <div className="mt-6 bg-red-600 text-white p-3 rounded-md">⚠️ {error}</div>}
      </section>

      {/* Footer */}
      <footer className="text-center py-6 text-gray-500 text-sm">
        Built by Lahiru De Silva | <a href="https://github.com/RashmithaDeSilva/Watchman" target="_blank" className="underline">GitHub Repo</a>
      </footer>
    </div>
  );
}
