/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_IBUDDY_BASE_URL?: string;
  readonly VITE_IBUDDY_ENDPOINT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
