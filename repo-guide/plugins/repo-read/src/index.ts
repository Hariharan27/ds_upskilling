import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";
import { readFile, stat } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep } from "node:path";

const configSchema = Type.Object({
  repositoryPath: Type.String({
    description:
      "Absolute path to the repository that RepoGuide is allowed to read.",
  }),
});

const MAX_FILE_SIZE = 512 * 1024; // 512 KB

async function readRepositoryFile(
  repositoryPath: string,
  filePath: string,
): Promise<string> {
  if (isAbsolute(filePath)) {
    throw new Error("filePath must be relative to the configured repository.");
  }

  const repositoryRoot = resolve(repositoryPath);
  const targetPath = resolve(repositoryRoot, filePath);
  const relativePath = relative(repositoryRoot, targetPath);

  if (
    relativePath === ".." ||
    relativePath.startsWith(`..${sep}`) ||
    isAbsolute(relativePath)
  ) {
    throw new Error("filePath must stay inside the configured repository.");
  }

  const fileInfo = await stat(targetPath);

  if (!fileInfo.isFile()) {
    throw new Error(`Not a file: ${filePath}`);
  }

  if (fileInfo.size > MAX_FILE_SIZE) {
    throw new Error(
      `File is too large to read. Maximum size is ${MAX_FILE_SIZE} bytes.`,
    );
  }

  const content = await readFile(targetPath, "utf8");

  const lines = content.split(/\r?\n/);

  return lines
    .map((line, index) => `${index + 1}: ${line}`)
    .join("\n");
}

export default defineToolPlugin({
  id: "repo-read",
  name: "Repo Read",
  description:
    "Read files from the configured repository and return line-numbered content.",
  configSchema,

  tools: (tool) => [
    tool({
      name: "repo_read",
      description:
        "Read a file from the configured repository using a repository-relative path.",
      parameters: Type.Object({
        filePath: Type.String({
          description:
            "Repository-relative file path, for example main.py or src/services/user.ts.",
        }),
      }),

      execute: async ({ filePath }, config) => {
        const content = await readRepositoryFile(
          config.repositoryPath,
          filePath,
        );

        return {
          filePath,
          repositoryPath: config.repositoryPath,
          content,
        };
      },
    }),
  ],
});