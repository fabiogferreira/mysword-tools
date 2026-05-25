import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MySword Tools - Convert Word to MySword Format",
  description: "Convert your study .docx files to MySword Bible study journal databases easily. Includes automatic verse linking, formatting preserving, and lesson splitting.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body>{children}</body>
    </html>
  );
}
