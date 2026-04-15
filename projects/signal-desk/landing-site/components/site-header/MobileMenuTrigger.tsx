"use client";

import { useState } from "react";

export function MobileMenuTrigger() {
  const [open, setOpen] = useState(false);
  // Sheet implementation intentionally deferred — this is the trigger surface only.
  return (
    <>
      <button
        type="button"
        aria-label={open ? "메뉴 닫기" : "메뉴 열기"}
        aria-expanded={open}
        aria-controls="mobile-menu"
        onClick={() => setOpen((v) => !v)}
        className="mobile-menu-trigger"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          width: "44px",
          height: "44px",
          background: "var(--color-button-ghost-surface-default)",
          color: "var(--color-button-ghost-text-default)",
          border: "1px solid var(--color-border)",
          borderRadius: "var(--radius-md)",
          cursor: "pointer",
          transition:
            "background var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
        }}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          aria-hidden="true"
        >
          <line x1="3" y1="6" x2="17" y2="6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="3" y1="10" x2="17" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="3" y1="14" x2="17" y2="14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
      </button>
      <style>{`
        @media (min-width: 768px) {
          .mobile-menu-trigger { display: none !important; }
        }
        .mobile-menu-trigger:hover {
          background: var(--color-button-ghost-surface-hover);
          color: var(--color-button-ghost-text-hover);
        }
      `}</style>
    </>
  );
}
