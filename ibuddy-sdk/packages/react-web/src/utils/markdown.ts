/**
 * Lightweight markdown → HTML renderer for assistant messages.
 * Handles: headings (##/###), bold (**), italic (*), bullet lists (- / *), and paragraphs.
 * HTML-escapes content before processing to prevent XSS.
 */

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderInline(text: string): string {
  return (
    text
      // Bold: **text**
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      // Italic: *text* (not preceded/followed by *)
      .replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, "<em>$1</em>")
  );
}

function renderBlock(block: string): string {
  const lines = block.split("\n");

  // Heading ##
  if (/^##\s/.test(lines[0] ?? "")) {
    return `<h3 class="ibuddy-md-h3">${renderInline(escapeHtml((lines[0] ?? "").replace(/^##\s+/, "")))}</h3>`;
  }

  // Heading ###
  if (/^###\s/.test(lines[0] ?? "")) {
    return `<h4 class="ibuddy-md-h4">${renderInline(escapeHtml((lines[0] ?? "").replace(/^###\s+/, "")))}</h4>`;
  }

  // Bullet list: lines starting with "- " or "* "
  const bulletLines = lines.filter((line) => /^[-*]\s/.test(line));
  if (bulletLines.length > 0 && bulletLines.length === lines.length) {
    const items = lines
      .map((line) => `<li>${renderInline(escapeHtml(line.replace(/^[-*]\s+/, "")))}</li>`)
      .join("");
    return `<ul class="ibuddy-md-ul">${items}</ul>`;
  }

  // Mixed block: some lines are bullets, some are text — render line by line
  if (bulletLines.length > 0) {
    const rendered = lines
      .map((line) => {
        if (/^[-*]\s/.test(line)) {
          return `<li>${renderInline(escapeHtml(line.replace(/^[-*]\s+/, "")))}</li>`;
        }
        return `<span class="ibuddy-md-line">${renderInline(escapeHtml(line))}</span>`;
      })
      .join("");
    return `<div class="ibuddy-md-mixed">${rendered}</div>`;
  }

  // Plain paragraph — join lines with <br> to preserve single line breaks
  const content = lines
    .map((line) => renderInline(escapeHtml(line)))
    .join("<br>");

  return `<p class="ibuddy-md-p">${content}</p>`;
}

export function renderMarkdown(text: string): string {
  if (!text || text.trim().length === 0) {
    return "";
  }

  // Split on blank lines to get blocks
  const blocks = text.split(/\n{2,}/);
  return blocks.map(renderBlock).join("");
}
