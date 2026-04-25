/* design-ontology:START */
// preset: conversation-copilot--minimal-tech
// adapter: nextjs-tailwind-shadcn@0.1.0
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx,js,jsx,mdx}",
    "./components/**/*.{ts,tsx,js,jsx,mdx}",
    "./design-system/**/*.{ts,tsx,js,jsx,mdx}",
  ],
  darkMode: ["class", "[data-theme='dark']"],
  theme: {
    extend: {
      colors: {
        ds: {
        "accent": "var(--ds-color-accent)",
        "border": "var(--ds-color-border)",
        "border-strong": "var(--ds-color-border-strong)",
        "canvas": "var(--ds-color-canvas)",
        "danger": "var(--ds-color-danger)",
        "info": "var(--ds-color-info)",
        "ink": "var(--ds-color-ink)",
        "ink-inverse": "var(--ds-color-ink-inverse)",
        "ink-muted": "var(--ds-color-ink-muted)",
        "ink-subtle": "var(--ds-color-ink-subtle)",
        "link": "var(--ds-color-link)",
        "link-hover": "var(--ds-color-link-hover)",
        "primary": "var(--ds-color-primary)",
        "success": "var(--ds-color-success)",
        "surface": "var(--ds-color-surface)",
        "surface-elevated": "var(--ds-color-surface-elevated)",
        "surface-muted": "var(--ds-color-surface-muted)",
        "surface-tint": "var(--ds-color-surface-tint)",
        "warning": "var(--ds-color-warning)"
        },
        "primary": "var(--ds-color-primary)",
        "accent": "var(--ds-color-accent)",
        "background": "var(--ds-color-canvas)",
        "foreground": "var(--ds-color-ink)",
        "border": "var(--ds-color-border)",
      },
      fontFamily: {
        "heading": ["var(--ds-font-heading)"],
        "sans": ["var(--ds-font-body)"],
        "mono": ["var(--ds-font-mono)"],
      },
      borderRadius: {
        "none": "0px",
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "20px",
        "pill": "999px"
      },
      spacing: {
        "ds-0": "0px",
        "ds-2": "2px",
        "ds-4": "4px",
        "ds-8": "8px",
        "ds-12": "12px",
        "ds-16": "16px",
        "ds-24": "24px",
        "ds-32": "32px",
        "ds-48": "48px",
        "ds-64": "64px",
        "ds-96": "96px"
      },
      fontSize: {
        "xs": "12px",
        "sm": "13px",
        "md": "15px",
        "lg": "19px",
        "xl": "24px",
        "2xl": "30px",
        "3xl": "37px"
      },
    },
  },
  plugins: [],
};

export default config;
/* design-ontology:END */
