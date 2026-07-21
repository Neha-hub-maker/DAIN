import React from 'react'
import { getPersonalMilestones } from '../lib/api'
import PersonalForm from './PersonalForm'

export const dynamic = 'force-dynamic'

export default async function PersonalSectorPage() {
  const milestones = await getPersonalMilestones().catch((err) => {
    console.error("Failed to fetch personal milestones:", err)
    return []
  })

  return (
    <div className="p-8 min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-rose-500/20 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-rose-500 tracking-tight">Personal & Extracurricular</h1>
            <p className="text-slate-400 mt-2">Track credential achievements, external skills, and extracurricular activities.</p>
          </div>
          <div>
            <PersonalForm />
          </div>
        </header>

        {/* Dashboard Indicators */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Skills & Certs</span>
            <span className="text-3xl font-extrabold text-rose-400 mt-1 block">
              {milestones.filter(m => m.category === 'skill').length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Extracurriculars</span>
            <span className="text-3xl font-extrabold text-rose-400 mt-1 block">
              {milestones.filter(m => m.category === 'extracurricular').length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Total Accomplished</span>
            <span className="text-3xl font-extrabold text-rose-400 mt-1 block">
              {milestones.filter(m => m.status === 'achieved').length}
            </span>
          </div>
        </section>

        {/* Milestones List */}
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">Extracurricular logs</h2>
          {milestones.length === 0 ? (
            <div className="text-center py-16 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              No personal milestones registered. Click "Add Milestone" to input certifications or activities.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {milestones.map((milestone) => (
                <div 
                  key={milestone.id} 
                  className="bg-slate-900 border border-slate-850 hover:border-rose-500/30 rounded-xl p-6 transition shadow-md hover:shadow-lg flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 uppercase tracking-wide">
                        {milestone.category}
                      </span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                        milestone.status === 'achieved' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'
                      }`}>
                        {milestone.status === 'achieved' ? 'Achieved' : 'In Progress'}
                      </span>
                      {milestone.date_achieved && (
                        <span className="text-xs text-slate-500">Date: {milestone.date_achieved}</span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-white">{milestone.title}</h3>
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
