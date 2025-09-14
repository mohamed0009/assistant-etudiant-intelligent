import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"

import { Suspense } from "react"
import "./globals.css"
import { ThemeWrapper } from "@/components/theme-wrapper"
import { SiteFooter } from "@/components/site-footer"

export const metadata: Metadata = {
  title: "Assistant Étudiant Intelligent",
  description: "Assistant IA pour étudiants universitaires",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr" className={`${GeistSans.variable} ${GeistMono.variable} antialiased`}>
      <body>
        <ThemeWrapper>
          <div className="min-h-dvh flex flex-col relative overflow-hidden">
            {/* Global animated background blobs */}
            <div className="pointer-events-none absolute inset-0 -z-10">
              <div className="blob blob-static -top-24 -left-24 h-80 w-80 bg-primary/15" />
              <div className="blob delay-2 top-1/3 -right-24 h-80 w-80 bg-secondary/15" />
              <div className="blob delay-4 -bottom-24 left-1/3 h-80 w-80 bg-accent/15" />
            </div>
            <main className="flex-1 container mx-auto px-4 py-6">
              <Suspense fallback={null}>{children}</Suspense>
            </main>
            <SiteFooter />
          </div>
        </ThemeWrapper>
      </body>
    </html>
  )
}
