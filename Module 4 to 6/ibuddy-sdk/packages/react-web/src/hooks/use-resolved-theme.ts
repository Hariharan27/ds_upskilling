import { useEffect, useState } from "react";
import type { IBuddyWidgetTheme } from "../types.js";

function readSystemTheme(): Exclude<IBuddyWidgetTheme, "system"> {
  if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
    return "light";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function useResolvedTheme(theme: IBuddyWidgetTheme): "light" | "dark" {
  const [resolvedTheme, setResolvedTheme] = useState<"light" | "dark">(
    theme === "system" ? readSystemTheme() : theme
  );

  useEffect(() => {
    if (theme !== "system") {
      setResolvedTheme(theme);
      return;
    }

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const applyTheme = () => setResolvedTheme(mediaQuery.matches ? "dark" : "light");

    applyTheme();
    mediaQuery.addEventListener("change", applyTheme);

    return () => {
      mediaQuery.removeEventListener("change", applyTheme);
    };
  }, [theme]);

  return resolvedTheme;
}
