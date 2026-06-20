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
  | 'admin-dashboard'
  | 'mini-register'
  | 'mini-login'
  | 'mini-admin-login';

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

// ─── Persist all state to localStorage ───
const PERSIST_KEY = 'estam_app_state';

function loadPersistedState(): Record<string, unknown> | null {
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
  currentPage: Page;
  setPage: (page: Page) => void;

  student: Student | null;
  setStudent: (s: Student | null) => void;

  isAdmin: boolean;
  setAdmin: (v: boolean) => void;
  adminEmail: string;
  setAdminEmail: (e: string) => void;

  registeredEmail: string;
  registeredStudentId: string;
  registeredCode: string;
  setRegistration: (email: string, studentId: string, code: string) => void;

  grades: Grade[];
  setGrades: (g: Grade[]) => void;
  payments: Payment[];
  setPayments: (p: Payment[]) => void;
  notifications: Notification[];
  setNotifications: (n: Notification[]) => void;

  selectedStudent: Record<string, unknown> | null;
  setSelectedStudent: (s: Record<string, unknown> | null) => void;

  notificationReplies: Record<string, string>;
  setNotificationReply: (notifId: string, reply: string) => void;

  hydrated: boolean;
  hydrate: () => void;
  logout: () => void;
}

export const useAppStore = create<AppStore>((set, get) => ({
  currentPage: 'landing',
  setPage: (page) => {
    set({ currentPage: page });
    // Persist EVERY page change so refresh never loses position
    savePersistedState({ currentPage: page });
  },

  student: null,
  setStudent: (s) => {
    set({ student: s });
    savePersistedState({ student: s });
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
  setRegistration: (email, studentId, code) => {
    set({ registeredEmail: email, registeredStudentId: studentId, registeredCode: code });
    savePersistedState({ registeredEmail: email, registeredStudentId: studentId, registeredCode: code });
  },

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

    const restoredState: Record<string, unknown> = { hydrated: true };

    // Restore page — for loading pages, convert back to target
    const currentPage = persisted.currentPage as Page | undefined;
    if (currentPage) {
      // Skip loading/transition pages on restore — go directly to target
      if (currentPage === 'loading') restoredState.currentPage = 'student-dashboard';
      else if (currentPage === 'admin-loading') restoredState.currentPage = 'admin-dashboard';
      else if (currentPage === 'mini-register') restoredState.currentPage = 'register';
      else if (currentPage === 'mini-login') restoredState.currentPage = 'login';
      else if (currentPage === 'mini-admin-login') restoredState.currentPage = 'admin-login';
      else restoredState.currentPage = currentPage;
    }

    // Restore student session if available
    if (persisted.student) {
      restoredState.student = persisted.student;
      // If we restored a dashboard page but no student, go to landing
      if (currentPage === 'student-dashboard' || currentPage === 'loading') {
        restoredState.currentPage = 'student-dashboard';
      }
    } else if ((currentPage === 'student-dashboard' || currentPage === 'loading') && !persisted.student) {
      restoredState.currentPage = 'landing';
    }

    // Restore admin session if available
    if (persisted.isAdmin && persisted.adminEmail) {
      restoredState.isAdmin = true;
      restoredState.adminEmail = persisted.adminEmail;
      if (currentPage === 'admin-dashboard' || currentPage === 'admin-loading') {
        restoredState.currentPage = 'admin-dashboard';
      }
    } else if ((currentPage === 'admin-dashboard' || currentPage === 'admin-loading') && !persisted.isAdmin) {
      restoredState.currentPage = 'landing';
    }

    // Restore registration data
    if (persisted.registeredEmail) restoredState.registeredEmail = persisted.registeredEmail;
    if (persisted.registeredStudentId) restoredState.registeredStudentId = persisted.registeredStudentId;
    if (persisted.registeredCode) restoredState.registeredCode = persisted.registeredCode;

    set(restoredState);
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
      registeredEmail: '',
      registeredStudentId: '',
      registeredCode: '',
    });
  },
}));
