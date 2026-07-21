import React from 'react'
import { getEntrepreneurialMilestones } from '../lib/api'
import EntrepreneurialForm from './EntrepreneurialForm'

export const dynamic = 'force-dynamic'

export default async function EntrepreneurialSectorPage() {
  const milestones = await getEntrepreneurialMilestones().catch((err) => {
    console.error("Failed to fetch entrepreneurial milestones:", err)
    return []
  })

  // Format funding amount helper
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(value)
  }

  const totalFunding = milestones.reduce((sum, m) => sum + m.funding_amount, 0)

  return (
    <div className="p-8 min-h-[calc(100vh-8rem)]">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-amber-500/20 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-amber-500 tracking-tight">Entrepreneurial Ventures</h1>
            <p className="text-slate-400 mt-2">Log startup launch metrics, business stages, and funding rounds.</p>
          </div>
          <div>
            <EntrepreneurialForm />
          </div>
        </header>

        {/* Dashboard Indicators */}
        <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Ventures Managed</span>
            <span className="text-3xl font-extrabold text-amber-400 mt-1 block">
              {milestones.length}
            </span>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-lg">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Total Funding Raised</span>
            <span className="text-3xl font-extrabold text-amber-400 mt-1 block">
              {formatCurrency(totalFunding)}
            </span>
          </div>
        </section>

        {/* Milestones List */}
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">Startup Operations</h2>
          {milestones.length === 0 ? (
            <div className="text-center py-16 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/20">
              No startup milestones cataloged yet. Click "Add Milestone" to register your venture.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {milestones.map((milestone) => (
                <div 
                  key={milestone.id} 
                  className="bg-slate-900 border border-slate-850 hover:border-amber-500/30 rounded-xl p-6 transition shadow-md hover:shadow-lg flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 uppercase tracking-wide">
                        {milestone.stage}
                      </span>
                      {milestone.launch_date && (
                        <span className="text-xs text-slate-500">Launched: {milestone.launch_date}</span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-white">{milestone.venture_name}</h3>
                    <p className="text-sm text-slate-300 font-medium">{milestone.role}</p>
                    {milestone.description && (
                      <p className="text-sm text-slate-400 leading-relaxed max-w-2xl">{milestone.description}</p>
                    )}
                  </div>
                  {(milestone.funding_amount > 0 || milestone.funding_source) && (
                    <div className="bg-slate-950 px-4 py-2 rounded-lg border border-slate-800 h-fit w-fit">
                      <span className="text-xs text-slate-500 block uppercase font-medium">Funding</span>
                      <span className="text-sm font-bold text-amber-400">{formatCurrency(milestone.funding_amount)}</span>
                      {milestone.funding_source && (
                        <span className="text-[10px] text-slate-500 block mt-0.5">{milestone.funding_source}</span>
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
