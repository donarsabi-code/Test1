import { create } from 'zustand';

export type Page =
  | 'landing'
  | 'register'
  | 'verify'
  | 'verification-steps'
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
  dateOfBirth?: string | null;
  address?: string | null;
  nationality?: string | null;
  genre?: string | null;
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

// ─── Persisted keys (survive page refresh) ───
const PERSIST_KEY = 'estam_app_state';

function loadPersistedState() {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(PERSIST_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch { return null; }
}

function savePersistedState(partial: Record<string, unknown>) {
  if (typeof window === 'undefined') return;
  try {
    const existing = loadPersistedState() || {};
    const merged = { ...existing, ...partial };
    localStorage.setItem(PERSIST_KEY, JSON.stringify(merged));
  } catch { /* ignore */ }
}

function clearPersistedState() {
  if (typeof window === 'undefined') return;
  try { localStorage.removeItem(PERSIST_KEY); } catch { /* ignore */ }
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

  // Notification reply
  notificationReplies: Record<string, string>;
  setNotificationReply: (notifId: string, reply: string) => void;

  // Session restore
  hydrated: boolean;
  hydrate: () => void;
  logout: () => void;
}

export const useAppStore = create<AppStore>((set, get) => ({
  currentPage: 'landing',
  setPage: (page) => {
    set({ currentPage: page });
    // Persist page only for dashboard pages (skip loading/transitions)
    if (page === 'student-dashboard' || page === 'admin-dashboard') {
      savePersistedState({ currentPage: page });
    }
  },

  student: null,
  setStudent: (s) => {
    set({ student: s });
    if (s) {
      savePersistedState({ student: s });
    }
  },

  isAdmin: false,
  setAdmin: (v) => {
    set({ isAdmin: v });
    savePersistedState({ isAdmin: v });
  },
  adminEmail: '',
  setAdminEmail: (e) => {
    set({ adminEmail: e });
    savePersistedState({ adminEmail: e });
  },

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

  notificationReplies: {},
  setNotificationReply: (notifId, reply) => set((state) => ({
    notificationReplies: { ...state.notificationReplies, [notifId]: reply }
  })),

  hydrated: false,
  hydrate: () => {
    const persisted = loadPersistedState();
    if (!persisted) {
      set({ hydrated: true });
      return;
    }

    const student = persisted.student || null;
    const isAdmin = persisted.isAdmin || false;
    const adminEmail = persisted.adminEmail || '';
    const currentPage = persisted.currentPage || 'landing';

    // Only restore to dashboard if there's a valid session
    if (student && (currentPage === 'student-dashboard')) {
      set({
        student,
        currentPage: 'student-dashboard',
        hydrated: true,
      });
    } else if (isAdmin && adminEmail && currentPage === 'admin-dashboard') {
      set({
        isAdmin: true,
        adminEmail,
        currentPage: 'admin-dashboard',
        hydrated: true,
      });
    } else {
      // Session expired or invalid, clear and go to landing
      clearPersistedState();
      set({ hydrated: true });
    }
  },

  logout: () => {
    clearPersistedState();
    set({
      student: null,
      isAdmin: false,
      adminEmail: '',
      grades: [],
      payments: [],
      notifications: [],
      currentPage: 'landing',
      selectedStudent: null,
      notificationReplies: {},
    });
  },
}));
