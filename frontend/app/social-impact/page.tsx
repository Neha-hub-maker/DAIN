import React from 'react'
import { getSocialImpactMilestones } from '../lib/api'
import SocialImpactForm from './SocialImpactForm'

export const dynamic = 'force-dynamic'

export default async function SocialImpactSectorPage() {
  const milestones = await getSocialImpactMilestones().catch((err) => {
    console.error("Failed to fetch social impact milestones:", err)
    return []
  })

  const totalHours = milestones.reduce((sum, m) => sum + m.hours_volunteered, 0)
  const totalInitiatives = milestones.reduce((sum, m) => sum + m.initiatives_led, 0)

  return (
    <div className="p-8 min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-purple-500/20 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-purple-500 tracking-tight">Social Impact</h1>
            <p className="text-slate-400 mt-2">Log community campaign progress, volunteer hours, and local scaling projects.</p>
          </div>
          <div>
            <SocialImpactForm />
          </div>
        </header>

        {/* Dashboard Indicators */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Volunteer Contribution</span>
            <span className="text-3xl font-extrabold text-purple-400 mt-1 block">
              {totalHours} hrs
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Initiatives Guided</span>
            <span className="text-3xl font-extrabold text-purple-400 mt-1 block">
              {totalInitiatives} Projects
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Voluntary Chapters</span>
            <span className="text-3xl font-extrabold text-purple-400 mt-1 block">
              {milestones.length} Logs
            </span>
          </div>
        </section>

        {/* Milestones List */}
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">Impact Portfolio</h2>
          {milestones.length === 0 ? (
            <div className="text-center py-16 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              No impact milestones recorded yet. Click "Add Milestone" to document volunteering or advocacy work.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {milestones.map((milestone) => (
                <div 
                  key={milestone.id} 
                  className="bg-slate-900 border border-slate-850 hover:border-purple-500/30 rounded-xl p-6 transition shadow-md hover:shadow-lg flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 uppercase tracking-wide">
                        {milestone.cause_area}
                      </span>
                      {milestone.date && (
                        <span className="text-xs text-slate-500">Date: {milestone.date}</span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-white">{milestone.role}</h3>
                    <p className="text-sm text-slate-300 font-medium">{milestone.organization}</p>
                    {milestone.description && (
                      <p className="text-sm text-slate-400 leading-relaxed max-w-2xl">{milestone.description}</p>
                    )}
                  </div>
                  {(milestone.hours_volunteered > 0 || milestone.scale_metric) && (
                    <div className="bg-slate-950 px-4 py-2 rounded-lg border border-slate-800 h-fit w-fit text-right min-w-[6rem]">
                      <span className="text-xs text-slate-500 block uppercase font-medium">Metrics</span>
                      {milestone.hours_volunteered > 0 && (
                        <span className="text-sm font-bold text-purple-400 block">{milestone.hours_volunteered} hrs</span>
                      )}
                      {milestone.scale_metric && (
                        <span className="text-[10px] text-slate-500 block mt-0.5">{milestone.scale_metric}</span>
                      )}
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
