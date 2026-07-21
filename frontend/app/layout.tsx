import type { Metadata } from 'next'
import Link from 'next/link'
import './globals.css'

export const metadata: Metadata = {
  title: 'DAIN Ecosystem Platform',
  description: 'Track and map growth across Academic, Professional, Entrepreneurial, Social Impact, and Personal sectors.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-brand-dark text-brand-light font-sans min-h-screen flex flex-col">
        {/* Navigation Bar */}
        <header className="border-b border-slate-800 bg-brand-dark/80 backdrop-blur sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <Link href="/" className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-500 via-purple-500 to-rose-500 bg-clip-text text-transparent hover:opacity-90 transition">
                DAIN Platform
              </Link>
              <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">MVP</span>
            </div>

            {/* Navigation links for sectors */}
            <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
              <Link 
                href="/academic" 
                className="text-slate-400 hover:text-sector-academic transition-colors"
              >
                Academic
              </Link>
              <Link 
                href="/professional" 
                className="text-slate-400 hover:text-sector-professional transition-colors"
              >
                Professional
              </Link>
              <Link 
                href="/entrepreneurial" 
                className="text-slate-400 hover:text-sector-entrepreneurial transition-colors"
              >
                Entrepreneurial
              </Link>
              <Link 
                href="/social-impact" 
                className="text-slate-400 hover:text-sector-socialImpact transition-colors"
              >
                Social Impact
              </Link>
              <Link 
                href="/personal" 
                className="text-slate-400 hover:text-sector-personal transition-colors"
              >
                Personal
              </Link>
            </nav>

            {/* Action buttons */}
            <div className="flex items-center gap-4">
              <button className="text-xs font-semibold px-4 py-2 rounded-full border border-slate-800 hover:bg-slate-900 transition">
                Sign In
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-grow">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-900 bg-brand-dark py-6 text-center text-xs text-slate-600">
          <p>&copy; {new Date().getFullYear()} DAIN Ecosystem Platform. All rights reserved.</p>
        </footer>
      </body>
    </html>
  )
}
