import React from 'react'
import { getAcademicMilestones } from '../lib/api'
import AcademicForm from './AcademicForm'

export const dynamic = 'force-dynamic'

export default async function AcademicSectorPage() {
  const milestones = await getAcademicMilestones().catch((err) => {
    console.error("Failed to fetch academic milestones:", err)
    return []
  })

  return (
    <div className="p-8 min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-blue-500/20 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-blue-500 tracking-tight">Academic Portfolio</h1>
            <p className="text-slate-400 mt-2">Track publications, research activities, and CGPA achievements.</p>
          </div>
          <div>
            <AcademicForm />
          </div>
        </header>

        {/* Dashboard Indicators */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Publications</span>
            <span className="text-3xl font-extrabold text-blue-400 mt-1 block">
              {milestones.filter(m => m.type === 'publication').length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Research Projects</span>
            <span className="text-3xl font-extrabold text-blue-400 mt-1 block">
              {milestones.filter(m => m.type === 'research').length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">CGPA Records</span>
            <span className="text-3xl font-extrabold text-blue-400 mt-1 block">
              {milestones.filter(m => m.type === 'cgpa').length}
            </span>
          </div>
        </section>

        {/* Milestones List */}
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">Milestone History</h2>
          {milestones.length === 0 ? (
            <div className="text-center py-16 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              No academic milestones logged yet. Click "Add Milestone" to create your first entry.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {milestones.map((milestone) => (
                <div 
                  key={milestone.id} 
                  className="bg-slate-900 border border-slate-850 hover:border-blue-500/30 rounded-xl p-6 transition shadow-md hover:shadow-lg flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 uppercase tracking-wide">
                        {milestone.type}
                      </span>
                      {milestone.date && (
                        <span className="text-xs text-slate-500">{milestone.date}</span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-white">{milestone.title}</h3>
                    <p className="text-sm text-slate-300 font-medium">{milestone.institution}</p>
                    {milestone.description && (
                      <p className="text-sm text-slate-400 leading-relaxed max-w-2xl">{milestone.description}</p>
                    )}
                  </div>
                  {milestone.value && (
                    <div className="bg-slate-950 px-4 py-2 rounded-lg border border-slate-800 h-fit w-fit">
                      <span className="text-xs text-slate-500 block uppercase font-medium">Metric</span>
                      <span className="text-sm font-bold text-blue-400">{milestone.value}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
