"use client";

import { useState } from "react";

const MOBILE_NAV_ITEMS = [
  { label: "리뷰", href: "#reviews" },
  { label: "비교표", href: "#compare" },
  { label: "랭킹", href: "#rankings" },
  { label: "탐색", href: "#discover" },
  { label: "방법론", href: "#methodology" },
];

export function MobileMenuTrigger() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-label={open ? "메뉴 닫기" : "메뉴 열기"}
        aria-expanded={open}
        aria-controls="mobile-menu"
        className="md:hidden"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          width: "44px",
          height: "44px",
          marginLeft: "auto",
          background: open ? "rgba(255,255,255,0.08)" : "transparent",
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
          {open ? (
            <>
              <line x1="5" y1="5" x2="15" y2="15" />
              <line x1="15" y1="5" x2="5" y2="15" />
            </>
          ) : (
            <>
              <line x1="3" y1="6" x2="17" y2="6" />
              <line x1="3" y1="10" x2="17" y2="10" />
              <line x1="3" y1="14" x2="17" y2="14" />
            </>
          )}
        </svg>
      </button>

      {open ? (
        <>
          <button
            type="button"
            aria-label="메뉴 닫기"
            onClick={() => setOpen(false)}
            className="md:hidden"
            style={{
              position: "fixed",
              inset: 0,
              zIndex: 55,
              border: 0,
              background: "rgba(8, 11, 16, 0.66)",
              backdropFilter: "blur(10px)",
            }}
          />
          <div
            id="mobile-menu"
            className="md:hidden"
            style={{
              position: "fixed",
              top: "76px",
              left: "16px",
              right: "16px",
              zIndex: 60,
              borderRadius: "24px",
              border: "1px solid rgba(255,255,255,0.08)",
              background:
                "linear-gradient(180deg, rgba(16,23,34,0.98) 0%, rgba(10,14,21,1) 100%)",
              boxShadow: "0 24px 64px rgba(0,0,0,0.34)",
              padding: "18px",
              display: "grid",
              gap: "12px",
            }}
          >
            <nav aria-label="모바일 내비게이션">
              <ul
                style={{
                  listStyle: "none",
                  margin: 0,
                  padding: 0,
                  display: "grid",
                  gap: "8px",
                }}
              >
                {MOBILE_NAV_ITEMS.map((item, index) => (
                  <li key={item.href}>
                    <a
                      href={item.href}
                      onClick={() => setOpen(false)}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        minHeight: "48px",
                        padding: "0 14px",
                        borderRadius: "16px",
                        color: "var(--color-text)",
                        textDecoration: "none",
                        background: "rgba(255,255,255,0.03)",
                        border: "1px solid rgba(255,255,255,0.08)",
                        fontWeight: 600,
                      }}
                    >
                      <span>{item.label}</span>
                      <span
                        aria-hidden="true"
                        style={{
                          color: "var(--color-brand-accent)",
                          fontFamily: "var(--font-mono)",
                        }}
                      >
                        {String(index + 1).padStart(2, "0")}
                      </span>
                    </a>
                  </li>
                ))}
              </ul>
            </nav>

            <div
              style={{
                display: "grid",
                gap: "10px",
                paddingTop: "8px",
                borderTop: "1px solid rgba(255,255,255,0.08)",
              }}
            >
              <a
                href="#newsletter"
                onClick={() => setOpen(false)}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  minHeight: "48px",
                  borderRadius: "16px",
                  background: "var(--color-brand-accent)",
                  color: "var(--color-text-inverse)",
                  textDecoration: "none",
                  fontWeight: 700,
                }}
              >
                금요일 요약 받기
              </a>
              <a
                href="#compare"
                onClick={() => setOpen(false)}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  minHeight: "48px",
                  borderRadius: "16px",
                  background: "rgba(255,255,255,0.03)",
                  color: "var(--color-text)",
                  textDecoration: "none",
                  fontWeight: 600,
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                구매 판단 표 보기
              </a>
            </div>
          </div>
        </>
      ) : null}
    </>
  );
}
