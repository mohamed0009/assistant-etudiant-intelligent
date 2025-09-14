export function SiteFooter() {
  return (
    <footer className="border-t bg-background">
      <div className="container mx-auto px-4 py-8 grid gap-6 md:grid-cols-3 items-start">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground font-bold">AI</span>
          <div>
            <p className="text-sm font-semibold">Assistant Étudiant</p>
            <p className="text-xs text-foreground/60">IA universitaire, fiable et moderne</p>
          </div>
        </div>
        <nav className="text-sm text-foreground/70 grid grid-cols-2 gap-2">
          <a href="/confidentialite" className="hover:text-foreground">Confidentialité</a>
          <a href="/conditions" className="hover:text-foreground">Conditions</a>
          <a href="/contact" className="hover:text-foreground">Contact</a>
          <a href="/a-propos" className="hover:text-foreground">À propos</a>
        </nav>
        <div className="justify-self-start md:justify-self-end text-sm text-foreground/70">
          © {new Date().getFullYear()} Assistant Étudiant
        </div>
      </div>
      <div className="border-t">
        <div className="container mx-auto px-4 py-3 text-xs text-foreground/60 flex items-center gap-2">
          <span className="inline-block h-1.5 w-1.5 rounded-full bg-primary" />
          Optimisé pour la rapidité, l’accessibilité et tous les écrans
        </div>
      </div>
    </footer>
  )
}



