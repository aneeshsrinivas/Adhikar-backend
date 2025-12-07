export interface Scheme {
  id: string;
  name: string;
  ministry: string;
  category: 'Education' | 'Healthcare' | 'Housing' | 'Employment' | 'Food Security' | 'Agriculture';
  eligibilityMatch: number;
  benefitAmount: string;
  status: 'Active' | 'Pending' | 'Approved' | 'Not Started';
  description: string;
}

export interface User {
  name: string;
  location: string;
  pendingApplications: number;
  language: string;
}

export interface StatCard {
  label: string;
  value: string | number;
  subValue?: string;
  color: 'green' | 'orange' | 'blue' | 'purple';
  icon: any;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  time: string;
  read: boolean;
  type: 'info' | 'success' | 'alert';
}