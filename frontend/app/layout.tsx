import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "ALZERA | Clinical Decision Support", description: "Progressive diagnostic prioritization prototype" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
