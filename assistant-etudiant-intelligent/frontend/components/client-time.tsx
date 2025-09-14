"use client"

import { useState, useEffect } from "react"

interface ClientTimeProps {
  timestamp: Date
  className?: string
}

export function ClientTime({ timestamp, className }: ClientTimeProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <span className={className}>--:--:--</span>
  }

  return (
    <span className={className}>
      {timestamp.toLocaleTimeString()}
    </span>
  )
}

