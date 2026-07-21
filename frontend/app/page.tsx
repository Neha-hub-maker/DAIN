import React from 'react'
import Link from 'next/link'

export default function LandingPage() {
  const sectors = [
    {
      name: 'Academic Portfolio',
      description: 'Track and showcase publication achievements, research operations, and CGPA milestones.',
      path: '/academic',
      colorClass: 'border-blue-500/20 hover:border-blue-500 text-blue-400 bg-blue-500/5',
      badge: 'Publications & CGPA',
    },
    {
      name: 'Professional Placements',
      description: 'Document corporate job roles, industry internships, work placements, and corporate milestones.',
      path: '/professional',
      colorClass: 'border-emerald-500/20 hover:border-emerald-500 text-emerald-400 bg-emerald-500/5',
      badge: 'Corporate Roles',
    },
    {
      name: 'Entrepreneurial Ventures',
      description: 'Record startups launched, project ventures, and venture capital/angel funding rounds secured.',
      path: '/entrepreneurial',
      colorClass: 'border-amber-500/20 hover:border-amber-500 text-amber-400 bg-amber-500/5',
      badge: 'Startups & Funding',
    },
    {
      name: 'Social Impact Scaling',
      description: 'Catalog community volunteer projects, scaling initiatives, and civic contributions.',
      path: '/social-impact',
      colorClass: 'border-purple-500/20 hover:border-purple-500 text-purple-400 bg-purple-500/5',
      badge: 'Volunteering & Scale',
    },
    {
      name: 'Personal Achievements',
      description: 'Map extracurricular achievements, self-development projects, and skill certifications.',
      path: '/personal',
      colorClass: 'border-rose-500/20 hover:border-rose-500 text-rose-400 bg-rose-500/5',
      badge: 'Skills & Extracurriculars',
    },
  ]

  return (
    <div className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-4">
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-purple-400 to-rose-400 bg-clip-text text-transparent">
          Map Your Multi-Sector Growth
        </h1>
        <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-400">
          The DAIN Ecosystem Platform tracks, visualizes, and models developmental milestones across Academic, Professional, Entrepreneurial, Social Impact, and Personal growth layers.
        </p>
      </section>

      {/* Grid Section for Five Core Sectors */}
      <section className="space-y-8">
        <h2 className="text-2xl font-bold text-white text-center sm:text-left">Explore Development Layers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sectors.map((sector) => (
            <Link 
              key={sector.name} 
              href={sector.path}
              className={`block border rounded-xl p-6 transition-all duration-300 hover:scale-[1.02] ${sector.colorClass}`}
            >
              <div className="flex flex-col justify-between h-full space-y-4">
                <div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-slate-900 border border-slate-800 uppercase tracking-wider block w-fit mb-3">
                    {sector.badge}
                  </span>
                  <h3 className="text-xl font-bold text-white mb-2">{sector.name}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{sector.description}</p>
                </div>
                <div className="text-xs font-semibold flex items-center gap-1 group-hover:underline">
                  View Sector Portfolio &rarr;
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
