"use client";

import { useEffect, useState } from "react";
import Navbar from "../components/Navbar"; // Import Navbar

// const BACKEND_URL = "http://192.168.1.6:5000"; // Make sure this matches your backend URL

const Futagers = () => {
  const [videos, setVideos] = useState<string[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);

  // Fetch the footages when the component is mounted
  useEffect(() => {
    fetch(`/api/footages`)
      .then((res) => res.json())
      .then((data) => {
        setVideos(data);
        if (data.length > 0) {
          setSelectedVideo(data[0]); // Set the first video as the default selected one
        }
      })
      .catch((error) => console.error("Error fetching footages:", error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white pt-24">
      <Navbar /> {/* Navbar */}

      <div className="flex mt-6 px-8">
        {/* Left: List of Footages */}
        <div className="w-1/3 pr-6 border-r border-gray-700 overflow-auto">
          <h2 className="text-2xl font-semibold mb-4">Saved Footages</h2>
          <ul className="space-y-3">
            {videos.map((file, index) => (
              <li
                key={index}
                className={`cursor-pointer p-2 rounded hover:bg-gray-700 ${
                  selectedVideo === file ? "bg-gray-700" : ""
                }`}
                onClick={() => setSelectedVideo(file)}
              >
                {file}
              </li>
            ))}
          </ul>
        </div>

        {/* Right: Selected Video */}
        <div className="w-2/3 pl-6">
          <h2 className="text-2xl font-semibold mb-4">Preview</h2>
          {selectedVideo ? (
            <video
              controls
              className="w-full rounded border-2 border-white"
              src={`/api/footages/${selectedVideo}`}
            />
          ) : (
            <p>No video selected</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Futagers;
