'use client'

import React, { useState, useTransition } from 'react'
import { useRouter } from 'next/navigation'
import { createEntrepreneurialMilestone } from '../lib/api'

export default function EntrepreneurialForm() {
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    venture_name: '',
    role: '',
    stage: 'ideation',
    funding_amount: '',
    funding_source: '',
    launch_date: '',
    description: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    startTransition(async () => {
      try {
        await createEntrepreneurialMilestone({
          venture_name: formData.venture_name,
          role: formData.role,
          stage: formData.stage as any,
          funding_amount: parseFloat(formData.funding_amount) || 0.0,
          funding_source: formData.funding_source || undefined,
          launch_date: formData.launch_date || undefined,
          description: formData.description || undefined,
        })
        
        setFormData({
          venture_name: '',
          role: '',
          stage: 'ideation',
          funding_amount: '',
          funding_source: '',
          launch_date: '',
          description: '',
        })
        setIsOpen(false)
        router.refresh()
      } catch (err: any) {
        setError(err.message || 'Something went wrong')
      }
    })
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="px-5 py-2.5 rounded-lg bg-amber-600 hover:bg-amber-500 font-semibold text-white transition shadow-lg shadow-amber-600/10 text-sm"
      >
        Add Milestone
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-brand-dark/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <header className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h2 className="text-xl font-bold text-white">Add Entrepreneurial Milestone</h2>
              <button 
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-white transition text-sm"
              >
                ✕
              </button>
            </header>

            {error && (
              <div className="p-3 text-xs bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Venture / Startup Name *</label>
                  <input
                    type="text"
                    name="venture_name"
                    required
                    value={formData.venture_name}
                    onChange={handleChange}
                    placeholder="e.g. HealthAI Corp"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Your Role *</label>
                  <input
                    type="text"
                    name="role"
                    required
                    value={formData.role}
                    onChange={handleChange}
                    placeholder="e.g. Co-Founder & CTO"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Current Stage</label>
                  <select
                    name="stage"
                    value={formData.stage}
                    onChange={handleChange}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  >
                    <option value="ideation">Ideation</option>
                    <option value="mvp">MVP Stage</option>
                    <option value="funding">Funding Round</option>
                    <option value="scaling">Scaling / Growth</option>
                    <option value="exited">Exited</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Launch Date</label>
                  <input
                    type="date"
                    name="launch_date"
                    value={formData.launch_date}
                    onChange={handleChange}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Funding Amount (USD)</label>
                  <input
                    type="number"
                    name="funding_amount"
                    value={formData.funding_amount}
                    onChange={handleChange}
                    placeholder="e.g. 50000"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Funding Source</label>
                  <input
                    type="text"
                    name="funding_source"
                    value={formData.funding_source}
                    onChange={handleChange}
                    placeholder="e.g. Angel Investor, Seed Fund"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs text-slate-400 font-semibold">Description (Optional)</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={3}
                  placeholder="Outline the startup domain, targets achieved, and upcoming milestones..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-500 resize-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-2 rounded-lg border border-slate-800 hover:bg-slate-800 text-xs font-semibold text-slate-400 hover:text-white transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isPending}
                  className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-xs font-semibold text-white transition disabled:opacity-50"
                >
                  {isPending ? 'Saving...' : 'Save Milestone'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
