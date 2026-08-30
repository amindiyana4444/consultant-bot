import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'پنل مدیریت مشاوره کنکور',
  description: 'سیستم مدیریت مشاوره کنکور',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  )
}
