"use client";

import Navbar from "./components/Navbar";
import { useEffect, useState } from "react";

// const BACKEND_URL = "http://192.168.1.6:5000";

export default function Home() {
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    // On load, check current saving state from backend
    fetch(`/api/is-saving`)
      .then((res) => res.json())
      .then((data) => {
        setIsSaving(data.saving);
      });
  }, []);

  const toggleSaving = async () => {
    const endpoint = isSaving ? "stop-saving" : "start-saving";

    const res = await fetch(`/api/${endpoint}`, {
      method: "POST",
    });

    if (res.ok) {
      setIsSaving((prev) => !prev);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="flex flex-col items-center justify-center pt-24">
        <h1 className="text-4xl font-bold mb-6">Live Object Detection</h1>

        <div className="border-4 border-white rounded overflow-hidden">
          <img
            src={`/api/video`}
            alt="Live Object Detection"
            className="w-[640px] h-[480px] object-cover"
          />
        </div>

        {/* Save Toggle Button */}
        <button
          onClick={toggleSaving}
          className={`mt-6 px-6 py-3 rounded text-white font-semibold transition ${
            isSaving
              ? "bg-red-600 hover:bg-red-700"
              : "bg-green-600 hover:bg-green-700"
          }`}
        >
          {isSaving ? "Disable Saving" : "Enable Saving"}
        </button>
      </div>
    </div>
  );
}
