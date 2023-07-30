import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Health Monitor',
  description: 'Written by Henry Forsyth',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
      <html lang="en">
        <body>{children}</body>
      </html>
  )
}
