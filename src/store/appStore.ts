import { create } from 'zustand';

export type Page =
  | 'landing'
  | 'register'
  | 'verify'
  | 'login'
  | 'admin-login'
  | 'loading'
  | 'admin-loading'
  | 'student-dashboard'
  | 'admin-dashboard';

export interface Student {
  id: string;
  studentId: string;
  email: string;
  firstName: string;
  lastName: string;
  filiereCategory: string;
  filiere: string;
  niveau: string;
  anneeScolaire: string;
  city: string | null;
  phone: string | null;
  photoUrl: string | null;
  status: string;
}

export interface Grade {
  id: string;
  studentId: string;
  matiere: string;
  type: string;
  note: string;
  coefficient: number | null;
  semestre: string;
  anneeScolaire: string;
  comment: string | null;
  createdAt: string;
}

export interface Payment {
  id: string;
  studentId: string;
  mois: string;
  montant: number;
  datePaiement: string | null;
  statut: string;
  anneeScolaire: string;
  createdAt: string;
}

export interface Notification {
  id: string;
  studentId: string;
  titre: string;
  message: string;
  type: string;
  lu: boolean;
  createdAt: string;
}

interface AppStore {
  // Navigation
  currentPage: Page;
  setPage: (page: Page) => void;

  // Auth - Student
  student: Student | null;
  setStudent: (s: Student | null) => void;

  // Auth - Admin
  isAdmin: boolean;
  setAdmin: (v: boolean) => void;
  adminEmail: string;
  setAdminEmail: (e: string) => void;

  // Registration
  registeredEmail: string;
  registeredStudentId: string;
  registeredCode: string;
  setRegistration: (email: string, studentId: string, code: string) => void;

  // Student data
  grades: Grade[];
  setGrades: (g: Grade[]) => void;
  payments: Payment[];
  setPayments: (p: Payment[]) => void;
  notifications: Notification[];
  setNotifications: (n: Notification[]) => void;

  // Admin selected student
  selectedStudent: Record<string, unknown> | null;
  setSelectedStudent: (s: Record<string, unknown> | null) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  currentPage: 'landing',
  setPage: (page) => set({ currentPage: page }),

  student: null,
  setStudent: (s) => set({ student: s }),

  isAdmin: false,
  setAdmin: (v) => set({ isAdmin: v }),
  adminEmail: '',
  setAdminEmail: (e) => set({ adminEmail: e }),

  registeredEmail: '',
  registeredStudentId: '',
  registeredCode: '',
  setRegistration: (email, studentId, code) => set({ registeredEmail: email, registeredStudentId: studentId, registeredCode: code }),

  grades: [],
  setGrades: (g) => set({ grades: g }),
  payments: [],
  setPayments: (p) => set({ payments: p }),
  notifications: [],
  setNotifications: (n) => set({ notifications: n }),

  selectedStudent: null,
  setSelectedStudent: (s) => set({ selectedStudent: s }),
}));