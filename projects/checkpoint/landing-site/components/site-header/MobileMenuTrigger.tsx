"use client";

import { useState } from "react";

// NOTE: The mobile sheet/drawer this trigger controls is a follow-up task.
// For now we toggle local state and log so the a11y wiring (aria-expanded /
// aria-controls) is in place and ready for the sheet implementation.
export function MobileMenuTrigger() {
  const [open, setOpen] = useState(false);

  const handleClick = () => {
    setOpen((prev) => {
      const next = !prev;
      if (typeof window !== "undefined") {
        console.log("[MobileMenuTrigger] toggled:", next);
      }
      return next;
    });
  };

  return (
    <>
      <button
        type="button"
        onClick={handleClick}
        aria-label="메뉴 열기"
        aria-expanded={open}
        aria-controls="mobile-menu"
        className="checkpoint-mobile-menu-trigger"
        style={{
          alignItems: "center",
          justifyContent: "center",
          width: "44px",
          height: "44px",
          marginLeft: "auto",
          background: "transparent",
          border: "1px solid var(--color-border)",
          borderRadius: "var(--radius-md)",
          color: "var(--color-text)",
          cursor: "pointer",
          transition:
            "background var(--duration-120) var(--ease-standard), border-color var(--duration-120) var(--ease-standard)",
        }}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.75"
          strokeLinecap="round"
          aria-hidden="true"
          focusable="false"
        >
          <line x1="3" y1="6" x2="17" y2="6" />
          <line x1="3" y1="10" x2="17" y2="10" />
          <line x1="3" y1="14" x2="17" y2="14" />
        </svg>
      </button>
      <style>{`
        .checkpoint-mobile-menu-trigger {
          display: inline-flex;
        }
        @media (min-width: 900px) {
          .checkpoint-mobile-menu-trigger {
            display: none;
          }
        }
      `}</style>
    </>
  );
}
