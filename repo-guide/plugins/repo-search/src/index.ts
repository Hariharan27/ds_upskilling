import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";
import { readdir, readFile } from "node:fs/promises";
import { join, relative } from "node:path";

const configSchema = Type.Object({
  repositoryPath: Type.String({
    description: "Absolute path to the repository that RepoGuide is allowed to search.",
  }),
});

async function searchRepository(
  repositoryPath: string,
  query: string,
): Promise<Array<{ file: string; matches: string[] }>> {
  const results: Array<{ file: string; matches: string[] }> = [];
  const normalizedQuery = query.toLowerCase();

  async function walk(directory: string): Promise<void> {
    const entries = await readdir(directory, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = join(directory, entry.name);

      if (entry.isDirectory()) {
        if (
          entry.name === "node_modules" ||
          entry.name === ".git" ||
          entry.name === "__pycache__"
        ) {
          continue;
        }

        await walk(fullPath);
        continue;
      }

      try {
        const content = await readFile(fullPath, "utf8");

        if (!content.toLowerCase().includes(normalizedQuery)) {
          continue;
        }

        const lines = content.split(/\r?\n/);
        const matches = lines
          .map((line, index) => ({
            lineNumber: index + 1,
            line,
          }))
          .filter(({ line }) =>
            line.toLowerCase().includes(normalizedQuery),
          )
          .slice(0, 20)
          .map(({ lineNumber, line }) => `${lineNumber}: ${line}`);

        results.push({
          file: relative(repositoryPath, fullPath),
          matches,
        });
      } catch {
        // Ignore files that cannot be read as UTF-8 text.
      }
    }
  }

  await walk(repositoryPath);

  return results;
}

export default defineToolPlugin({
  id: "repo-search",
  name: "Repo Search",
  description: "Search repository files and return matching evidence.",
  configSchema,

  tools: (tool) => [
    tool({
      name: "repo_search",
      description:
        "Search the configured repository for a text query and return matching files and line evidence.",

      parameters: Type.Object({
        query: Type.String({
          description:
            "Text to search for in the repository, such as a filename, class name, function name, configuration key, or phrase.",
        }),
      }),

      execute: async ({ query }, config) => {
        const results = await searchRepository(
          config.repositoryPath,
          query,
        );

        return {
          query,
          repositoryPath: config.repositoryPath,
          matchCount: results.length,
          results,
        };
      },
    }),
  ],
});