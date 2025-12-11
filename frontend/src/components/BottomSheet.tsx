'use client';

import { useEffect, useRef } from 'react';

interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function BottomSheet({ isOpen, onClose, title, children, footer }: BottomSheetProps) {
  const sheetRef = useRef<HTMLDivElement>(null);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  // Focus trap
  useEffect(() => {
    if (isOpen && sheetRef.current) {
      sheetRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 md:hidden">
      {/* Dimmed overlay - clicking closes the sheet */}
      <div 
        className="absolute inset-0 bg-black/50 transition-opacity duration-300"
        onClick={onClose}
        aria-hidden="true"
      />
      
      {/* Bottom Sheet Panel - 85% height */}
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'bottom-sheet-title' : undefined}
        tabIndex={-1}
        className="absolute bottom-0 left-0 right-0 bg-white rounded-t-3xl shadow-2xl transform transition-transform duration-300 ease-out flex flex-col"
        style={{ 
          height: '85vh',
          boxShadow: '0 -10px 40px -10px rgba(0, 29, 61, 0.25)',
        }}
      >
        {/* Drag Handle */}
        <div className="flex justify-center pt-3 pb-2">
          <div className="w-10 h-1 bg-slate-300 rounded-full" />
        </div>

        {/* Header */}
        {title && (
          <div className="px-6 pb-4 border-b border-warm-grey/30">
            <div className="flex items-center justify-between">
              <h2 
                id="bottom-sheet-title" 
                className="text-xl font-heading text-navy"
              >
                {title}
              </h2>
              <button
                onClick={onClose}
                className="p-2 rounded-full hover:bg-slate-100 transition-colors"
                aria-label="Închide"
              >
                <svg className="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {children}
        </div>

        {/* Footer (sticky at bottom) */}
        {footer && (
          <div className="px-6 py-4 border-t border-warm-grey/30 bg-white">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
