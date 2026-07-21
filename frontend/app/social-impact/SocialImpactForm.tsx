'use client'

import React, { useState, useTransition } from 'react'
import { useRouter } from 'next/navigation'
import { createSocialImpactMilestone } from '../lib/api'

export default function SocialImpactForm() {
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    organization: '',
    cause_area: '',
    role: '',
    hours_volunteered: '',
    initiatives_led: '',
    scale_metric: '',
    date: '',
    description: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
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
        await createSocialImpactMilestone({
          organization: formData.organization,
          cause_area: formData.cause_area,
          role: formData.role,
          hours_volunteered: parseFloat(formData.hours_volunteered) || 0.0,
          initiatives_led: parseInt(formData.initiatives_led, 10) || 0,
          scale_metric: formData.scale_metric || undefined,
          date: formData.date || undefined,
          description: formData.description || undefined,
        })
        
        setFormData({
          organization: '',
          cause_area: '',
          role: '',
          hours_volunteered: '',
          initiatives_led: '',
          scale_metric: '',
          date: '',
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
        className="px-5 py-2.5 rounded-lg bg-purple-600 hover:bg-purple-500 font-semibold text-white transition shadow-lg shadow-purple-600/10 text-sm"
      >
        Add Milestone
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-brand-dark/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <header className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h2 className="text-xl font-bold text-white">Add Social Impact Milestone</h2>
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
                  <label className="text-xs text-slate-400 font-semibold">Organization / NGO *</label>
                  <input
                    type="text"
                    name="organization"
                    required
                    value={formData.organization}
                    onChange={handleChange}
                    placeholder="e.g. Red Cross, Local Shelter"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
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
                    placeholder="e.g. Campaign Lead, Volunteer"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Cause / Campaign Area *</label>
                  <input
                    type="text"
                    name="cause_area"
                    required
                    value={formData.cause_area}
                    onChange={handleChange}
                    placeholder="e.g. Environment, Literacy"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Date</label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Hours Invested</label>
                  <input
                    type="number"
                    name="hours_volunteered"
                    value={formData.hours_volunteered}
                    onChange={handleChange}
                    placeholder="e.g. 45"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs text-slate-400 font-semibold">Initiatives Led</label>
                  <input
                    type="number"
                    name="initiatives_led"
                    value={formData.initiatives_led}
                    onChange={handleChange}
                    placeholder="e.g. 2"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
                  />
                </div>
                <div className="space-y-1 col-span-1 sm:col-span-1">
                  <label className="text-xs text-slate-400 font-semibold">Scale Reach</label>
                  <input
                    type="text"
                    name="scale_metric"
                    value={formData.scale_metric}
                    onChange={handleChange}
                    placeholder="e.g. 150+ students"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
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
                  placeholder="Outline activities, social issues addressed, and local impact..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 resize-none"
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
                  className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white transition disabled:opacity-50"
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
