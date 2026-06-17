'use client'

import { useState, useEffect, useRef, type FormEvent } from 'react'
import { motion, useInView } from 'framer-motion'
import { useAppStore, type Page, type Student, type Grade, type Payment, type Notification } from '@/store/appStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Progress } from '@/components/ui/progress'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  GraduationCap, BookOpen, Users, Bell, LogOut, Settings, Search,
  User, Mail, Lock, Phone, MapPin, Calendar, ChevronRight, Award,
  CreditCard, CheckCircle2, XCircle, AlertCircle, Eye, EyeOff,
  Menu, X, ArrowLeft, Building2, BarChart3, FileText, Shield
} from 'lucide-react'

// ─── Data Constants ───
const FILIERES: Record<string, string[]> = {
  Gestion: [
    'Comptabilité et Gestion',
    'Marketing et Action Commerciale',
    'Gestion des Ressources Humaines',
    'Gestion Commerciale',
    'Transport et Logistique',
  ],
  Technologie: [
    'Génie Civil',
    'Génie Électrique',
    'Informatique de Gestion',
    'Réseaux Informatiques et Télécommunications',
  ],
}

const MOIS = ['Octobre', 'Novembre', 'Décembre', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Septembre']

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

// ─── Loading Page ───
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
        <GraduationCap className="w-16 h-16 text-amber-500" />
      </motion.div>
      <p className="mt-6 text-amber-500 text-lg font-semibold tracking-wider">ESTAM</p>
      <p className="text-zinc-400 text-sm mt-2">Chargement de votre espace...</p>
      <div className="w-64 mt-6">
        <Progress value={progress} className="h-2 bg-zinc-800 [&>div]:bg-amber-500" />
      </div>
    </div>
  )
}

