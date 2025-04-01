import Navbar from "../components/Navbar";
import Link from "next/link";

export default function About() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen px-6">
        <h1 className="text-4xl font-bold mb-4">About Watchman</h1>
        <p className="text-lg text-gray-300 max-w-2xl text-center">
          Watchman is a cutting-edge platform designed to analyze CCTV footage using AI-powered object detection.
          Our goal is to provide security and insights by detecting human presence and other objects in video footage.
        </p>
        <Link href="/" className="mt-6 text-gray-300 hover:text-white underline">
          Back to Home
        </Link>
      </div>
    </div>
  );
}