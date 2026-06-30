import type { FC } from "react";

export const LauncherButton: FC<{
  label: string;
  onClick: () => void;
}> = ({ label, onClick }) => (
  <button className="ibuddy-widget-launcher" onClick={onClick} type="button">
    <span className="ibuddy-widget-launcher-icon" aria-hidden="true">
      <svg fill="none" height="20" viewBox="0 0 24 24" width="20">
        <path
          d="M12 3c4.97 0 9 3.58 9 8 0 2.23-1.03 4.24-2.69 5.69-.41.36-.68.88-.72 1.42l-.09 1.21c-.05.73-.08 1.09-.3 1.29-.21.19-.55.16-1.23.1l-2.06-.2a2.32 2.32 0 0 0-1.39.26A10.03 10.03 0 0 1 12 21c-4.97 0-9-3.58-9-8s4.03-10 9-10Zm-3.5 8.75a1.25 1.25 0 1 0 0 2.5 1.25 1.25 0 0 0 0-2.5Zm3.5 0a1.25 1.25 0 1 0 0 2.5 1.25 1.25 0 0 0 0-2.5Zm3.5 0a1.25 1.25 0 1 0 0 2.5 1.25 1.25 0 0 0 0-2.5Z"
          fill="currentColor"
        />
      </svg>
    </span>
    <span className="ibuddy-widget-launcher-label">
      <span className="ibuddy-widget-launcher-title">{label}</span>
      <span className="ibuddy-widget-launcher-copy">Open secure chat</span>
    </span>
  </button>
);
