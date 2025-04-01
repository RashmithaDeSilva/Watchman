import Navbar from "../components/Navbar";

export default function LocalSetup() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      <div className="flex flex-col items-center justify-center min-h-screen px-6">
        <h1 className="text-4xl font-bold mb-4">Local Setup</h1>
        <p className="text-lg text-gray-300 max-w-2xl text-center">
          Learn how to set up Watchman on your local system for real-time CCTV monitoring and AI-based detection.
        </p>
      </div>
    </div>
  );
}