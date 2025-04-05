import Navbar from "../components/Navbar";
import Link from "next/link";
import {
  FaGithub,
  FaUserShield,
  FaRobot,
  FaLaptopCode,
  FaCogs,
  FaNetworkWired,
} from "react-icons/fa";

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <Navbar />

      {/* Add top padding to account for fixed navbar */}
      <div className="pt-28 px-6 py-16 max-w-6xl mx-auto space-y-12">
        <h1 className="text-5xl font-bold text-center bg-gradient-to-r from-cyan-400 to-blue-500 text-transparent bg-clip-text animate-fade-in">
          🛡️ About Watchman
        </h1>

        <div className="grid md:grid-cols-2 gap-10">
          {/* About Section */}
          <div className="bg-white/5 backdrop-blur-md p-6 rounded-2xl shadow-lg border border-white/10 transition hover:scale-[1.02]">
            <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2">
              <FaUserShield /> What is Watchman?
            </h2>
            <p className="text-gray-300">
              <strong>Watchman</strong> is an AI-powered CCTV footage analyzer that detects human presence in real time or uploaded videos. 
              It’s built to save only the important parts of the footage helping you reduce storage while increasing security insights.
            </p>
          </div>

          {/* Features */}
          <div className="bg-white/5 backdrop-blur-md p-6 rounded-2xl shadow-lg border border-white/10 transition hover:scale-[1.02]">
            <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2">
              <FaRobot /> Key Features
            </h2>
            <ul className="list-disc list-inside text-gray-300 space-y-1">
              <li>🔴 Real-time human detection</li>
              <li>📁 Analyze uploaded CCTV footage</li>
              <li>💾 Save only relevant video segments</li>
              <li>📹 Custom-trained YOLOv8n model</li>
              <li>🧠 Optimized for Raspberry Pi Zero 2 W</li>
              <li>🌐 Clean frontends for live and upload modes</li>
            </ul>
          </div>

          {/* Architecture */}
          <div className="bg-white/5 backdrop-blur-md p-6 rounded-2xl shadow-lg border border-white/10 transition hover:scale-[1.02]">
            <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2">
              <FaNetworkWired /> Architecture
            </h2>
            <ul className="list-disc list-inside text-gray-300 space-y-1">
              <li>🔌 Flask APIs for live & upload detection</li>
              <li>🎯 YOLOv8n model (detects only humans)</li>
              <li>🖥️ Frontend with Next.js + Tailwind CSS</li>
              <li>🐳 Containerized with Docker</li>
              <li>⚙️ Video conversion using FFmpeg</li>
            </ul>
          </div>

          {/* Tech Stack */}
          <div className="bg-white/5 backdrop-blur-md p-6 rounded-2xl shadow-lg border border-white/10 transition hover:scale-[1.02]">
            <h2 className="text-2xl font-semibold mb-2 flex items-center gap-2">
              <FaLaptopCode /> Tech Stack
            </h2>
            <ul className="list-disc list-inside text-gray-300 space-y-1">
              <li>💻 Frontend: Next.js, TypeScript, Tailwind CSS</li>
              <li>🔧 Backend: Flask (Python)</li>
              <li>🧠 Object Detection: YOLOv8n</li>
              <li>🎥 Video Tools: FFmpeg</li>
              <li>🐳 Docker, ESP32-CAM, Raspberry Pi</li>
            </ul>
          </div>
        </div>

        {/* GitHub and Author */}
        <div className="text-center space-y-6">
          <a
            href="https://github.com/RashmithaDeSilva/Watchman"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-xl shadow-lg text-white font-semibold text-lg hover:scale-105 transition"
          >
            <FaGithub className="mr-2" /> View on GitHub
          </a>
          <p className="text-gray-400 text-sm">
            Created by <strong>Lahiru De Silva</strong> as a final year project.
            <br />
            Made with using Flask, Next.js, and YOLOv8.
          </p>
        </div>
      </div>
    </div>
  );
}
