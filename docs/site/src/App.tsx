type DocSection = {
  id: string
  title: string
  summary: string
  bullets: string[]
}

const navSections: DocSection[] = [
  {
    id: 'overview',
    title: 'Overview',
    summary: 'lavoix is the speech gateway used by Seal and Otter for STT/TTS operations.',
    bullets: [
      'Primary STT path: Mistral Voxtral',
      'Primary TTS path: Voxtral TTS + OSS fallback',
      'Runs as both a Python library and FastAPI server',
    ],
  },
  {
    id: 'providers',
    title: 'Provider Model',
    summary: 'Providers are explicit interfaces so each engine can be swapped without changing API contracts.',
    bullets: [
      'Base provider contract in src/lavoix/providers/base.py',
      'Mistral providers for STT and TTS',
      'OSS fallback provider (pyttsx3) for local/offline TTS',
    ],
  },
  {
    id: 'api',
    title: 'HTTP API',
    summary: 'FastAPI endpoints expose deterministic speech operations with typed request/response schemas.',
    bullets: [
      'GET /healthz for service readiness',
      'POST /v1/stt/transcribe for speech-to-text',
      'POST /v1/tts/synthesize for text-to-speech',
    ],
  },
  {
    id: 'config',
    title: 'Configuration',
    summary: 'Runtime behavior is controlled by LAVOIX_* environment variables and typed settings.',
    bullets: [
      'LAVOIX_MISTRAL_API_KEY for Voxtral provider access',
      'Provider defaults for STT and TTS',
      'Service port and model selection are configurable',
    ],
  },
  {
    id: 'integration',
    title: 'Integration',
    summary: 'Otter forwards voice prompts to lavoix while Seal consumes the resulting orchestration flow.',
    bullets: [
      'Otter -> lavoix for transcription',
      'Seal -> Otter voice endpoints for UX',
      'Standalone usage via Python SDK is also supported',
    ],
  },
]

function App() {
  return (
    <main className="min-h-screen bg-rust-bg text-rust-text">
      <div className="border-b border-rust-border bg-rust-panel/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
          <a href="#overview" className="text-lg font-semibold tracking-wide text-rust-accentSoft">
            lavoix docs
          </a>
          <nav className="flex flex-wrap gap-2">
            {navSections.map((section) => (
              <a
                key={section.id}
                href={`#${section.id}`}
                className="rounded-md border border-rust-border px-3 py-1.5 text-sm text-rust-muted transition hover:bg-rust-panelSoft hover:text-rust-text"
              >
                {section.title}
              </a>
            ))}
          </nav>
        </div>
      </div>

      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 lg:grid-cols-[260px_minmax(0,1fr)]">
        <aside className="h-fit rounded-2xl border border-rust-border bg-rust-panel p-5 shadow-glow lg:sticky lg:top-6">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-rust-accentSoft">Sections</p>
          <div className="mt-4 space-y-2">
            {navSections.map((section) => (
              <a
                key={section.id}
                href={`#${section.id}`}
                className="block rounded-lg border border-transparent px-3 py-2 text-sm text-rust-muted transition hover:border-rust-border hover:bg-rust-panelSoft hover:text-rust-text"
              >
                {section.title}
              </a>
            ))}
          </div>
          <a
            href="https://github.com/Unchained-Labs/lavoix"
            target="_blank"
            rel="noreferrer"
            className="mt-6 inline-flex rounded-lg bg-rust-accent px-3 py-2 text-sm font-semibold text-white transition hover:opacity-90"
          >
            GitHub Repository
          </a>
        </aside>

        <section className="space-y-4">
          {navSections.map((section) => (
            <article
              key={section.id}
              id={section.id}
              className="scroll-mt-24 rounded-2xl border border-rust-border bg-rust-panel p-6 shadow-glow"
            >
              <h2 className="text-2xl font-semibold">{section.title}</h2>
              <p className="mt-2 text-rust-muted">{section.summary}</p>
              <ul className="mt-4 grid gap-2">
                {section.bullets.map((bullet) => (
                  <li key={bullet} className="rounded-lg border border-rust-border bg-rust-panelSoft px-3 py-2 text-sm">
                    {bullet}
                  </li>
                ))}
              </ul>
            </article>
          ))}

          <article id="commands" className="scroll-mt-24 rounded-2xl border border-rust-border bg-rust-panel p-6 shadow-glow">
            <h2 className="text-2xl font-semibold">Site Commands</h2>
            <pre className="mt-3 overflow-auto rounded-lg bg-rust-bg p-4 text-sm text-rust-accentSoft">
{`cd docs/site
npm install
npm run dev
npm run build
npm run preview`}
            </pre>
          </article>
        </section>
      </div>
    </main>
  )
}

export default App