// ─── Landing Page ───
function LandingPage() {
  const setPage = useAppStore(s => s.setPage)
  return (
    <div className="min-h-screen bg-black">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-md border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <img src="/estam/IMG_1627.webp" alt="ESTAM" className="h-10 w-10 rounded-full object-cover" />
            <span className="text-amber-500 font-bold text-xl tracking-wider">ESTAM</span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <button onClick={() => document.getElementById('apropos')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-amber-500 transition text-sm">À propos</button>
            <button onClick={() => document.getElementById('filieres')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-amber-500 transition text-sm">Filières</button>
            <button onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })} className="text-zinc-300 hover:text-amber-500 transition text-sm">Contact</button>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" className="border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-black text-sm" onClick={() => setPage('login')}>Connexion</Button>
            <Button className="bg-amber-500 text-black hover:bg-amber-600 text-sm" onClick={() => setPage('register')}>S&apos;inscrire</Button>
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
            <img src="/estam/IMG_1627.webp" alt="ESTAM Logo" className="w-24 h-24 mx-auto rounded-full border-4 border-amber-500/50 mb-6 object-cover" />
          </Reveal>
          <Reveal delay={0.1}>
            <h1 className="text-4xl sm:text-6xl font-bold text-white mb-4">
              <span className="text-amber-500">ESTAM</span>
            </h1>
          </Reveal>
          <Reveal delay={0.2}>
            <p className="text-lg sm:text-xl text-zinc-300 mb-2">École Supérieure des Technologies Avancées et de Management</p>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="text-amber-500 font-semibold italic text-lg mb-8">&laquo; Une formation, un métier, une réussite &raquo;</p>
          </Reveal>
          <Reveal delay={0.4}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-amber-500 text-black hover:bg-amber-600 text-base px-8 py-6" onClick={() => setPage('register')}>
                <GraduationCap className="w-5 h-5 mr-2" /> S&apos;inscrire maintenant
              </Button>
              <Button size="lg" variant="outline" className="border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-black text-base px-8 py-6" onClick={() => setPage('login')}>
                <LogIn className="w-5 h-5 mr-2" /> Se connecter
              </Button>
            </div>
          </Reveal>
        </div>
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ChevronRight className="w-6 h-6 text-amber-500 rotate-90" />
        </div>
      </section>

      {/* About Section */}
      <section id="apropos" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <Reveal>
            <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">À propos de l&apos;ESTAM</h2>
            <div className="w-20 h-1 bg-amber-500 mx-auto mb-12" />
          </Reveal>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <Reveal delay={0.1}>
              <div className="space-y-6">
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;<strong className="text-amber-500">École Supérieure des Technologies Avancées et de Management (ESTAM)</strong> est un établissement d&apos;enseignement supérieur privé situé en <strong className="text-white">République du Congo</strong>, avec des campus à <strong className="text-white">Brazzaville</strong> et <strong className="text-white">Pointe-Noire</strong>. Créée par arrêté <strong className="text-amber-500">N° 0076/MES-CAB-DGESUP</strong>, l&apos;ESTAM travaille en étroite collaboration avec l&apos;Université CEREC-ISCOM.
                </p>
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;ESTAM a pour mission d&apos;offrir des programmes d&apos;études innovants, une formation professionnelle et personnelle de qualité, axée sur l&apos;excellence, l&apos;innovation et l&apos;inclusion. Elle prépare les étudiants aux défis du monde professionnel à travers des formations en <strong className="text-white">Gestion</strong> et en <strong className="text-white">Technologie</strong>.
                </p>
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <BookOpen className="w-8 h-8 text-amber-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">9+</p>
                    <p className="text-zinc-400 text-sm">Filières</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Users className="w-8 h-8 text-amber-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">2</p>
                    <p className="text-zinc-400 text-sm">Campus</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Award className="w-8 h-8 text-amber-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-white">Licence</p>
                    <p className="text-zinc-400 text-sm">Diplôme</p>
                  </div>
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-center">
                    <Building2 className="w-8 h-8 text-amber-500 mx-auto mb-2" />
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
            <div className="w-20 h-1 bg-amber-500 mx-auto mb-4" />
            <p className="text-zinc-400 text-center max-w-2xl mx-auto mb-12">Des formations professionnelles en Licence dans les domaines de la Gestion et de la Technologie</p>
          </Reveal>
          {Object.entries(FILIERES).map(([category, fils], idx) => (
            <Reveal key={category} delay={idx * 0.2}>
              <div className="mb-12">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-amber-500/10 flex items-center justify-center">
                    {category === 'Gestion' ? <BarChart3 className="w-6 h-6 text-amber-500" /> : <Settings className="w-6 h-6 text-amber-500" />}
                  </div>
                  <h3 className="text-2xl font-bold text-white">{category}</h3>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {fils.map((f, i) => (
                    <motion.div
                      key={f}
                      whileHover={{ scale: 1.03, borderColor: 'rgb(245, 158, 11)' }}
                      className="bg-zinc-900 border border-zinc-800 rounded-xl p-5 cursor-default transition-all"
                    >
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 rounded bg-amber-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-amber-500 text-sm font-bold">{i + 1}</span>
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
            <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">Inscription</h2>
            <div className="w-20 h-1 bg-amber-500 mx-auto mb-12" />
          </Reveal>
          <div className="grid sm:grid-cols-2 gap-6">
            <Reveal delay={0.1}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-amber-500 flex items-center gap-2"><FileText className="w-5 h-5" /> Nouvelle inscription</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Frais d&apos;inscription : <span className="text-amber-500 font-bold text-lg">25 000 FCFA</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Dossier à fournir sur place lors de la rentrée</p>
                </CardContent>
              </Card>
            </Reveal>
            <Reveal delay={0.2}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-amber-500 flex items-center gap-2"><CreditCard className="w-5 h-5" /> Réinscription</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Réinscription : <span className="text-green-400 font-bold text-lg">Gratuite</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Se reconnecter avec vos identifiants existants</p>
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
            <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">Contact</h2>
            <div className="w-20 h-1 bg-amber-500 mx-auto mb-12" />
          </Reveal>
          <div className="grid sm:grid-cols-2 gap-6">
            <Reveal delay={0.1}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Brazzaville</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> Brazzaville, République du Congo</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 06 822 91 78</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 05 557 58 32</p>
                </CardContent>
              </Card>
            </Reveal>
            <Reveal delay={0.2}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Pointe-Noire</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> 82 Avenue Nelson Mandela, entre le rond-point ILAMA et la route de l&apos;aéroport</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Mail className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> info@estamuni.net</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Globe className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> estam.cg</p>
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
            <img src="/estam/IMG_1627.webp" alt="ESTAM" className="w-8 h-8 rounded-full object-cover" />
            <span className="text-amber-500 font-bold">ESTAM</span>
          </div>
          <p className="text-zinc-500 text-xs text-center">
            © {new Date().getFullYear()} École Supérieure des Technologies Avancées et de Management. Tous droits réservés.
          </p>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" className="text-zinc-500 hover:text-amber-500 text-xs" onClick={() => setPage('admin-login')}>
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

function Globe({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" /><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
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
          <img src="/estam/IMG_1627.webp" alt="ESTAM" className="w-16 h-16 rounded-full mx-auto border-2 border-amber-500/50 object-cover mb-4" />
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
                <div><Label className="text-zinc-300">Email *</Label><Input type="email" className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.email} onChange={e => update('email', e.target.value)} required /></div>
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
                  <Select value={form.filiere} onValueChange={v => update('filiere', v)}>
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
              <Button type="submit" disabled={loading} className="w-full bg-amber-500 text-black hover:bg-amber-600">
                {loading ? 'Inscription en cours...' : "S'inscrire"}
              </Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <p className="text-zinc-400 text-sm">Déjà inscrit ? <button onClick={() => setPage('login')} className="text-amber-500 hover:underline">Se connecter</button></p>
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
      setPage('login')
    } catch { setError('Erreur de connexion') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="w-full max-w-md">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader className="text-center">
            <CheckCircle2 className="w-12 h-12 text-amber-500 mx-auto mb-4" />
            <CardTitle className="text-white text-xl">Inscription réussie !</CardTitle>
            <CardDescription className="text-zinc-400">Vérifiez votre boîte email</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-zinc-800 rounded-lg p-4 space-y-2">
              <p className="text-zinc-400 text-xs">Votre identifiant étudiant</p>
              <p className="text-amber-500 font-bold text-lg font-mono">{registeredStudentId}</p>
              <p className="text-zinc-400 text-xs">Email : {registeredEmail}</p>
            </div>
            <p className="text-zinc-300 text-sm text-center">Un code de vérification a été envoyé à votre adresse email. Saisissez-le ci-dessous :</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input className="bg-zinc-800 border-zinc-700 text-white text-center text-2xl tracking-[0.5em] font-mono" maxLength={6} value={code} onChange={e => setCode(e.target.value.replace(/\D/g, ''))} placeholder="000000" required />
              {error && <p className="text-red-400 text-sm text-center flex items-center justify-center gap-1"><AlertCircle className="w-4 h-4" />{error}</p>}
              <Button type="submit" disabled={loading} className="w-full bg-amber-500 text-black hover:bg-amber-600">{loading ? 'Vérification...' : 'Vérifier mon compte'}</Button>
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
          <img src="/estam/IMG_1627.webp" alt="ESTAM" className="w-16 h-16 rounded-full mx-auto border-2 border-amber-500/50 object-cover mb-4" />
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
              <Button type="submit" disabled={loading} className="w-full bg-amber-500 text-black hover:bg-amber-600">{loading ? 'Connexion...' : 'Se connecter'}</Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <p className="text-zinc-400 text-sm">Pas encore de compte ? <button onClick={() => setPage('register')} className="text-amber-500 hover:underline">S&apos;inscrire</button></p>
              <button onClick={() => setPage('admin-login')} className="text-zinc-500 hover:text-zinc-300 text-xs">Accès Administration</button>
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
          <Shield className="w-16 h-16 text-amber-500 mx-auto mb-4" />
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
              <Button type="submit" disabled={loading} className="w-full bg-amber-500 text-black hover:bg-amber-600">{loading ? 'Connexion...' : 'Se connecter'}</Button>
            </form>
            <div className="text-center mt-4 space-y-2">
              <button onClick={() => setPage('login')} className="text-zinc-400 text-sm hover:text-amber-500">Connexion Étudiant</button>
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

  if (!student) return null

  const unreadNotifs = notifications.filter(n => !n.lu).length
  const paidCount = payments.filter(p => p.statut === 'paye').length
  const unpaidCount = payments.filter(p => p.statut === 'impaye').length

  const markRead = async (id: string) => {
    await fetch('/api/notifications', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ notificationId: id }) })
    setNotifications(notifications.map(n => n.id === id ? { ...n, lu: true } : n))
  }

  const handleLogout = () => {
    setStudent(null); setGrades([]); setPayments([]); setNotifications([])
    setPage('landing')
  }

  const menuItems = [
    { id: 'dashboard', icon: BarChart3, label: 'Tableau de bord' },
    { id: 'notes', icon: BookOpen, label: 'Mes Notes' },
    { id: 'paiements', icon: CreditCard, label: 'Mes Paiements' },
    { id: 'notifications', icon: Bell, label: `Notifications${unreadNotifs > 0 ? ` (${unreadNotifs})` : ''}` },
    { id: 'profil', icon: User, label: 'Mon Profil' },
  ]

  return (
    <div className="min-h-screen bg-black flex">
      {/* Mobile overlay */}
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}
      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col transition-transform lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-4 border-b border-zinc-800 flex items-center gap-3">
          <img src="/estam/IMG_1627.webp" alt="ESTAM" className="w-10 h-10 rounded-full object-cover" />
          <div>
            <p className="text-amber-500 font-bold text-sm">ESTAM</p>
            <p className="text-zinc-500 text-xs">Espace Étudiant</p>
          </div>
          <button className="ml-auto lg:hidden text-zinc-400" onClick={() => setSidebarOpen(false)}><X className="w-5 h-5" /></button>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {menuItems.map(item => (
            <button key={item.id} onClick={() => { setTab(item.id); setSidebarOpen(false) }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${tab === item.id ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-white hover:bg-zinc-800'}`}>
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

      {/* Main */}
      <main className="flex-1 min-h-screen">
        <header className="sticky top-0 z-30 bg-black/80 backdrop-blur-md border-b border-zinc-800 px-4 sm:px-6 h-14 flex items-center gap-4">
          <button className="lg:hidden text-zinc-400" onClick={() => setSidebarOpen(true)}><Menu className="w-6 h-6" /></button>
          <h2 className="text-white font-semibold text-sm sm:text-base">{menuItems.find(m => m.id === tab)?.label}</h2>
          <div className="ml-auto flex items-center gap-3">
            <Badge variant="outline" className="border-amber-500/30 text-amber-500 text-xs font-mono">{student.studentId}</Badge>
            <div className="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 text-sm font-bold">
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
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-amber-500">{grades.length}</p><p className="text-zinc-400 text-xs">Notes</p></div>
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-green-400">{paidCount}</p><p className="text-zinc-400 text-xs">Payés</p></div>
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-red-400">{unpaidCount}</p><p className="text-zinc-400 text-xs">Impayés</p></div>
                      <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-amber-400">{unreadNotifs}</p><p className="text-zinc-400 text-xs">Notifications</p></div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
              {/* Recent notifications */}
              {notifications.slice(0, 3).map(n => (
                <motion.div key={n.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
                  <Card className={`bg-zinc-900 border-zinc-800 ${!n.lu ? 'border-l-2 border-l-amber-500' : ''}`}>
                    <CardContent className="py-3 px-4 flex items-start gap-3">
                      <Bell className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-white text-sm font-medium">{n.titre}</p>
                        <p className="text-zinc-400 text-xs mt-0.5 truncate">{n.message}</p>
                      </div>
                      <span className="text-zinc-600 text-xs flex-shrink-0">{new Date(n.createdAt).toLocaleDateString('fr-FR')}</span>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
              {notifications.length === 0 && <p className="text-zinc-500 text-sm text-center py-8">Aucune notification</p>}
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
                            <td className="px-4 py-3 font-bold text-amber-500">{g.note}</td>
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
                        <p className="text-amber-500 font-bold text-lg">{p.montant.toLocaleString()} FCFA</p>
                        {p.datePaiement && <p className="text-zinc-500 text-xs mt-1">Date : {p.datePaiement}</p>}
                        <p className="text-zinc-600 text-xs mt-1">Année : {p.anneeScolaire}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {/* Notifications Tab */}
          {tab === 'notifications' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
              {notifications.length === 0 && <p className="text-zinc-500 text-sm text-center py-12">Aucune notification</p>}
              {notifications.map(n => (
                <Card key={n.id} className={`bg-zinc-900 border-zinc-800 cursor-pointer transition hover:border-zinc-600 ${!n.lu ? 'border-l-2 border-l-amber-500' : ''}`}
                  onClick={() => !n.lu && markRead(n.id)}>
                  <CardContent className="py-4 px-4">
                    <div className="flex items-start gap-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${n.type === 'note' ? 'bg-amber-500/20' : n.type === 'paiement' ? 'bg-green-500/20' : 'bg-blue-500/20'}`}>
                        {n.type === 'note' ? <BookOpen className="w-4 h-4 text-amber-500" /> : n.type === 'paiement' ? <CreditCard className="w-4 h-4 text-green-400" /> : <Bell className="w-4 h-4 text-blue-400" />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="text-white text-sm font-medium">{n.titre}</p>
                          {!n.lu && <span className="w-2 h-2 rounded-full bg-amber-500" />}
                        </div>
                        <p className="text-zinc-400 text-xs mt-1">{n.message}</p>
                        <p className="text-zinc-600 text-xs mt-1">{new Date(n.createdAt).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </motion.div>
          )}

          {/* Profil Tab */}
          {tab === 'profil' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <Card className="bg-zinc-900 border-zinc-800">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 text-2xl font-bold">
                      {student.firstName[0]}{student.lastName[0]}
                    </div>
                    <div>
                      <CardTitle className="text-white">{student.firstName} {student.lastName}</CardTitle>
                      <CardDescription className="text-amber-500 font-mono">{student.studentId}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
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
                        <item.icon className="w-4 h-4 text-amber-500 flex-shrink-0" />
                        <div><p className="text-zinc-500 text-xs">{item.label}</p><p className="text-white text-sm">{item.value}</p></div>
                      </div>
                    ))}
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

  const handleLogout = () => { setAdmin(false); setPage('landing') }

  const openStudent = async (studentId: string) => {
    try {
      const res = await fetch(`/api/students/by-studentid?studentId=${studentId}`)
      const data = await res.json()
      if (data.student) { setSelectedStudent(data.student as Record<string, unknown>); setTab('student-detail') }
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
    { id: 'gestion', icon: Users, label: 'Gestion' },
    { id: 'technologie', icon: Settings, label: 'Technologie' },
    { id: 'parametres', icon: Settings, label: 'Paramètres' },
  ]

  return (
    <div className="min-h-screen bg-black flex">
      {sidebarOpen && <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col transition-transform lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-4 border-b border-zinc-800 flex items-center gap-3">
          <Shield className="w-8 h-8 text-amber-500" />
          <div>
            <p className="text-amber-500 font-bold text-sm">ESTAM Admin</p>
            <p className="text-zinc-500 text-xs">{adminEmail}</p>
          </div>
          <button className="ml-auto lg:hidden text-zinc-400" onClick={() => setSidebarOpen(false)}><X className="w-5 h-5" /></button>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          {adminMenu.map(item => (
            <button key={item.id} onClick={() => { setTab(item.id); setSidebarOpen(false); setSelectedStudent(null) }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${tab === item.id ? 'bg-amber-500/10 text-amber-500' : 'text-zinc-400 hover:text-white hover:bg-zinc-800'}`}>
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
              <button onClick={() => { setTab(selectedCategory === 'Gestion' ? 'gestion' : 'technologie'); setSelectedStudent(null) }} className="flex items-center gap-2 text-zinc-400 hover:text-white">
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
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><p className="text-2xl font-bold text-amber-500">{students.length || '-'}</p><p className="text-zinc-400 text-xs">Total étudiants</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Users className="w-6 h-6 text-green-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Gestion</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Settings className="w-6 h-6 text-blue-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Technologie</p></div>
                    <div className="bg-zinc-800 rounded-lg p-4 text-center"><Bell className="w-6 h-6 text-amber-400 mx-auto mb-1" /><p className="text-zinc-400 text-xs">Activité</p></div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Gestion / Technologie Tab */}
          {(tab === 'gestion' || tab === 'technologie') && !selectedStudent && (
            <div className="space-y-6">
              {!selectedFiliere ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <h3 className="text-white font-semibold mb-4">Sélectionnez une filière en {tab === 'gestion' ? 'Gestion' : 'Technologie'}</h3>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {FILIERES[tab === 'gestion' ? 'Gestion' : 'Technologie'].map((f, i) => (
                      <Card key={f} className="bg-zinc-900 border-zinc-800 cursor-pointer hover:border-amber-500/50 transition" onClick={() => { setSelectedCategory(tab === 'gestion' ? 'Gestion' : 'Technologie'); setSelectedFiliere(f); setSearchQuery('') }}>
                        <CardContent className="pt-4 flex items-center gap-3">
                          <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-500 font-bold">{i + 1}</div>
                          <div>
                            <p className="text-white text-sm font-medium">{f}</p>
                            <p className="text-zinc-500 text-xs">Cliquez pour voir les étudiants</p>
                          </div>
                          <ChevronRight className="w-5 h-5 text-zinc-600 ml-auto" />
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </motion.div>
              ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <button onClick={() => { setSelectedFiliere(null); setStudents([]) }} className="flex items-center gap-2 text-zinc-400 hover:text-white text-sm"><ArrowLeft className="w-4 h-4" />Retour aux filières</button>
                  <h3 className="text-white font-semibold">{selectedFiliere}</h3>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                    <Input className="pl-10 bg-zinc-900 border-zinc-800 text-white" placeholder="Rechercher par identifiant (EST...)" value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
                  </div>
                  {loading ? <p className="text-zinc-500 text-sm">Chargement...</p> : students.length === 0 ? (
                    <p className="text-zinc-500 text-sm text-center py-12">Aucun étudiant trouvé dans cette filière</p>
                  ) : (
                    <div className="space-y-2">
                      {students.map(s => {
                        const st = s as Record<string, string>
                        return (
                          <Card key={st.id} className="bg-zinc-900 border-zinc-800 cursor-pointer hover:border-amber-500/50 transition" onClick={() => openStudent(st.studentId)}>
                            <CardContent className="py-3 px-4 flex items-center gap-4">
                              <div className="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 font-bold text-sm">{(st.firstName || '?')[0]}{(st.lastName || '?')[0]}</div>
                              <div className="flex-1 min-w-0">
                                <p className="text-white text-sm font-medium">{st.firstName} {st.lastName}</p>
                                <p className="text-zinc-500 text-xs font-mono">{st.studentId} · {st.niveau}</p>
                              </div>
                              <Badge variant="outline" className={st.verified === 'true' ? 'border-green-500/30 text-green-400' : 'border-zinc-700 text-zinc-500'}>{st.verified === 'true' ? 'Vérifié' : 'Non vérifié'}</Badge>
                              <ChevronRight className="w-5 h-5 text-zinc-600" />
                            </CardContent>
                          </Card>
                        )
                      })}
                    </div>
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
                {/* Student Info */}
                <Card className="bg-zinc-900 border-zinc-800">
                  <CardHeader>
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 text-xl font-bold">{String(s.firstName || '?')[0]}{String(s.lastName || '?')[0]}</div>
                      <div>
                        <CardTitle className="text-white">{String(s.firstName)} {String(s.lastName)}</CardTitle>
                        <CardDescription className="text-amber-500 font-mono">{String(s.studentId)} · {String(s.filiere)} · {String(s.niveau)}</CardDescription>
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
                            <tr key={g.id} className="border-b border-zinc-800/50"><td className="px-3 py-2 text-white">{g.matiere}</td><td className="px-3 py-2 text-zinc-400">{g.type}</td><td className="px-3 py-2 text-amber-500 font-bold">{g.note}</td><td className="px-3 py-2 text-zinc-400">{g.semestre}</td></tr>
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
                      <Button type="submit" className="bg-amber-500 text-black hover:bg-amber-600">Publier</Button>
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
                              <p className="text-amber-500 font-bold text-sm">{Number(p.montant).toLocaleString()} F</p>
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
                      <Button type="submit" className="bg-amber-500 text-black hover:bg-amber-600 sm:col-span-2">Enregistrer</Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            )
          })()}

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
                    <Button type="submit" className="w-full bg-amber-500 text-black hover:bg-amber-600">Modifier le mot de passe</Button>
                  </form>
                  <div className="mt-6 p-4 bg-zinc-800 rounded-lg">
                    <p className="text-zinc-500 text-xs">Identifiants par défaut</p>
                    <p className="text-zinc-300 text-sm">Email : <span className="text-amber-500 font-mono">admin@estam.cg</span></p>
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

  // Ensure admin exists on load
  useEffect(() => {
    fetch('/api/auth/register').catch(() => {})
  }, [])

  switch (currentPage) {
    case 'landing': return <LandingPage />
    case 'register': return <RegisterPage />
    case 'verify': return <VerifyPage />
    case 'login': return <LoginPage />
    case 'admin-login': return <AdminLoginPage />
    case 'loading': return <LoadingPage targetPage="student-dashboard" />
    case 'admin-loading': return <LoadingPage targetPage="admin-dashboard" />
    case 'student-dashboard': return <StudentDashboard />
    case 'admin-dashboard': return <AdminDashboard />
    default: return <LandingPage />
  }
}