import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Zeta Zeros Lab — do the zeros of ζ(s) behave like random matrices?",
  description:
    "A reproducible, interactive test of whether 4,000 Riemann zeta zeros follow GUE random-matrix statistics, with a calibrated simulated null and a preregistered protocol.",
  applicationName: "Zeta Zeros Lab",
  keywords: [
    "Riemann zeta function",
    "random matrix theory",
    "GUE",
    "Montgomery-Odlyzko",
    "pair correlation",
    "reproducible research",
  ],
  openGraph: {
    title: "Zeta Zeros Lab",
    description: "Do the Riemann zeta zeros really look like random-matrix eigenvalues? Measured, not asserted.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Zeta Zeros Lab",
    description: "A reproducible test of GUE statistics in 4,000 Riemann zeta zeros.",
  },
  icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
    </html>
  );
}
