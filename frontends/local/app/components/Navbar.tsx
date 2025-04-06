import React from 'react'
import Link from "next/link";

const Navbar = () => {
  return (
    <div>
      {/* Navigation */}
      <nav className="p-6 bg-gray-800 shadow-lg fixed top-0 w-full flex justify-between items-center px-10">
          <h1 className="text-2xl font-bold text-white"><Link href="/">Watchman</Link></h1>
          <div className="space-x-6 text-lg">
            <Link href="/" className="text-gray-300 hover:text-white">Live</Link>
            <Link href="/footages" className="text-gray-300 hover:text-white">Footages</Link>
          </div>
      </nav>
    </div>
  );
}

export default Navbar