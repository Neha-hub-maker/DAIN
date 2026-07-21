const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers = new Headers(options.headers);
  if (options.body && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(url, {
    ...options,
    headers,
    // Add default caching rules if needed. For development, we keep it fresh.
    cache: 'no-store',
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error (${response.status}): ${errorText || response.statusText}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

// ----------------------------------------------------
 //ACADEMIC MILESTONES API
// ----------------------------------------------------
export interface AcademicMilestone {
  id: number;
  user_id: number;
  type: 'publication' | 'research' | 'cgpa' | 'other';
  title: string;
  institution: string;
  value?: string;
  date?: string;
  description?: string;
  created_at: string;
}

export async function getAcademicMilestones(): Promise<AcademicMilestone[]> {
  return fetchAPI('/academic/');
}

export async function createAcademicMilestone(data: Omit<AcademicMilestone, 'id' | 'user_id' | 'created_at'>): Promise<AcademicMilestone> {
  return fetchAPI('/academic/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ----------------------------------------------------
// PROFESSIONAL MILESTONES API
// ----------------------------------------------------
export interface ProfessionalMilestone {
  id: number;
  user_id: number;
  company: string;
  role: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  industry_sector?: string;
  description?: string;
  created_at: string;
}

export async function getProfessionalMilestones(): Promise<ProfessionalMilestone[]> {
  return fetchAPI('/professional/');
}

export async function createProfessionalMilestone(data: Omit<ProfessionalMilestone, 'id' | 'user_id' | 'created_at'>): Promise<ProfessionalMilestone> {
  return fetchAPI('/professional/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ----------------------------------------------------
// ENTREPRENEURIAL MILESTONES API
// ----------------------------------------------------
export interface EntrepreneurialMilestone {
  id: number;
  user_id: number;
  venture_name: string;
  role: string;
  stage: 'ideation' | 'mvp' | 'funding' | 'scaling' | 'exited' | 'other';
  funding_amount: number;
  funding_source?: string;
  launch_date?: string;
  description?: string;
  created_at: string;
}

export async function getEntrepreneurialMilestones(): Promise<EntrepreneurialMilestone[]> {
  return fetchAPI('/entrepreneurial/');
}

export async function createEntrepreneurialMilestone(data: Omit<EntrepreneurialMilestone, 'id' | 'user_id' | 'created_at'>): Promise<EntrepreneurialMilestone> {
  return fetchAPI('/entrepreneurial/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ----------------------------------------------------
// SOCIAL IMPACT MILESTONES API
// ----------------------------------------------------
export interface SocialImpactMilestone {
  id: number;
  user_id: number;
  organization: string;
  cause_area: string;
  role: string;
  hours_volunteered: number;
  initiatives_led: number;
  scale_metric?: string;
  date?: string;
  description?: string;
  created_at: string;
}

export async function getSocialImpactMilestones(): Promise<SocialImpactMilestone[]> {
  return fetchAPI('/social-impact/');
}

export async function createSocialImpactMilestone(data: Omit<SocialImpactMilestone, 'id' | 'user_id' | 'created_at'>): Promise<SocialImpactMilestone> {
  return fetchAPI('/social-impact/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ----------------------------------------------------
// PERSONAL MILESTONES API
// ----------------------------------------------------
export interface PersonalMilestone {
  id: number;
  user_id: number;
  category: 'extracurricular' | 'skill' | 'hobby' | 'other';
  title: string;
  status: 'in_progress' | 'achieved';
  date_achieved?: string;
  description?: string;
  created_at: string;
}

export async function getPersonalMilestones(): Promise<PersonalMilestone[]> {
  return fetchAPI('/personal/');
}

export async function createPersonalMilestone(data: Omit<PersonalMilestone, 'id' | 'user_id' | 'created_at'>): Promise<PersonalMilestone> {
  return fetchAPI('/personal/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}
