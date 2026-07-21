import React from 'react'
import { getProfessionalMilestones } from '../lib/api'
import ProfessionalForm from './ProfessionalForm'

export const dynamic = 'force-dynamic'

export default async function ProfessionalSectorPage() {
  const milestones = await getProfessionalMilestones().catch((err) => {
    console.error("Failed to fetch professional milestones:", err)
    return []
  })

  return (
    <div className="p-8 min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-emerald-500/20 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-emerald-500 tracking-tight">Professional Placements</h1>
            <p className="text-slate-400 mt-2">Manage corporate employment records, internships, and industry roles.</p>
          </div>
          <div>
            <ProfessionalForm />
          </div>
        </header>

        {/* Dashboard Indicators */}
        <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Total Positions</span>
            <span className="text-3xl font-extrabold text-emerald-400 mt-1 block">
              {milestones.length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Recent Employer</span>
            <span className="text-lg font-bold text-emerald-400 mt-1 block truncate">
              {milestones[0] ? `${milestones[0].role} at ${milestones[0].company}` : 'None logged'}
            </span>
          </div>
        </section>

        {/* Milestones List */}
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">Placement History</h2>
          {milestones.length === 0 ? (
            <div className="text-center py-16 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              No professional placements recorded yet. Click "Add Milestone" to capture your first job or internship.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {milestones.map((milestone) => (
                <div 
                  key={milestone.id} 
                  className="bg-slate-900 border border-slate-850 hover:border-emerald-500/30 rounded-xl p-6 transition shadow-md hover:shadow-lg flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 uppercase tracking-wide">
                        {milestone.industry_sector || 'Professional'}
                      </span>
                      {(milestone.start_date || milestone.end_date) && (
                        <span className="text-xs text-slate-500">
                          {milestone.start_date || 'Start'} — {milestone.end_date || 'Present'}
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-white">{milestone.role}</h3>
                    <p className="text-sm text-slate-300 font-medium">{milestone.company} {milestone.location && `• ${milestone.location}`}</p>
                    {milestone.description && (
                      <p className="text-sm text-slate-400 leading-relaxed max-w-2xl">{milestone.description}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
