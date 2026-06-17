#!/usr/bin/env python3
"""Generate the main page.tsx for ESTAM student management app."""

content = r"""'use client'

import { useState, useEffect, useRef, type FormEvent } from 'react'
import { motion, useInView, AnimatePresence } from 'framer-motion'
import { useAppStore, type Page, type Student, type Grade, type Payment, type Notification } from '@/store/appStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Progress } from '@/components/ui/progress'
import QRCode from 'qrcode'
import {
  GraduationCap, BookOpen, Users, Bell, LogOut, Settings, Search,
  User, Mail, Lock, Phone, MapPin, Calendar, ChevronRight, Award,
  CreditCard, CheckCircle2, XCircle, AlertCircle, Eye, EyeOff,
  Menu, X, ArrowLeft, Building2, BarChart3, FileText, Shield,
  Trash2, Send, Edit3, Save, Check, Megaphone, Clock, Loader2,
  Download, QrCode, MessageSquare, UsersRound, Globe, Camera
} from 'lucide-react'

// ─── Data Constants ───
const FILIERES: Record<string, string[]> = {
  Gestion: [
    'Comptabilité et Gestion',
    'Finance, Banque et Assurances',
    'Marketing et Action Commerciale',
    'Gestion des Ressources Humaines',
    'Gestion Commerciale',
    'Transport et Logistique',
    'Communication et Marketing',
  ],
  Technologie: [
    'Génie Civil',
    'Génie Électrique',
    'Informatique de Gestion',
    'Réseaux Informatiques et Télécommunications',
    'Audit Sécurité et Systèmes des Réseaux Informatiques',
    'Informatique Industriel et Maintenance',
  ],
}

const MOIS = ['Octobre', 'Novembre', 'Décembre', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Septembre']

const LOGO = '/estam/IMG_1693.png'

// ─── Reveal Animation Wrapper ───
function Reveal({ children, className = '', delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-50px' })
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.6, delay, ease: 'easeOut' }}
      className={className}
    >
      {children}
    </motion.div>
  )
}

// ─── Mini Loading (brief transition) ───
function MiniLoading({ targetPage }: { targetPage: Page }) {
  const setPage = useAppStore(s => s.setPage)
  useEffect(() => {
    const t = setTimeout(() => setPage(targetPage), 600)
    return () => clearTimeout(t)
  }, [setPage, targetPage])
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black">
      <motion.div animate={{ rotate: 360 }} transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}>
        <Loader2 className="w-10 h-10 text-blue-500" />
      </motion.div>
      <p className="mt-4 text-zinc-400 text-sm">Chargement...</p>
    </div>
  )
}

// ─── Step-by-Step Loading Page (after verification) ───
function VerificationStepsPage() {
  const setPage = useAppStore(s => s.setPage)
  const [step, setStep] = useState(0)
  const steps = [
    { icon: CheckCircle2, label: 'Vérification du code...' },
    { icon: Users, label: 'Activation du compte...' },
    { icon: GraduationCap, label: 'Configuration de l\'espace étudiant...' },
    { icon: BarChart3, label: 'Redirection vers la connexion...' },
  ]

  useEffect(() => {
    const timers = steps.map((_, i) =>
      setTimeout(() => setStep(i), i * 800)
    )
    const finalTimer = setTimeout(() => setPage('login'), steps.length * 800 + 600)
    return () => { timers.forEach(clearTimeout); clearTimeout(finalTimer) }
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black px-4">
      <img src={LOGO} alt="ESTAM" className="w-20 h-20 mx-auto mb-8 rounded-xl object-contain" />
      <div className="w-full max-w-sm space-y-4">
        {steps.map((s, i) => {
          const Icon = s.icon
          const active = i === step
          const done = i < step
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`flex items-center gap-4 p-3 rounded-xl transition-all duration-500 ${
                active ? 'bg-blue-600/10 border border-blue-500/30' : done ? 'bg-green-500/5 border border-green-500/10' : 'bg-zinc-900/50 border border-zinc-800/50'
              }`}
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                active ? 'bg-blue-600' : done ? 'bg-green-500' : 'bg-zinc-800'
              }`}>
                {done ? (
                  <Check className="w-5 h-5 text-white" />
                ) : active ? (
                  <motion.div animate={{ rotate: 360 }} transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}>
                    <Icon className="w-5 h-5 text-white" />
                  </motion.div>
                ) : (
                  <span className="text-zinc-600 text-sm font-bold">{i + 1}</span>
                )}
              </div>
              <div>
                <p className={`text-sm font-medium ${active ? 'text-blue-400' : done ? 'text-green-400' : 'text-zinc-600'}`}>{s.label}</p>
              </div>
              {done && <CheckCircle2 className="w-5 h-5 text-green-400 ml-auto" />}
              {active && <Loader2 className="w-5 h-5 text-blue-400 ml-auto animate-spin" />}
            </motion.div>
          )
        })}
      </div>
      <p className="shimmer-blue text-lg font-bold mt-8 tracking-wider">ESTAM</p>
    </div>
  )
}

// ─── Loading Page (for login transition) ───
function LoadingPage({ targetPage }: { targetPage: Page }) {
  const setPage = useAppStore(s => s.setPage)
  const [progress, setProgress] = useState(0)
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) { clearInterval(interval); return 100 }
        return p + 4
      })
    }, 60)
    const timer = setTimeout(() => setPage(targetPage), 2600)
    return () => { clearInterval(interval); clearTimeout(timer) }
  }, [setPage, targetPage])
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black">
      <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}>
        <GraduationCap className="w-16 h-16 text-blue-500" />
      </motion.div>
      <p className="mt-6 shimmer-blue text-2xl font-bold tracking-wider">ESTAM</p>
      <p className="text-zinc-400 text-sm mt-2">Chargement de votre espace...</p>
      <div className="w-64 mt-6">
        <Progress value={progress} className="h-2 bg-zinc-800 [&>div]:bg-blue-500" />
      </div>
    </div>
  )
}

// ─── Notification Bell Popover ───
function NotificationBell() {
  const { notifications, setNotifications } = useAppStore()
  const [open, setOpen] = useState(false)
  const [selectedNotif, setSelectedNotif] = useState<Notification | null>(null)
  const unreadCount = notifications.filter(n => !n.lu).length

  const markRead = async (id: string) => {
    await fetch('/api/notifications', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ notificationId: id }) })
    setNotifications(notifications.map(n => n.id === id ? { ...n, lu: true } : n))
  }

  const handleOpen = (notif: Notification) => {
    if (!notif.lu) markRead(notif.id)
    setSelectedNotif(notif)
  }

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        className="relative p-2 rounded-lg hover:bg-zinc-800 transition"
      >
        <Bell className="w-5 h-5 text-zinc-400" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 w-5 h-5 bg-blue-600 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      <AnimatePresence>
        {open && (
          <>
            <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
            <div className="notif-popup absolute right-0 top-full mt-2 w-80 sm:w-96 max-h-[70vh] bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl z-50 flex flex-col overflow-hidden">
              <div className="p-3 border-b border-zinc-800 flex items-center justify-between">
                <h3 className="text-white font-semibold text-sm">Notifications</h3>
                <span className="text-zinc-500 text-xs">{unreadCount} non lue(s)</span>
              </div>
              <div className="flex-1 overflow-y-auto">
                {notifications.length === 0 ? (
                  <div className="p-8 text-center text-zinc-500 text-sm">Aucune notification</div>
                ) : (
                  notifications.map(n => (
                    <button
                      key={n.id}
                      onClick={() => handleOpen(n)}
                      className={`w-full text-left p-3 border-b border-zinc-800/50 hover:bg-zinc-800/50 transition ${!n.lu ? 'bg-blue-600/5' : ''}`}
                    >
                      <div className="flex items-start gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${
                          n.type === 'note' ? 'bg-blue-500/20' : n.type === 'paiement' ? 'bg-green-500/20' : 'bg-blue-500/20'
                        }`}>
                          {n.type === 'note' ? <BookOpen className="w-4 h-4 text-blue-400" /> : n.type === 'paiement' ? <CreditCard className="w-4 h-4 text-green-400" /> : <Bell className="w-4 h-4 text-blue-400" />}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <p className="text-white text-sm font-medium truncate">{n.titre}</p>
                            {!n.lu && <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />}
                          </div>
                          <p className="text-zinc-500 text-xs mt-0.5 line-clamp-1">{n.message}</p>
                          <p className="text-zinc-600 text-[10px] mt-1">{new Date(n.createdAt).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}</p>
                        </div>
                      </div>
                    </button>
                  ))
                )}
              </div>
            </div>
          </>
        )}
      </AnimatePresence>

      {/* Notification Detail Modal */}
      <AnimatePresence>
        {selectedNotif && (
          <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/70"
              onClick={() => setSelectedNotif(null)}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                    selectedNotif.type === 'note' ? 'bg-blue-500/20' : selectedNotif.type === 'paiement' ? 'bg-green-500/20' : 'bg-blue-500/20'
                  }`}>
                    {selectedNotif.type === 'note' ? <BookOpen className="w-6 h-6 text-blue-400" /> : selectedNotif.type === 'paiement' ? <CreditCard className="w-6 h-6 text-green-400" /> : <Bell className="w-6 h-6 text-blue-400" />}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-white font-semibold text-lg">{selectedNotif.titre}</h3>
                    <p className="text-zinc-500 text-xs mt-1">{new Date(selectedNotif.createdAt).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
                    <Badge className="mt-2 bg-blue-500/20 text-blue-400 text-xs capitalize">{selectedNotif.type}</Badge>
                  </div>
                  <button onClick={() => setSelectedNotif(null)} className="text-zinc-500 hover:text-white"><X className="w-5 h-5" /></button>
                </div>
                <div className="mt-4 p-4 bg-zinc-800 rounded-xl">
                  <p className="text-zinc-300 text-sm leading-relaxed whitespace-pre-wrap">{selectedNotif.message}</p>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  )
}

// ─── Generate PDF ───
async function generateStudentPDF(studentData: Record<string, unknown>) {
  const { default: jsPDF } = await import('jspdf')
  const doc = new jsPDF()
  const s = studentData

  // Header
  doc.setFillColor(37, 99, 235)
  doc.rect(0, 0, 210, 40, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(20)
  doc.text('ESTAM', 15, 20)
  doc.setFontSize(10)
  doc.text('Ecole Superieure des Technologies Avancees et de Management', 15, 30)

  // Student Info
  doc.setTextColor(0, 0, 0)
  doc.setFontSize(16)
  doc.text('Fiche Etudiant', 15, 55)

  doc.setFontSize(11)
  const fields = [
    ['Identifiant', String(s.studentId || '-')],
    ['Nom complet', `${String(s.firstName || '')} ${String(s.lastName || '')}`],
    ['Email', String(s.email || '-')],
    ['Telephone', String(s.phone || '-')],
    ['Ville', String(s.city || '-')],
    ['Nationalite', String(s.nationality || '-')],
    ['Genre', String(s.genre === 'M' ? 'Masculin' : s.genre === 'F' ? 'Feminin' : '-')],
    ['Date de naissance', String(s.dateOfBirth || '-')],
    ['Adresse', String(s.address || '-')],
    ['Filiere', String(s.filiere || '-')],
    ['Domaine', String(s.filiereCategory || '-')],
    ['Niveau', String(s.niveau || '-')],
    ['Annee scolaire', String(s.anneeScolaire || '-')],
    ['Statut', String(s.status || '-')],
    ['Verifie', String(s.verified === true ? 'Oui' : 'Non')],
  ]

  let y = 65
  for (const [label, value] of fields) {
    doc.setFont(undefined, 'bold')
    doc.setTextColor(80, 80, 80)
    doc.text(`${label} :`, 15, y)
    doc.setFont(undefined, 'normal')
    doc.setTextColor(0, 0, 0)
    doc.text(value, 75, y)
    y += 10
  }

  // Grades
  const grades = (s.grades as Record<string, string>[]) || []
  if (grades.length > 0) {
    y += 5
    doc.setFontSize(14)
    doc.setTextColor(37, 99, 235)
    doc.text('Notes', 15, y)
    y += 8
    doc.setFontSize(9)
    doc.setTextColor(100, 100, 100)
    doc.text('Matiere', 15, y)
    doc.text('Type', 80, y)
    doc.text('Note', 120, y)
    doc.text('Semestre', 150, y)
    y += 2
    doc.setDrawColor(200, 200, 200)
    doc.line(15, y, 195, y)
    y += 6
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(10)
    for (const g of grades) {
      if (y > 270) { doc.addPage(); y = 20 }
      doc.text(String(g.matiere || ''), 15, y)
      doc.text(String(g.type || ''), 80, y)
      doc.text(String(g.note || ''), 120, y)
      doc.text(String(g.semestre || ''), 150, y)
      y += 8
    }
  }

  // Payments
  const payments = (s.payments as Record<string, string>[]) || []
  if (payments.length > 0) {
    y += 10
    if (y > 250) { doc.addPage(); y = 20 }
    doc.setFontSize(14)
    doc.setTextColor(37, 99, 235)
    doc.text('Paiements', 15, y)
    y += 8
    doc.setFontSize(9)
    doc.setTextColor(100, 100, 100)
    doc.text('Mois', 15, y)
    doc.text('Montant', 80, y)
    doc.text('Statut', 120, y)
    doc.text('Date', 160, y)
    y += 2
    doc.line(15, y, 195, y)
    y += 6
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(10)
    for (const p of payments) {
      if (y > 270) { doc.addPage(); y = 20 }
      doc.text(String(p.mois || ''), 15, y)
      doc.text(`${Number(p.montant || 0).toLocaleString()} FCFA`, 80, y)
      doc.text(String(p.statut === 'paye' ? 'Paye' : 'Impaye'), 120, y)
      doc.text(String(p.datePaiement || '-'), 160, y)
      y += 8
    }
  }

  // Footer
  const pageCount = doc.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setTextColor(150, 150, 150)
    doc.text(`ESTAM Congo - Fiche etudiante - Genere le ${new Date().toLocaleDateString('fr-FR')}`, 15, 290)
    doc.text(`Page ${i}/${pageCount}`, 180, 290)
  }

  doc.save(`ESTAM_${String(s.studentId || 'etudiant')}.pdf`)
}

// ─── Landing Page ───
function LandingPage() {
  const setPage = useAppStore(s => s.setPage)
  return (
    <div className="min-h-screen bg-black">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-md border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
          <button onClick={() => setPage('landing')} className="flex items-center gap-3 hover:opacity-80 transition">
            <img src={LOGO} alt="ESTAM" className="h-10 w-10 rounded-lg object-cover" />
            <span className="text-blue-500 font-bold text-xl tracking-wider">ESTAM</span>
          </button>
          <div className="hidden md:flex items-center gap-6">
            <button onClick={() => document.getElementById('apropos')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-blue-400 transition text-sm">À propos</button>
            <button onClick={() => document.getElementById('filieres')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-blue-400 transition text-sm">Filières</button>
            <button onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-blue-400 transition text-sm">Contact</button>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" className="border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white text-sm" onClick={() => setPage('mini-login')}>Connexion</Button>
            <Button className="bg-blue-600 text-white hover:bg-blue-700 text-sm" onClick={() => setPage('mini-register')}>S&apos;inscrire</Button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        <div className="absolute inset-0">
          <img src="/estam/IMG_1628.jpeg" alt="ESTAM Campus" className="w-full h-full object-cover opacity-30" />
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/80 to-black" />
        </div>
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
          <Reveal>
            <img src={LOGO} alt="ESTAM Logo" className="w-28 h-28 mx-auto rounded-2xl border-4 border-blue-500/30 mb-6 object-contain" />
          </Reveal>
          <Reveal delay={0.1}>
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-4">
              <span className="shimmer-blue text-4xl sm:text-6xl font-bold">ESTAM</span>
            </h1>
          </Reveal>
          <Reveal delay={0.2}>
            <p className="text-lg sm:text-xl text-zinc-300 mb-2">École Supérieure des Technologies Avancées et de Management</p>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="shimmer-text text-blue-400 font-semibold italic text-lg mb-8">&laquo; Une formation, un métier, une réussite &raquo;</p>
          </Reveal>
          <Reveal delay={0.4}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-blue-600 text-white hover:bg-blue-700 text-base px-8 py-6" onClick={() => setPage('mini-register')}>
                <GraduationCap className="w-5 h-5 mr-2" /> S&apos;inscrire maintenant
              </Button>
              <Button size="lg" variant="outline" className="border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white text-base px-8 py-6" onClick={() => setPage('mini-login')}>
                <LogIn className="w-5 h-5 mr-2" /> Se connecter
              </Button>
            </div>
          </Reveal>
        </div>
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ChevronRight className="w-6 h-6 text-blue-500 rotate-90" />
        </div>
      </section>

      {/* About Section */}
      <section id="apropos" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <Reveal>
            <h2 className="shimmer-blue text-3xl sm:text-4xl font-bold text-center text-white mb-4">À propos de l&apos;ESTAM</h2>
            <div className="w-20 h-1 bg-blue-600 mx-auto mb-12" />
          </Reveal>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <Reveal delay={0.1}>
              <div className="space-y-6">
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;<strong className="text-blue-400">École Supérieure des Technologies Avancées et de Management (ESTAM)</strong> est un établissement d&apos;enseignement supérieur privé situé en <strong className="text-white">République du Congo</strong>, avec des campus à <strong className="text-white">Brazzaville</strong> et <strong className="text-white">Pointe-Noire</strong>. Créée par arrêté <strong className="text-blue-400">N° 0076/MES-CAB-DGESUP</strong>, l&apos;ESTAM travaille en étroite collaboration avec l&apos;Université CEREC-ISCOM.
                </p>
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;ESTAM a pour mission d&apos;offrir des programmes d&apos;études innovants, une formation professionnelle et personnelle de qualité, axée sur l&apos;excellence, l&apos;innovation et l&apos;inclusion. Elle prépare les étudiants aux défis du monde professionnel à travers des formations en <strong className="text-white">Gestion</strong> et en <strong className="text-white">Technologie</strong>.
                </p>
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <BookOpen className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">9+</p>
                    <p className="text-zinc-400 text-sm">Filières</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Users className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">2</p>
                    <p className="text-zinc-400 text-sm">Campus</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Award className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">Licence</p>
                    <p className="text-zinc-400 text-sm">Diplôme</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Building2 className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">CEREC</p>
                    <p className="text-zinc-400 text-sm">Partenaire</p>
                  </div>
                </div>
              </div>
            </Reveal>
            <Reveal delay={0.2}>
              <div className="space-y-4">
                <img src="/estam/IMG_1625.jpeg" alt="ESTAM" className="rounded-xl w-full h-64 object-cover border border-zinc-800" />
                <div className="grid grid-cols-2 gap-4">
                  <img src="/estam/IMG_1624.jpeg" alt="ESTAM" className="rounded-xl h-40 object-cover border border-zinc-800 w-full" />
                  <img src="/estam/IMG_1623.jpeg" alt="ESTAM" className="rounded-xl h-40 object-cover border border-zinc-800 w-full" />
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* Filières Section */}
      <section id="filieres" className="py-20 px-4 bg-zinc-950">
        <div className="max-w-6xl mx-auto">
          <Reveal>
            <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">Nos Filières</h2>
            <div className="w-20 h-1 bg-blue-600 mx-auto mb-4" />
            <p className="text-zinc-400 text-center max-w-2xl mx-auto mb-12">Des formations professionnelles en Licence dans les domaines de la Gestion et de la Technologie</p>
          </Reveal>
          {Object.entries(FILIERES).map(([category, fils], idx) => (
            <Reveal key={category} delay={idx * 0.2}>
              <div className="mb-12">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-blue-600/10 flex items-center justify-center">
                    {category === 'Gestion' ? <BarChart3 className="w-6 h-6 text-blue-500" /> : <Settings className="w-6 h-6 text-blue-500" />}
                  </div>
                  <h3 className="text-2xl font-bold text-white">{category}</h3>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {fils.map((f, i) => (
                    <motion.div
                      key={f}
                      whileHover={{ scale: 1.03, borderColor: 'rgb(37, 99, 235)' }}
                      className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 cursor-default transition-all"
                    >
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 rounded bg-blue-600/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-blue-400 text-sm font-bold">{i + 1}</span>
                        </div>
                        <div>
                          <h4 className="text-white font-semibold text-sm">{f}</h4>
                          <p className="text-zinc-500 text-xs mt-1">Licence 3 ans</p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Inscription Info */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Reveal>
            <h2 className="shimmer-blue text-3xl sm:text-4xl font-bold text-center text-white mb-4">Inscription</h2>
            <div className="w-20 h-1 bg-blue-600 mx-auto mb-12" />
          </Reveal>
          <div className="grid sm:grid-cols-2 gap-6">
            <Reveal delay={0.1}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-blue-400 flex items-center gap-2"><FileText className="w-5 h-5" /> Nouvelle inscription</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Frais d&apos;inscription : <span className="text-blue-400 font-bold text-lg">26 000 FCFA</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Ouvert lun-ven 8h-17h, sam 8h-12h</p>
                </CardContent>
              </Card>
            </Reveal>
            <Reveal delay={0.2}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-blue-400 flex items-center gap-2"><Clock className="w-5 h-5" /> Cours du soir</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Vague Soir : <span className="shimmer-blue font-bold text-lg">Disponible</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Pour les travailleurs, cours du soir aménagés</p>
                </CardContent>
              </Card>
            </Reveal>
          </div>
          <Reveal delay={0.3}>
            <div className="text-center mt-10">
              <img src="/estam/IMG_1626.png" alt="ESTAM Document" className="mx-auto rounded-xl max-h-64 border border-zinc-800 object-contain" />
            </div>
          </Reveal>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 bg-zinc-950">
        <div className="max-w-4xl mx-auto">
          <Reveal>
            <h2 className="shimmer-blue text-3xl sm:text-4xl font-bold text-center text-white mb-4">Contact</h2>
            <div className="w-20 h-1 bg-blue-600 mx-auto mb-12" />
          </Reveal>
          <div className="grid sm:grid-cols-2 gap-6">
            <Reveal delay={0.1}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Brazzaville</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><MapPin className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> 233 Rue de la Libération / 22 Rue Likouala, Poto-Poto</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> +242 06 822 91 78</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> +242 05 557 58 32 (WhatsApp)</p>
                </CardContent>
              </Card>
            </Reveal>
            <Reveal delay={0.2}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Pointe-Noire</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><MapPin className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> 82 Avenue Nelson Mandela, rd-pt ILAMA</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Mail className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> info@estamuni.net</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Globe className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" /> estam.cg</p>
                </CardContent>
              </Card>
            </Reveal>
          </div>
          <Reveal delay={0.3}>
            <div className="mt-10 text-center">
              <img src="/estam/IMG_1625.jpeg" alt="ESTAM Campus" className="mx-auto rounded-xl max-h-72 object-cover border border-zinc-800 w-full" />
            </div>
          </Reveal>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8 px-4">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <img src={LOGO} alt="ESTAM" className="w-8 h-8 rounded-lg object-cover" />
            <span className="text-blue-500 font-bold">ESTAM</span>
          </div>
          <p className="text-zinc-500 text-xs text-center">
            © {new Date().getFullYear()} École Supérieure des Technologies Avancées et de Management. Tous droits réservés.
          </p>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" className="text-zinc-500 hover:text-blue-400 text-xs" onClick={() => setPage('mini-admin-login')}>
              <Shield className="w-3 h-3 mr-1" /> Administration
            </Button>
          </div>
        </div>
      </footer>
    </div>
  )
}

// ─── Login Icon ───
function LogIn({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" /><polyline points="10 17 15 12 10 7" /><line x1="15" y1="12" x2="3" y2="12" />
    </svg>
  )
}

// ─── Register Page ───
function RegisterPage() {
  const setPage = useAppStore(s => s.setPage)
  const setRegistration = useAppStore(s => s.setRegistration)
  const [form, setForm] = useState({
    email: '', password: '', firstName: '', lastName: '', dateOfBirth: '', phone: '',
    address: '', city: 'Brazzaville', nationality: 'Congo', genre: 'M',
    filiereCategory: 'Gestion', filiere: '', niveau: 'L1', anneeScolaire: new Date().getFullYear().toString(),
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const update = (k: string, v: string) => {
    const n = { ...form, [k]: v }
    if (k === 'filiereCategory') n.filiere = ''
    setForm(n)
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    if (!form.filiere) { setError('Veuillez sélectionner une filière'); return }
    if (!form.email.toLowerCase().endsWith('@gmail.com')) { setError('Seules les adresses @gmail.com sont acceptées'); return }
    setLoading(true)
    try {
      const res = await fetch('/api/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      const data = await res.json()
      if (!res.ok) { setError(data.error || 'Erreur'); return }
      setRegistration(data.email, data.studentId, data.verificationCode)
      setPage('verify')
    } catch { setError('Erreur de connexion au serveur') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <button onClick={() => setPage('landing')} className="inline-block">
            <img src={LOGO} alt="ESTAM" className="w-16 h-16 rounded-xl mx-auto border-2 border-blue-500/30 object-contain mb-4" />
          </button>
          <h1 className="text-2xl font-bold text-white">Inscription Étudiant</h1>
          <p className="text-zinc-400 text-sm mt-1">Créez votre compte ESTAM</p>
        </div>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div><Label className="text-zinc-300">Prénom *</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.firstName} onChange={e => update('firstName', e.target.value)} required /></div>
                <div><Label className="text-zinc-300">Nom *</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.lastName} onChange={e => update('lastName', e.target.value)} required /></div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div><Label className="text-zinc-300">Email (Gmail uniquement) *</Label><Input type="email" className="mt-1 bg-zinc-800 border-zinc-700 text-white" placeholder="exemple@gmail.com" value={form.email} onChange={e => update('email', e.target.value)} required /></div>
                <div><Label className="text-zinc-300">Mot de passe *</Label><Input type="password" className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.password} onChange={e => update('password', e.target.value)} required /></div>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                <div><Label className="text-zinc-300">Date de naissance</Label><Input type="date" className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.dateOfBirth} onChange={e => update('dateOfBirth', e.target.value)} /></div>
                <div><Label className="text-zinc-300">Genre</Label>
                  <Select value={form.genre} onValueChange={v => update('genre', v)}>
                    <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="M">Masculin</SelectItem><SelectItem value="F">Féminin</SelectItem></SelectContent>
                  </Select>
                </div>
                <div><Label className="text-zinc-300">Téléphone</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.phone} onChange={e => update('phone', e.target.value)} placeholder="+242 06 XXX XX XX" /></div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div><Label className="text-zinc-300">Ville *</Label>
                  <Select value={form.city} onValueChange={v => update('city', v)}>
                    <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="Brazzaville">Brazzaville</SelectItem><SelectItem value="Pointe-Noire">Pointe-Noire</SelectItem></SelectContent>
                  </Select>
                </div>
                <div><Label className="text-zinc-300">Nationalité</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.nationality} onChange={e => update('nationality', e.target.value)} /></div>
              </div>
              <div><Label className="text-zinc-300">Adresse</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.address} onChange={e => update('address', e.target.value)} /></div>
              <Separator className="bg-zinc-700" />
              <div className="grid sm:grid-cols-3 gap-4">
                <div><Label className="text-zinc-300">Domaine *</Label>
                  <Select value={form.filiereCategory} onValueChange={v => update('filiereCategory', v)}>
                    <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="Gestion">Gestion</SelectItem><SelectItem value="Technologie">Technologie</SelectItem></SelectContent>
                  </Select>
                </div>
                <div><Label className="text-zinc-300">Filière *</Label>
                  <Select value={form.filiere || ''} onValueChange={v => update('filiere', v)}>
                    <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue placeholder="Sélectionner" /></SelectTrigger>
                    <SelectContent className="bg-zinc-800 border-zinc-700">
                      {FILIERES[form.filiereCategory]?.map(f => <SelectItem key={f} value={f}>{f}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </div>
                <div><Label className="text-zinc-300">Niveau *</Label>
                  <Select value={form.niveau} onValueChange={v => update('niveau', v)}>
                    <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="L1">Licence 1</SelectItem><SelectItem value="L2">Licence 2</SelectItem><SelectItem value="L3">Licence 3</SelectItem></SelectContent>
                  </Select>
                </div>
              </div>
              {error && <p className="text-red-400 text-sm flex items-center gap-1"><AlertCircle className="w-4 h-4" />{error}</p>}
              <Button type="submit" disabled={loading} className="w-full bg-blue-600 text-white hover:bg-blue-700">
                {loading ? 'Inscription en cours...' : "S'inscrire"}
              </Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <p className="text-zinc-400 text-sm">Déjà inscrit ? <button onClick={() => setPage('mini-login')} className="text-blue-400 hover:underline">Se connecter</button></p>
              <button onClick={() => setPage('landing')} className="text-zinc-500 hover:text-zinc-300 text-xs flex items-center gap-1 mx-auto"><ArrowLeft className="w-3 h-3" /> Retour à l&apos;accueil</button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// ─── Verify Page ───
function VerifyPage() {
  const { registeredEmail, registeredStudentId, registeredCode, setPage } = useAppStore()
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await fetch('/api/auth/verify', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ studentId: registeredStudentId, code }) })
      const data = await res.json()
      if (!res.ok) { setError(data.error || 'Erreur'); return }
      setPage('verification-steps')
    } catch { setError('Erreur de connexion') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="w-full max-w-md">
        <button onClick={() => setPage('landing')} className="inline-block mb-4">
          <img src={LOGO} alt="ESTAM" className="w-14 h-14 rounded-xl mx-auto object-contain" />
        </button>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="text-center">
            <CheckCircle2 className="w-12 h-12 text-blue-500 mx-auto mb-4" />
            <CardTitle className="text-white text-xl">Inscription réussie !</CardTitle>
            <CardDescription className="text-zinc-400">Vérifiez votre boîte email Gmail</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-zinc-800 rounded-lg p-4 space-y-2">
              <p className="text-zinc-400 text-xs">Votre identifiant étudiant</p>
              <p className="text-blue-400 font-bold text-lg font-mono">{registeredStudentId}</p>
              <p className="text-zinc-400 text-xs">Email : {registeredEmail}</p>
            </div>
            <p className="text-zinc-300 text-sm text-center">Un code de vérification a été envoyé à votre adresse email. Saisissez-le ci-dessous :</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input className="bg-zinc-800 border-zinc-700 text-white text-center text-2xl tracking-[0.5em] font-mono" maxLength={6} value={code} onChange={e => setCode(e.target.value.replace(/\D/g, ''))} placeholder="000000" required />
              {error && <p className="text-red-400 text-sm text-center flex items-center justify-center gap-1"><AlertCircle className="w-4 h-4" />{error}</p>}
              <Button type="submit" disabled={loading} className="w-full bg-blue-600 text-white hover:bg-blue-700">{loading ? 'Vérification...' : 'Vérifier mon compte'}</Button>
            </form>
            <p className="text-zinc-500 text-xs text-center">(Code de test : {registeredCode})</p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// ─── Login Page ───
function LoginPage() {
  const { setPage, setStudent, setGrades, setPayments, setNotifications } = useAppStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) })
      const data = await res.json()
      if (!res.ok) {
        if (data.needsVerification) setError('Compte non vérifié. Veuillez vérifier votre email.')
        else setError(data.error || 'Identifiants incorrects')
        return
      }
      setStudent(data.student)
      setNotifications(data.notifications || [])
      const [gRes, pRes] = await Promise.all([
        fetch(`/api/grades?studentDbId=${data.student.id}`),
        fetch(`/api/payments?studentDbId=${data.student.id}`),
      ])
      const gData = await gRes.json()
      const pData = await pRes.json()
      setGrades(gData.grades || [])
      setPayments(pData.payments || [])
      setPage('loading')
    } catch { setError('Erreur de connexion au serveur') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="text-center mb-8">
          <button onClick={() => setPage('landing')} className="inline-block">
            <img src={LOGO} alt="ESTAM" className="w-16 h-16 rounded-xl mx-auto border-2 border-blue-500/30 object-contain mb-4" />
          </button>
          <h1 className="text-2xl font-bold text-white">Connexion Étudiant</h1>
          <p className="text-zinc-400 text-sm mt-1">Accédez à votre espace ESTAM</p>
        </div>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label className="text-zinc-300">Email</Label>
                <div className="relative mt-1">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                  <Input className="pl-10 bg-zinc-800 border-zinc-700 text-white" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
                </div>
              </div>
              <div>
                <Label className="text-zinc-300">Mot de passe</Label>
                <div className="relative mt-1">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                  <Input className="pl-10 pr-10 bg-zinc-800 border-zinc-700 text-white" type={showPw ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)} required />
                  <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300">
                    {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>
              {error && <p className="text-red-400 text-sm flex items-center gap-1"><AlertCircle className="w-4 h-4" />{error}</p>}
              <Button type="submit" disabled={loading} className="w-full bg-blue-600 text-white hover:bg-blue-700">{loading ? 'Connexion...' : 'Se connecter'}</Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <p className="text-zinc-400 text-sm">Pas encore de compte ? <button onClick={() => setPage('mini-register')} className="text-blue-400 hover:underline">S&apos;inscrire</button></p>
              <button onClick={() => setPage('mini-admin-login')} className="text-zinc-500 hover:text-blue-400 text-xs">Accès Administration</button>
              <br />
              <button onClick={() => setPage('landing')} className="text-zinc-500 hover:text-zinc-300 text-xs flex items-center gap-1 mx-auto"><ArrowLeft className="w-3 h-3" /> Retour</button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// ─── Admin Login Page ───
function AdminLoginPage() {
  const { setPage, setAdmin, setAdminEmail } = useAppStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await fetch('/api/admin/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) })
      const data = await res.json()
      if (!res.ok) { setError(data.error || 'Identifiants incorrects'); return }
      setAdmin(true)
      setAdminEmail(data.admin.email)
      setPage('admin-loading')
    } catch { setError('Erreur de connexion') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="text-center mb-8">
          <button onClick={() => setPage('landing')} className="inline-block">
            <img src={LOGO} alt="ESTAM" className="w-16 h-16 rounded-xl mx-auto border-2 border-blue-500/30 object-contain mb-4" />
          </button>
          <Shield className="w-10 h-10 text-blue-500 mx-auto mb-2" />
          <h1 className="text-2xl font-bold text-white">Administration ESTAM</h1>
          <p className="text-zinc-400 text-sm mt-1">Connexion administrateur</p>
        </div>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label className="text-zinc-300">Email administrateur</Label>
                <Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={email} onChange={e => setEmail(e.target.value)} required placeholder="admin@estam.cg" />
              </div>
              <div>
                <Label className="text-zinc-300">Mot de passe</Label>
                <Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
              </div>
              {error && <p className="text-red-400 text-sm flex items-center gap-1"><AlertCircle className="w-4 h-4" />{error}</p>}
              <Button type="submit" disabled={loading} className="w-full bg-blue-600 text-white hover:bg-blue-700">{loading ? 'Connexion...' : 'Se connecter'}</Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <button onClick={() => setPage('mini-login')} className="text-zinc-400 text-sm hover:text-blue-400">Connexion Étudiant</button>
              <br />
              <button onClick={() => setPage('landing')} className="text-zinc-500 hover:text-zinc-300 text-xs flex items-center gap-1 mx-auto"><ArrowLeft className="w-3 h-3" /> Retour</button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// ─── Student Dashboard ───
function StudentDashboard() {
  const { student, grades, payments, notifications, setPage, setStudent, setGrades, setPayments, setNotifications } = useAppStore()
  const [tab, setTab] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState({ firstName: '', lastName: '', phone: '', address: '', city: '', nationality: '', genre: '', dateOfBirth: '' })
  const [saveMsg, setSaveMsg] = useState('')

  if (!student) return null

  const startEdit = () => {
    setEditForm({ firstName: student.firstName, lastName: student.lastName, phone: student.phone || '', address: student.address || '', city: student.city || '', nationality: student.nationality || '', genre: student.genre || '', dateOfBirth: student.dateOfBirth || '' })
    setEditing(true)
    setSaveMsg('')
  }

  const saveProfile = async () => {
    try {
      const res = await fetch('/api/students/update', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: student.id, ...editForm }) })
      const data = await res.json()
      if (data.success) {
        setStudent({ ...student, ...editForm })
        setSaveMsg('Profil mis à jour avec succès')
        setEditing(false)
      } else { setSaveMsg(data.error || 'Erreur') }
    } catch { setSaveMsg('Erreur serveur') }
  }

  const paidCount = payments.filter(p => p.statut === 'paye').length
  const unpaidCount = payments.filter(p => p.statut === 'impaye').length

  const handleLogout = () => {
    setStudent(null); setGrades([]); setPayments([]); setNotifications([])
    setPage('landing')
  }

  const menuItems = [
    { id: 'dashboard', icon: BarChart3, label: 'Tableau de bord' },
    { id: 'notes', icon: BookOpen, label: 'Mes Notes' },
    { id: 'paiements', icon: CreditCard, label: 'Mes Paiements' },
    { id: 'profil', icon: User, label: 'Mon Profil' },
  ]

  return (
    <div className="min-h-screen bg-black flex">
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col transition-transform lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-4 border-b border-zinc-800">
          <button onClick={() => setPage('landing')} className="flex items-center gap-3 hover:opacity-80 transition">
            <img src={LOGO} alt="ESTAM" className="w-10 h-10 rounded-lg object-contain" />
            <div>
              <p className="text-blue-500 font-bold text-sm">ESTAM</p>
              <p className="text-zinc-500 text-xs">Espace Étudiant</p>
            </div>
          </button>
          <button className="ml-auto lg:hidden absolute right-4 top-4 text-zinc-400" onClick={() => setSidebarOpen(false)}><X className="w-5 h-5" /></button>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {menuItems.map(item => (
            <button key={item.id} onClick={() => { setTab(item.id); setSidebarOpen(false) }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${tab === item.id ? 'bg-blue-600/10 text-blue-400' : 'text-zinc-400 hover:text-white hover:bg-zinc-800'}`}>
              <item.icon className="w-5 h-5" />{item.label}
            </button>
          ))}
        </nav>
        <div className="p-3 border-t border-zinc-800">
          <button onClick={handleLogout} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-500/10 transition">
            <LogOut className="w-5 h-5" />Déconnexion
          </button>
        </div>
      </aside>

      <main className="flex-1 min-h-screen">
        <header className="sticky top-0 z-30 bg-black/80 backdrop-blur-md border-b border-zinc-800 px-4 sm:px-6 h-14 flex items-center gap-4">
          <button className="lg:hidden text-zinc-400" onClick={() => setSidebarOpen(true)}><Menu className="w-6 h-6" /></button>
          <h2 className="text-white font-semibold text-sm sm:text-base">{menuItems.find(m => m.id === tab)?.label}</h2>
          <div className="ml-auto flex items-center gap-3">
            <NotificationBell />
            <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs font-mono">{student.studentId}</Badge>
            <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 text-sm font-bold">
              {student.firstName[0]}{student.lastName[0]}
            </div>
          </div>
        </header>

        <div className="p-4 sm:p-6 max-w-6xl">
          {/* Dashboard Tab */}
          {tab === 'dashboard' && (
            <div className="space-y-6">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardContent className="pt-6">
                    <h3 className="text-white text-lg font-semibold">Bienvenue, {student.firstName} {student.lastName}</h3>
                    <p className="text-zinc-400 text-sm mt-1">{student.filiere} - {student.niveau} | {student.anneeScolaire}</p>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-6">
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-blue-500">{grades.length}</p><p className="text-zinc-400 text-xs">Notes</p></div>
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-green-400">{paidCount}</p><p className="text-zinc-400 text-xs">Payés</p></div>
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-red-400">{unpaidCount}</p><p className="text-zinc-400 text-xs">Impayés</p></div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          )}

          {/* Notes Tab */}
          {tab === 'notes' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              {grades.length === 0 ? (
                <Card className="bg-zinc-900 border-zinc-800"><CardContent className="py-12 text-center"><BookOpen className="w-12 h-12 text-zinc-700 mx-auto mb-3" /><p className="text-zinc-500">Aucune note publiée pour le moment</p></CardContent></Card>
              ) : (
                <Card className="bg-zinc-900 border-zinc-800 overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead><tr className="border-b border-zinc-800">
                        <th className="text-left text-zinc-400 font-medium px-4 py-3">Matière</th>
                        <th className="text-left text-zinc-400 font-medium px-4 py-3">Type</th>
                        <th className="text-left text-zinc-400 font-medium px-4 py-3">Note</th>
                        <th className="text-left text-zinc-400 font-medium px-4 py-3 hidden sm:table-cell">Coeff.</th>
                        <th className="text-left text-zinc-400 font-medium px-4 py-3">Semestre</th>
                      </tr></thead>
                      <tbody>
                        {grades.map(g => (
                          <tr key={g.id} className="border-b border-zinc-800/50 hover:bg-zinc-800/30 transition">
                            <td className="px-4 py-3 text-white">{g.matiere}</td>
                            <td className="px-4 py-3"><Badge variant="outline" className="border-zinc-700 text-zinc-300 text-xs">{g.type}</Badge></td>
                            <td className="px-4 py-3 font-bold text-blue-400">{g.note}</td>
                            <td className="px-4 py-3 text-zinc-400 hidden sm:table-cell">{g.coefficient || '-'}</td>
                            <td className="px-4 py-3 text-zinc-400">{g.semestre}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </Card>
              )}
            </motion.div>
          )}

          {/* Paiements Tab */}
          {tab === 'paiements' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              {payments.length === 0 ? (
                <Card className="bg-zinc-900 border-zinc-800"><CardContent className="py-12 text-center"><CreditCard className="w-12 h-12 text-zinc-700 mx-auto mb-3" /><p className="text-zinc-500">Aucun paiement enregistré</p></CardContent></Card>
              ) : (
                <div className="grid sm:grid-cols-2 gap-4">
                  {payments.map(p => (
                    <Card key={p.id} className="bg-zinc-900 border-zinc-800">
                      <CardContent className="pt-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white font-medium">{p.mois}</span>
                          <Badge className={p.statut === 'paye' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}>
                            {p.statut === 'paye' ? <><CheckCircle2 className="w-3 h-3 mr-1" />Payé</> : <><XCircle className="w-3 h-3 mr-1" />Impayé</>}
                          </Badge>
                        </div>
                        <p className="text-blue-400 font-bold text-lg">{p.montant.toLocaleString()} FCFA</p>
                        {p.datePaiement && <p className="text-zinc-500 text-xs mt-1">Date : {p.datePaiement}</p>}
                        <p className="text-zinc-600 text-xs mt-1">Année : {p.anneeScolaire}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {/* Profil Tab */}
          {tab === 'profil' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 text-2xl font-bold">
                        {student.firstName[0]}{student.lastName[0]}
                      </div>
                      <div>
                        <CardTitle className="text-white">{student.firstName} {student.lastName}</CardTitle>
                        <CardDescription className="text-blue-400 font-mono">{student.studentId}</CardDescription>
                      </div>
                    </div>
                    {!editing ? (
                      <Button variant="outline" size="sm" className="border-blue-500/30 text-blue-400 text-xs" onClick={startEdit}><Edit3 className="w-3 h-3 mr-1" />Modifier</Button>
                    ) : (
                      <div className="flex gap-2">
                        <Button size="sm" className="bg-blue-600 text-white hover:bg-blue-700 text-xs" onClick={saveProfile}><Save className="w-3 h-3 mr-1" />Enregistrer</Button>
                        <Button size="sm" variant="outline" className="border-zinc-700 text-zinc-400 text-xs" onClick={() => { setEditing(false); setSaveMsg('') }}>Annuler</Button>
                      </div>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {saveMsg && <p className={`text-sm flex items-center gap-1 ${saveMsg.includes('succès') ? 'text-green-400' : 'text-red-400'}`}>{saveMsg.includes('succès') ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}{saveMsg}</p>}
                  {!editing ? (
                    <div className="grid sm:grid-cols-2 gap-4">
                      {[
                        { label: 'Email', value: student.email, icon: Mail },
                        { label: 'Téléphone', value: student.phone || '-', icon: Phone },
                        { label: 'Ville', value: student.city || '-', icon: MapPin },
                        { label: 'Filière', value: student.filiere, icon: BookOpen },
                        { label: 'Niveau', value: student.niveau, icon: GraduationCap },
                        { label: 'Année', value: student.anneeScolaire, icon: Calendar },
                      ].map(item => (
                        <div key={item.label} className="bg-zinc-800 rounded-lg p-3 flex items-center gap-3">
                          <item.icon className="w-4 h-4 text-blue-400 flex-shrink-0" />
                          <div><p className="text-zinc-500 text-xs">{item.label}</p><p className="text-white text-sm">{item.value}</p></div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="grid sm:grid-cols-2 gap-4">
                      <div><Label className="text-zinc-300">Prénom</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.firstName} onChange={e => setEditForm({ ...editForm, firstName: e.target.value })} /></div>
                      <div><Label className="text-zinc-300">Nom</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.lastName} onChange={e => setEditForm({ ...editForm, lastName: e.target.value })} /></div>
                      <div><Label className="text-zinc-300">Téléphone</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.phone} onChange={e => setEditForm({ ...editForm, phone: e.target.value })} /></div>
                      <div><Label className="text-zinc-300">Date de naissance</Label><Input type="date" className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.dateOfBirth} onChange={e => setEditForm({ ...editForm, dateOfBirth: e.target.value })} /></div>
                      <div><Label className="text-zinc-300">Genre</Label>
                        <Select value={editForm.genre} onValueChange={v => setEditForm({ ...editForm, genre: v })}>
                          <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="M">Masculin</SelectItem><SelectItem value="F">Féminin</SelectItem></SelectContent>
                        </Select>
                      </div>
                      <div><Label className="text-zinc-300">Ville</Label>
                        <Select value={editForm.city} onValueChange={v => setEditForm({ ...editForm, city: v })}>
                          <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                          <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="Brazzaville">Brazzaville</SelectItem><SelectItem value="Pointe-Noire">Pointe-Noire</SelectItem></SelectContent>
                        </Select>
                      </div>
                      <div className="sm:col-span-2"><Label className="text-zinc-300">Adresse</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.address} onChange={e => setEditForm({ ...editForm, address: e.target.value })} /></div>
                      <div><Label className="text-zinc-300">Nationalité</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={editForm.nationality} onChange={e => setEditForm({ ...editForm, nationality: e.target.value })} /></div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}

// ─── Admin Dashboard ───
function AdminDashboard() {
  const { adminEmail, setPage, setAdmin } = useAppStore()
  const [tab, setTab] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedFiliere, setSelectedFiliere] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [students, setStudents] = useState<Record<string, unknown>[]>([])
  const [selectedStudent, setSelectedStudent] = useState<Record<string, unknown> | null>(null)
  const [loading, setLoading] = useState(false)
  const [gradeForm, setGradeForm] = useState({ matiere: '', type: 'Semestre', note: '', coefficient: '', semestre: 'Semestre 1', anneeScolaire: new Date().getFullYear().toString(), comment: '' })
  const [payForm, setPayForm] = useState({ mois: MOIS[0], montant: '35000', datePaiement: '', statut: 'impaye', anneeScolaire: new Date().getFullYear().toString() })
  const [pwForm, setPwForm] = useState({ current: '', newPw: '', confirm: '' })
  const [pwMsg, setPwMsg] = useState('')
  const [filiereCounts, setFiliereCounts] = useState<Record<string, number>>({})
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [broadcastForm, setBroadcastForm] = useState({ titre: '', message: '', type: 'info' })
  const [broadcastMsg, setBroadcastMsg] = useState('')
  const [allStudents, setAllStudents] = useState<Record<string, unknown>[]>([])
  const [allSearch, setAllSearch] = useState('')
  const [qrDataUrl, setQrDataUrl] = useState('')

  const fetchCounts = async () => {
    try {
      const res = await fetch('/api/admin/counts')
      const data = await res.json()
      setFiliereCounts(data.counts || {})
    } catch {}
  }

  useEffect(() => { fetchCounts() }, [tab, selectedStudent])

  const fetchStudents = async (category?: string, filiere?: string, search?: string) => {
    setLoading(true)
    const params = new URLSearchParams()
    if (category) params.set('category', category)
    if (filiere) params.set('filiere', filiere)
    if (search) params.set('search', search)
    try {
      const res = await fetch(`/api/admin/students?${params.toString()}`)
      const data = await res.json()
      setStudents(data.students || [])
    } catch { setStudents([]) }
    finally { setLoading(false) }
  }

  useEffect(() => {
    if (selectedCategory && selectedFiliere) fetchStudents(selectedCategory, selectedFiliere, searchQuery)
  }, [selectedCategory, selectedFiliere, searchQuery])

  const fetchAllStudents = async (search?: string) => {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.set('search', search)
    try {
      const res = await fetch(`/api/admin/students?${params.toString()}`)
      const data = await res.json()
      setAllStudents(data.students || [])
    } catch { setAllStudents([]) }
    finally { setLoading(false) }
  }

  useEffect(() => {
    if (tab === 'classe') fetchAllStudents(allSearch)
  }, [tab, allSearch])

  const handleLogout = () => { setAdmin(false); setPage('landing') }

  const deleteStudents = async (ids: string[]) => {
    if (!confirm(`Supprimer ${ids.length} étudiant(s) ?`)) return
    try {
      await fetch(`/api/admin/students?ids=${ids.join(',')}`, { method: 'DELETE' })
      setSelectedIds([])
      fetchStudents(selectedCategory || undefined, selectedFiliere || undefined, searchQuery)
      fetchAllStudents(allSearch)
      fetchCounts()
    } catch {}
  }

  const sendBroadcast = async (e: FormEvent) => {
    e.preventDefault()
    if (!broadcastForm.titre || !broadcastForm.message) return
    try {
      const res = await fetch('/api/notifications/broadcast', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(broadcastForm) })
      const data = await res.json()
      setBroadcastMsg(data.success ? `Notification envoyée à ${data.sent} étudiant(s)` : 'Erreur')
      setBroadcastForm({ titre: '', message: '', type: 'info' })
    } catch { setBroadcastMsg('Erreur serveur') }
  }

  const toggleSelect = (id: string) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id])
  }

  const openStudent = async (studentId: string) => {
    try {
      const res = await fetch(`/api/students/by-studentid?studentId=${studentId}`)
      const data = await res.json()
      if (data.student) {
        const s = data.student as Record<string, unknown>
        setSelectedStudent(s)
        setTab('student-detail')
        // Generate QR code
        const qrInfo = JSON.stringify({
          id: s.studentId, nom: `${s.firstName} ${s.lastName}`,
          email: s.email, filiere: s.filiere, niveau: s.niveau,
          ville: s.city
        })
        QRCode.toDataURL(qrInfo, { width: 200, margin: 2, color: { dark: '#2563eb', light: '#18181b' } }).then(setQrDataUrl).catch(() => {})
      }
    } catch { }
  }

  const addGrade = async (e: FormEvent) => {
    e.preventDefault()
    if (!selectedStudent) return
    try {
      await fetch('/api/grades', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...gradeForm, studentId: (selectedStudent as Record<string, string>).id, coefficient: gradeForm.coefficient ? parseFloat(gradeForm.coefficient) : null }) })
      const res = await fetch(`/api/students/${(selectedStudent as Record<string, string>).id}`)
      const data = await res.json()
      setSelectedStudent(data.student)
      setGradeForm({ matiere: '', type: 'Semestre', note: '', coefficient: '', semestre: 'Semestre 1', anneeScolaire: new Date().getFullYear().toString(), comment: '' })
    } catch { }
  }

  const addPayment = async (e: FormEvent) => {
    e.preventDefault()
    if (!selectedStudent) return
    try {
      await fetch('/api/payments', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...payForm, studentId: (selectedStudent as Record<string, string>).id }) })
      const res = await fetch(`/api/students/${(selectedStudent as Record<string, string>).id}`)
      const data = await res.json()
      setSelectedStudent(data.student)
    } catch { }
  }

  const changePassword = async (e: FormEvent) => {
    e.preventDefault()
    setPwMsg('')
    if (pwForm.newPw !== pwForm.confirm) { setPwMsg('Les mots de passe ne correspondent pas'); return }
    try {
      const res = await fetch('/api/admin/password', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ currentPassword: pwForm.current, newPassword: pwForm.newPw }) })
      const data = await res.json()
      setPwMsg(data.success ? 'Mot de passe modifié avec succès !' : data.error)
      if (data.success) setPwForm({ current: '', newPw: '', confirm: '' })
    } catch { setPwMsg('Erreur serveur') }
  }

  const adminMenu = [
    { id: 'dashboard', icon: BarChart3, label: 'Tableau de bord' },
    { id: 'classe', icon: UsersRound, label: 'Classe Étudiant' },
    { id: 'gestion', icon: Users, label: 'Gestion' },
    { id: 'technologie', icon: Settings, label: 'Technologie' },
    { id: 'diffusion', icon: Megaphone, label: 'Diffusion' },
    { id: 'parametres', icon: Settings, label: 'Paramètres' },
  ]

  return (
    <div className="min-h-screen bg-black flex">
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col transition-transform lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-4 border-b border-zinc-800">
          <button onClick={() => setPage('landing')} className="flex items-center gap-3 hover:opacity-80 transition">
            <img src={LOGO} alt="ESTAM" className="w-10 h-10 rounded-lg object-contain" />
            <div>
              <p className="text-blue-500 font-bold text-sm">ESTAM Admin</p>
              <p className="text-zinc-500 text-xs">{adminEmail}</p>
            </div>
          </button>
          <button className="ml-auto lg:hidden absolute right-4 top-4 text-zinc-400" onClick={() => setSidebarOpen(false)}><X className="w-5 h-5" /></button>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {adminMenu.map(item => (
            <button key={item.id} onClick={() => { setTab(item.id); setSidebarOpen(false); setSelectedStudent(null); setSelectedFiliere(null) }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${tab === item.id ? 'bg-blue-600/10 text-blue-400' : 'text-zinc-400 hover:text-white hover:bg-zinc-800'}`}>
              <item.icon className="w-5 h-5" />{item.label}
            </button>
          ))}
        </nav>
        <div className="p-3 border-t border-zinc-800">
          <button onClick={handleLogout} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-red-400 hover:bg-red-500/10 transition">
            <LogOut className="w-5 h-5" />Déconnexion
          </button>
        </div>
      </aside>

      <main className="flex-1 min-h-screen">
        <header className="sticky top-0 z-30 bg-black/80 backdrop-blur-md border-b border-zinc-800 px-4 sm:px-6 h-14 flex items-center gap-4">
          <button className="lg:hidden text-zinc-400" onClick={() => setSidebarOpen(true)}><Menu className="w-6 h-6" /></button>
          <h2 className="text-white font-semibold text-sm sm:text-base">
            {tab === 'student-detail' && selectedStudent ? (
              <button onClick={() => { setTab(selectedCategory === 'Gestion' ? 'gestion' : selectedCategory === 'Technologie' ? 'technologie' : 'classe'); setSelectedStudent(null) }} className="flex items-center gap-2 text-zinc-400 hover:text-white">
                <ArrowLeft className="w-4 h-4" />{(selectedStudent as Record<string, string>).studentId}
              </button>
            ) : adminMenu.find(m => m.id === tab)?.label}
          </h2>
        </header>

        <div className="p-4 sm:p-6 max-w-7xl">
          {/* Admin Dashboard */}
          {tab === 'dashboard' && (
            <div className="space-y-6">
              <Card className="bg-zinc-900 border-zinc-800">
                <CardContent className="pt-6">
                  <h3 className="text-white text-lg font-semibold mb-4">Vue d&apos;ensemble</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-blue-500">{Object.values(filiereCounts).reduce((a, b) => a + b, 0) || 0}</p><p className="text-zinc-400 text-xs">Total étudiants</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Users className="w-6 h-6 text-blue-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Gestion</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Settings className="w-6 h-6 text-blue-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Technologie</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Bell className="w-6 h-6 text-blue-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Activité</p></div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Classe Étudiant - ALL students */}
          {tab === 'classe' && !selectedStudent && (
            <div className="space-y-4">
              <h3 className="text-white font-semibold text-lg">Tous les étudiants inscrits</h3>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                <Input className="pl-10 bg-zinc-900 border-zinc-800 text-white" placeholder="Rechercher par nom, prénom ou identifiant (EST...)" value={allSearch} onChange={e => setAllSearch(e.target.value)} />
              </div>
              {loading ? <div className="text-center py-12"><Loader2 className="w-8 h-8 text-blue-500 mx-auto animate-spin" /></div> : allStudents.length === 0 ? (
                <p className="text-zinc-500 text-sm text-center py-12">Aucun étudiant trouvé</p>
              ) : (
                <div className="space-y-2">
                  <p className="text-zinc-500 text-xs">{allStudents.length} étudiant(s) trouvé(s)</p>
                  {allStudents.map(s => {
                    const st = s as Record<string, string>
                    return (
                      <Card key={st.id} className="bg-zinc-900 border-zinc-800 cursor-pointer hover:border-blue-500/50 transition" onClick={() => openStudent(st.studentId)}>
                        <CardContent className="py-3 px-4 flex items-center gap-4">
                          <div className="w-10 h-10 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 font-bold text-sm">{(st.firstName || '?')[0]}{(st.lastName || '?')[0]}</div>
                          <div className="flex-1 min-w-0">
                            <p className="text-white text-sm font-medium">{st.firstName} {st.lastName}</p>
                            <p className="text-zinc-500 text-xs font-mono">{st.studentId} · {st.filiere || '-'} · {st.niveau || '-'}</p>
                          </div>
                          <Badge variant="outline" className="border-zinc-700 text-zinc-400 text-xs hidden sm:block">{st.filiereCategory || '-'}</Badge>
                          <Badge variant="outline" className={st.verified === 'true' ? 'border-green-500/30 text-green-400 text-xs' : 'border-zinc-700 text-zinc-500 text-xs'}>{st.verified === 'true' ? 'Vérifié' : 'Non vérifié'}</Badge>
                          <button onClick={(e) => { e.stopPropagation(); deleteStudents([st.id]) }} className="text-zinc-600 hover:text-red-400 transition p-1"><Trash2 className="w-4 h-4" /></button>
                          <ChevronRight className="w-5 h-5 text-zinc-600" />
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>
              )}
            </div>
          )}

          {/* Gestion / Technologie Tab */}
          {(tab === 'gestion' || tab === 'technologie') && !selectedStudent && (
            <div className="space-y-6">
              {!selectedFiliere ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <h3 className="text-white font-semibold mb-4">Sélectionnez une filière en {tab === 'gestion' ? 'Gestion' : 'Technologie'}</h3>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {FILIERES[tab === 'gestion' ? 'Gestion' : 'Technologie'].map((f, i) => {
                      const cat = tab === 'gestion' ? 'Gestion' : 'Technologie'
                      const countKey = `${cat}|||${f}`
                      const count = filiereCounts[countKey] || 0
                      return (
                      <Card key={f} className="bg-zinc-900 border-zinc-800 cursor-pointer hover:border-blue-500/50 transition" onClick={() => { setSelectedCategory(cat); setSelectedFiliere(f); setSearchQuery(''); setSelectedIds([]) }}>
                        <CardContent className="pt-4 flex items-center gap-3">
                          <div className="w-10 h-10 rounded-lg bg-blue-600/10 flex items-center justify-center text-blue-400 font-bold">{i + 1}</div>
                          <div className="flex-1 min-w-0">
                            <p className="text-white text-sm font-medium truncate">{f}</p>
                            <p className="text-zinc-500 text-xs">{count} étudiant{count > 1 ? 's' : ''} inscrit{count > 1 ? 's' : ''}</p>
                          </div>
                          <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 font-bold text-sm">{count}</div>
                          <ChevronRight className="w-5 h-5 text-zinc-600" />
                        </CardContent>
                      </Card>
                      )
                    })}
                  </div>
                </motion.div>
              ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <button onClick={() => { setSelectedFiliere(null); setStudents([]) }} className="flex items-center gap-2 text-zinc-400 hover:text-white text-sm"><ArrowLeft className="w-4 h-4" />Retour aux filières</button>
                  <h3 className="text-white font-semibold">{selectedFiliere}</h3>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                    <Input className="pl-10 bg-zinc-900 border-zinc-800 text-white" placeholder="Rechercher par nom ou identifiant (EST...)" value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
                  </div>
                  {loading ? <p className="text-zinc-500 text-sm">Chargement...</p> : students.length === 0 ? (
                    <p className="text-zinc-500 text-sm text-center py-12">Aucun étudiant trouvé dans cette filière</p>
                  ) : (
                    <>
                    {selectedIds.length > 0 && (
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-zinc-400 text-sm">{selectedIds.length} sélectionné(s)</span>
                        <Button variant="destructive" size="sm" className="bg-red-500/20 text-red-400 hover:bg-red-500/30 text-xs h-8" onClick={(e) => { e.stopPropagation(); deleteStudents(selectedIds) }}><Trash2 className="w-3 h-3 mr-1" />Supprimer</Button>
                        <Button variant="outline" size="sm" className="border-zinc-700 text-zinc-400 text-xs h-8" onClick={() => { if (confirm('Supprimer TOUS les étudiants de cette filière ?')) deleteStudents(students.map(s => (s as Record<string, string>).id)) }}><Trash2 className="w-3 h-3 mr-1" />Tous supprimer</Button>
                      </div>
                    )}
                    <div className="space-y-2">
                      {students.map(s => {
                        const st = s as Record<string, string>
                        const isSelected = selectedIds.includes(st.id)
                        return (
                          <Card key={st.id} className={`bg-zinc-900 border-zinc-800 cursor-pointer hover:border-blue-500/50 transition ${isSelected ? 'border-blue-500/50 bg-blue-600/5' : ''}`} onClick={() => openStudent(st.studentId)}>
                            <CardContent className="py-3 px-4 flex items-center gap-4">
                              <button onClick={(e) => { e.stopPropagation(); toggleSelect(st.id) }} className={`w-5 h-5 rounded border flex items-center justify-center flex-shrink-0 transition ${isSelected ? 'bg-blue-600 border-blue-600' : 'border-zinc-600 hover:border-zinc-400'}`}>
                                {isSelected && <Check className="w-3 h-3 text-white" />}
                              </button>
                              <div className="w-10 h-10 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 font-bold text-sm">{(st.firstName || '?')[0]}{(st.lastName || '?')[0]}</div>
                              <div className="flex-1 min-w-0">
                                <p className="text-white text-sm font-medium">{st.firstName} {st.lastName}</p>
                                <p className="text-zinc-500 text-xs font-mono">{st.studentId} · {st.niveau}</p>
                              </div>
                              <Badge variant="outline" className={st.verified === 'true' ? 'border-green-500/30 text-green-400' : 'border-zinc-700 text-zinc-500'}>{st.verified === 'true' ? 'Vérifié' : 'Non vérifié'}</Badge>
                              <button onClick={(e) => { e.stopPropagation(); deleteStudents([st.id]) }} className="text-zinc-600 hover:text-red-400 transition p-1"><Trash2 className="w-4 h-4" /></button>
                              <ChevronRight className="w-5 h-5 text-zinc-600" />
                            </CardContent>
                          </Card>
                        )
                      })}
                    </div>
                    </>
                  )}
                </motion.div>
              )}
            </div>
          )}

          {/* Student Detail */}
          {tab === 'student-detail' && selectedStudent && (() => {
            const s = selectedStudent as Record<string, unknown>
            const sGrades = (s.grades as Record<string, string>[]) || []
            const sPayments = (s.payments as Record<string, string>[]) || []
            return (
              <div className="space-y-6">
                {/* Student Info Header */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader>
                    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                      <div className="w-16 h-16 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 text-2xl font-bold">{String(s.firstName || '?')[0]}{String(s.lastName || '?')[0]}</div>
                      <div className="flex-1">
                        <CardTitle className="text-white text-xl">{String(s.firstName)} {String(s.lastName)}</CardTitle>
                        <CardDescription className="text-blue-400 font-mono">{String(s.studentId)} · {String(s.filiere)} · {String(s.niveau)}</CardDescription>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="border-blue-500/30 text-blue-400 text-xs" onClick={() => generateStudentPDF(s)}><Download className="w-3 h-3 mr-1" />PDF</Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {[
                        { l: 'Email', v: String(s.email || '-') },
                        { l: 'Téléphone', v: String(s.phone || '-') },
                        { l: 'Ville', v: String(s.city || '-') },
                        { l: 'Statut', v: String(s.status || '-') },
                      ].map(i => (
                        <div key={i.l} className="bg-zinc-800 rounded p-2"><p className="text-zinc-500 text-xs">{i.l}</p><p className="text-white text-sm">{i.v}</p></div>
                      ))}
                    </div>
                    {/* QR Code */}
                    {qrDataUrl && (
                      <div className="mt-4 flex flex-col items-center p-4 bg-zinc-800 rounded-xl">
                        <p className="text-zinc-400 text-xs mb-2">Code QR - Informations étudiant</p>
                        <img src={qrDataUrl} alt="QR Code" className="w-48 h-48 rounded-lg" />
                        <p className="text-zinc-600 text-[10px] mt-2">Scannez pour retrouver les informations de l&apos;étudiant</p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Existing Grades */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader><CardTitle className="text-white text-base">Notes publiées</CardTitle></CardHeader>
                  <CardContent>
                    {sGrades.length === 0 ? <p className="text-zinc-500 text-sm">Aucune note</p> : (
                      <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                          <thead><tr className="border-b border-zinc-800"><th className="text-left text-zinc-400 px-3 py-2">Matière</th><th className="text-left text-zinc-400 px-3 py-2">Type</th><th className="text-left text-zinc-400 px-3 py-2">Note</th><th className="text-left text-zinc-400 px-3 py-2">Sem.</th></tr></thead>
                          <tbody>{sGrades.map(g => (
                            <tr key={g.id} className="border-b border-zinc-800/50"><td className="px-3 py-2 text-white">{g.matiere}</td><td className="px-3 py-2 text-zinc-400">{g.type}</td><td className="px-3 py-2 text-blue-400 font-bold">{g.note}</td><td className="px-3 py-2 text-zinc-400">{g.semestre}</td></tr>
                          ))}</tbody>
                        </table>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Add Grade Form */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader><CardTitle className="text-white text-base">Publier une note</CardTitle></CardHeader>
                  <CardContent>
                    <form onSubmit={addGrade} className="grid sm:grid-cols-3 gap-3">
                      <Input className="bg-zinc-800 border-zinc-700 text-white" placeholder="Matière" value={gradeForm.matiere} onChange={e => setGradeForm({ ...gradeForm, matiere: e.target.value })} required />
                      <Select value={gradeForm.type} onValueChange={v => setGradeForm({ ...gradeForm, type: v })}>
                        <SelectTrigger className="bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="Session">Session</SelectItem><SelectItem value="Devoir">Devoir</SelectItem><SelectItem value="Semestre">Semestre</SelectItem><SelectItem value="Rattrapage">Rattrapage</SelectItem></SelectContent>
                      </Select>
                      <Input className="bg-zinc-800 border-zinc-700 text-white" placeholder="Note (ex: 14/20)" value={gradeForm.note} onChange={e => setGradeForm({ ...gradeForm, note: e.target.value })} required />
                      <Input className="bg-zinc-800 border-zinc-700 text-white" placeholder="Coefficient" value={gradeForm.coefficient} onChange={e => setGradeForm({ ...gradeForm, coefficient: e.target.value })} />
                      <Select value={gradeForm.semestre} onValueChange={v => setGradeForm({ ...gradeForm, semestre: v })}>
                        <SelectTrigger className="bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="Semestre 1">Semestre 1</SelectItem><SelectItem value="Semestre 2">Semestre 2</SelectItem></SelectContent>
                      </Select>
                      <Button type="submit" className="bg-blue-600 text-white hover:bg-blue-700">Publier</Button>
                    </form>
                  </CardContent>
                </Card>

                {/* Existing Payments */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader><CardTitle className="text-white text-base">Paiements</CardTitle></CardHeader>
                  <CardContent>
                    {sPayments.length === 0 ? <p className="text-zinc-500 text-sm">Aucun paiement</p> : (
                      <div className="grid sm:grid-cols-2 gap-3">
                        {sPayments.map(p => (
                          <div key={p.id} className="bg-zinc-800 rounded-lg p-3 flex items-center justify-between">
                            <div>
                              <p className="text-white text-sm">{p.mois}</p>
                              <p className="text-zinc-500 text-xs">{p.datePaiement || '-'} · {p.anneeScolaire}</p>
                            </div>
                            <div className="text-right">
                              <p className="text-blue-400 font-bold text-sm">{Number(p.montant).toLocaleString()} F</p>
                              <Badge className={p.statut === 'paye' ? 'bg-green-500/20 text-green-400 text-xs' : 'bg-red-500/20 text-red-400 text-xs'}>{p.statut === 'paye' ? 'Payé' : 'Impayé'}</Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Add Payment Form */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader><CardTitle className="text-white text-base">Enregistrer un paiement</CardTitle></CardHeader>
                  <CardContent>
                    <form onSubmit={addPayment} className="grid sm:grid-cols-3 gap-3">
                      <Select value={payForm.mois} onValueChange={v => setPayForm({ ...payForm, mois: v })}>
                        <SelectTrigger className="bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-zinc-800 border-zinc-700">{MOIS.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
                      </Select>
                      <Input className="bg-zinc-800 border-zinc-700 text-white" type="number" placeholder="Montant (FCFA)" value={payForm.montant} onChange={e => setPayForm({ ...payForm, montant: e.target.value })} required />
                      <Input className="bg-zinc-800 border-zinc-700 text-white" type="date" value={payForm.datePaiement} onChange={e => setPayForm({ ...payForm, datePaiement: e.target.value })} />
                      <Select value={payForm.statut} onValueChange={v => setPayForm({ ...payForm, statut: v })}>
                        <SelectTrigger className="bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="paye">Payé</SelectItem><SelectItem value="impaye">Impayé</SelectItem></SelectContent>
                      </Select>
                      <Button type="submit" className="bg-blue-600 text-white hover:bg-blue-700 sm:col-span-2">Enregistrer</Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            )
          })()}

          {/* Diffusion */}
          {tab === 'diffusion' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <Card className="bg-zinc-900 border-zinc-800 max-w-2xl">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2"><Megaphone className="w-5 h-5 text-blue-500" /> Diffuser une notification</CardTitle>
                  <CardDescription className="text-zinc-400">Envoyer instantanément à tous les étudiants vérifiés</CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={sendBroadcast} className="space-y-4">
                    <div><Label className="text-zinc-300">Titre</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={broadcastForm.titre} onChange={e => setBroadcastForm({ ...broadcastForm, titre: e.target.value })} required /></div>
                    <div><Label className="text-zinc-300">Message</Label><textarea className="mt-1 w-full min-h-[100px] rounded-lg bg-zinc-800 border border-zinc-700 text-white p-3 text-sm resize-none" value={broadcastForm.message} onChange={e => setBroadcastForm({ ...broadcastForm, message: e.target.value })} required /></div>
                    <div><Label className="text-zinc-300">Type</Label>
                      <Select value={broadcastForm.type} onValueChange={v => setBroadcastForm({ ...broadcastForm, type: v })}>
                        <SelectTrigger className="mt-1 bg-zinc-800 border-zinc-700 text-white"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-zinc-800 border-zinc-700"><SelectItem value="info">Information</SelectItem><SelectItem value="alerte">Alerte</SelectItem><SelectItem value="note">Note</SelectItem><SelectItem value="paiement">Paiement</SelectItem></SelectContent>
                      </Select>
                    </div>
                    {broadcastMsg && <p className={`text-sm flex items-center gap-1 ${broadcastMsg.includes('envoyée') ? 'text-green-400' : 'text-red-400'}`}>{broadcastMsg.includes('envoyée') ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}{broadcastMsg}</p>}
                    <Button type="submit" className="bg-blue-600 text-white hover:bg-blue-700"><Send className="w-4 h-4 mr-2" />Publier à tous les étudiants</Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Paramètres */}
          {tab === 'parametres' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <Card className="bg-zinc-900 border-zinc-800 max-w-md">
                <CardHeader><CardTitle className="text-white">Modifier le mot de passe</CardTitle></CardHeader>
                <CardContent>
                  <form onSubmit={changePassword} className="space-y-4">
                    <div><Label className="text-zinc-300">Email actuel</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={adminEmail} disabled /></div>
                    <div><Label className="text-zinc-300">Mot de passe actuel</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" type="password" value={pwForm.current} onChange={e => setPwForm({ ...pwForm, current: e.target.value })} required /></div>
                    <div><Label className="text-zinc-300">Nouveau mot de passe</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" type="password" value={pwForm.newPw} onChange={e => setPwForm({ ...pwForm, newPw: e.target.value })} required /></div>
                    <div><Label className="text-zinc-300">Confirmer le nouveau mot de passe</Label><Input className="mt-1 bg-zinc-800 border-zinc-700 text-white" type="password" value={pwForm.confirm} onChange={e => setPwForm({ ...pwForm, confirm: e.target.value })} required /></div>
                    {pwMsg && <p className={`text-sm flex items-center gap-1 ${pwMsg.includes('succès') ? 'text-green-400' : 'text-red-400'}`}>{pwMsg.includes('succès') ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}{pwMsg}</p>}
                    <Button type="submit" className="w-full bg-blue-600 text-white hover:bg-blue-700">Modifier le mot de passe</Button>
                  </form>
                  <div className="mt-6 p-4 bg-zinc-800 rounded-lg">
                    <p className="text-zinc-500 text-xs">Identifiants par défaut</p>
                    <p className="text-zinc-300 text-sm">Email : <span className="text-blue-400 font-mono">admin@estam.cg</span></p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}

// ─── Main Home Component ───
export default function Home() {
  const currentPage = useAppStore(s => s.currentPage)

  useEffect(() => {
    fetch('/api/auth/register').catch(() => {})
  }, [])

  switch (currentPage) {
    case 'landing': return <LandingPage />
    case 'register': return <RegisterPage />
    case 'verify': return <VerifyPage />
    case 'verification-steps': return <VerificationStepsPage />
    case 'login': return <LoginPage />
    case 'admin-login': return <AdminLoginPage />
    case 'mini-register': return <MiniLoading targetPage='register' />
    case 'mini-login': return <MiniLoading targetPage='login' />
    case 'mini-admin-login': return <MiniLoading targetPage='admin-login' />
    case 'loading': return <LoadingPage targetPage="student-dashboard" />
    case 'admin-loading': return <LoadingPage targetPage="admin-dashboard" />
    case 'student-dashboard': return <StudentDashboard />
    case 'admin-dashboard': return <AdminDashboard />
    default: return <LandingPage />
  }
}
"""

with open('/home/z/my-project/src/app/page.tsx', 'w') as f:
    f.write(content)

print("page.tsx written successfully")