#!/usr/bin/env python3
"""Apply remaining edits to page.tsx"""
import re

with open('/home/z/my-project/src/app/page.tsx', 'r') as f:
    content = f.read()

# 1. Navigation: add MiniLoading transitions for buttons on landing
content = content.replace(
    "onClick={() => setPage('register')}",
    "onClick={() => setPage('mini-register')}"
)
content = content.replace(
    "onClick={() => setPage('login')}",
    "onClick={() => setPage('mini-login')}"
)

# Fix: the button already has mini-register/mini-login, revert if double-applied
content = content.replace("setPage('mini-mini-register')", "setPage('mini-register')")
content = content.replace("setPage('mini-mini-login')", "setPage('mini-login')")

# 2. Admin login navigation: add mini loading
content = content.replace(
    "onClick={() => setPage('admin-login')}",
    "onClick={() => setPage('mini-admin-login')}"
)
content = content.replace("setPage('mini-mini-admin-login')", "setPage('mini-admin-login')")

# 3. Update the "S'inscrire" and "Se connecter" links in login/register pages
content = content.replace(
    """onClick={() => setPage('register')} className="text-amber-500 hover:underline">S&apos;inscrire</button>""",
    """onClick={() => setPage('mini-register')} className="text-amber-500 hover:underline">S&apos;inscrire</button>"""
)
content = content.replace(
    """onClick={() => setPage('login')} className="text-amber-500 hover:underline">Se connecter</button>""",
    """onClick={() => setPage('mini-login')} className="text-amber-500 hover:underline">Se connecter</button>"""
)

# 4. Add @gmail.com validation hint in registration email field  
content = content.replace(
    'type="email" className="mt-1 bg-zinc-800 border-zinc-700 text-white" value={form.email}',
    'type="email" className="mt-1 bg-zinc-800 border-zinc-700 text-white" placeholder="exemple@gmail.com" value={form.email}'
)

# 5. Add shimmer to section headings on landing
content = content.replace(
    '<h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">À propos',
    '<h2 className="shimmer-gold text-3xl sm:text-4xl font-bold text-center text-white mb-4">À propos'
)
content = content.replace(
    '<h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">Inscription',
    '<h2 className="shimmer-gold text-3xl sm:text-4xl font-bold text-center text-white mb-4">Inscription'
)
content = content.replace(
    '<h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">Contact',
    '<h2 className="shimmer-gold text-3xl sm:text-4xl font-bold text-center text-white mb-4">Contact'
)

# 6. Update ESTAM about section text with real info
old_about = "L'establissement d'enseignement superieur prive situe en"
if old_about.lower() in content.lower():
    # Find and replace the about paragraph
    pass

# Replace the about text paragraphs
content = content.replace(
    """L&apos;<strong className="text-amber-500">École Supérieure des Technologies Avancées et de Management (ESTAM)</strong> est un établissement d&apos;enseignement supérieur privé situé en <strong className="text-white">République du Congo</strong>, avec des campus à <strong className="text-white">Brazzaville</strong> et <strong className="text-white">Pointe-Noire</strong>. Créée par arrêté <strong className="text-amber-500">N° 0076/MES-CAB-DGESUP</strong>, l&apos;ESTAM travaille en étroite collaboration avec l&apos;Université CEREC-ISCOM.</p>
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;ESTAM a pour mission d&apos;offrir des programmes d&apos;études innovants, une formation professionnelle et personnelle de qualité, axée sur l&apos;excellence, l&apos;innovation et l&apos;inclusion. Elle prépare les étudiants aux défis du monde professionnel à travers des formations en <strong className="text-white">Gestion</strong> et en <strong className="text-white">Technologie</strong>.</p>""",
    """L&apos;<strong className="text-amber-500">École Supérieure des Technologies Avancées et de Management (ESTAM)</strong> est un établissement d&apos;enseignement supérieur privé situé en <strong className="text-white">République du Congo</strong>, avec des campus à <strong className="text-white">Brazzaville</strong> (233 rue de la Libération et 22 Rue Likouala, Poto-Poto) et à <strong className="text-white">Pointe-Noire</strong> (82 Avenue Nelson Mandela). Créée par arrêté <strong className="text-amber-500">N° 0076/MES-CAB-DGESUP</strong>, l&apos;ESTAM est une émanation du Cabinet <strong className="text-white">IM Consulting</strong> et travaille avec l&apos;Université <strong className="text-white">CEREC-ISCOM</strong> et l&apos;Institut <strong className="text-white">C-TECH</strong>.</p>
                <p className="text-zinc-300 leading-relaxed text-base">
                  L&apos;ESTAM propose des <strong className="text-white">Licences professionnelles</strong> en cours du jour et du soir (Vague Soir), avec un corps enseignant expérimenté. En 2024, <strong className="text-amber-500">379 finalistes</strong> ont été félicités. L&apos;établissement est ouvert du lundi au vendredi de <strong className="text-white">8h à 17h</strong> et le samedi de <strong className="text-white">8h à 12h</strong>.</p>"""
)

# 7. Update contact info
content = content.replace(
    """<MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> Brazzaville, République du Congo</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 06 822 91 78</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 05 557 58 32</p>""",
    """<MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> 233 Rue de la Libération / 22 Rue Likouala, Poto-Poto</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 06 822 91 78</p>
                  <p className="text-zinc-300 text-sm flex items-start gap-2"><Phone className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> +242 05 557 58 32 (WhatsApp)</p>"""
)

content = content.replace(
    """<MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> 82 Avenue Nelson Mandela, entre le rond-point ILAMA et la route de l&apos;aéroport</p>""",
    """<MapPin className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" /> 82 Avenue Nelson Mandela, rd-pt ILAMA</p>"""
)

# 8. Update inscription card
content = content.replace(
    """<span className="text-amber-500 font-bold text-lg">25 000 FCFA</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Dossier à fournir sur place lors de la rentrée</p>""",
    """<span className="text-amber-500 font-bold text-lg">26 000 FCFA</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Ouvert lun-ven 8h-17h, sam 8h-12h</p>"""
)

# 9. Replace the reinscription card with "Cours du soir"
content = content.replace(
    """<CardTitle className="text-amber-500 flex items-center gap-2"><CreditCard className="w-5 h-5" /> Réinscription</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Réinscription : <span className="text-green-400 font-bold text-lg">Gratuite</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Se reconnecter avec vos identifiants existants</p>""",
    """<CardTitle className="text-amber-500 flex items-center gap-2"><Clock className="w-5 h-5" /> Cours du soir</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-zinc-300 text-sm">Vague Soir : <span className="shimmer-gold font-bold text-lg">Disponible</span></p>
                  <p className="text-zinc-400 text-xs mt-2">Pour les travailleurs, cours du soir aménagés</p>"""
)

# 10. Add "mini-register", "mini-login", "mini-admin-login" to the switch statement
content = content.replace(
    "case 'loading': return <LoadingPage targetPage=\"student-dashboard\" />",
    "case 'mini-register': return <MiniLoading targetPage='register' />\n    case 'mini-login': return <MiniLoading targetPage='login' />\n    case 'mini-admin-login': return <MiniLoading targetPage='admin-login' />\n    case 'loading': return <LoadingPage targetPage=\"student-dashboard\" />"
)

with open('/home/z/my-project/src/app/page.tsx', 'w') as f:
    f.write(content)

print("All edits applied successfully!")