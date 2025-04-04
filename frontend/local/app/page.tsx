"use client";

import Navbar from "./components/Navbar";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      {/* Add top padding to offset the fixed navbar */}
      <div className="pt-24 flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold mb-6 text-center">Live Object Detection</h1>

        <div className="border-4 border-white rounded overflow-hidden">
          <img
            src="http://192.168.1.6:5000/video"
            alt="Live Object Detection"
            className="w-[640px] h-[480px] object-cover"
          />
        </div>
      </div>
    </div>
  );
}
