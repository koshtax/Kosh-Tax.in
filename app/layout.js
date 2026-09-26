import './globals.css'

export const metadata = {
  title: 'Kosh-Tax | Form 16 Generator',
  description: 'Automated 7th CPC Form 16 Generation System',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-[#F4F7F6] text-slate font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
