import { useLayoutEffect, type RefObject } from "react";

export function useAutoResizeTextarea(
  ref: RefObject<HTMLTextAreaElement | null>,
  value: string
): void {
  useLayoutEffect(() => {
    const element = ref.current;

    if (!element) {
      return;
    }

    element.style.height = "0px";
    element.style.height = `${Math.min(element.scrollHeight, 132)}px`;
  }, [ref, value]);
}
