const sections = [
  'Getting Started',
  'Architecture',
  'API Surface',
  'Deployment',
  'Examples',
  'Changelog',
]

const highlights = [
  {
    title: 'Provider-first design',
    description: 'Speech providers are isolated behind interfaces to keep STT/TTS engines swappable.',
  },
  {
    title: 'FastAPI + Python SDK',
    description: 'Run as an HTTP speech service or embed with the shipped Python client.',
  },
  {
    title: 'Production quality gates',
    description: 'Typed config, tests, and CI-friendly structure keep integration predictable.',
  },
]

function App() {
  return (
    <main className="min-h-screen bg-docs-bg text-docs-text">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 lg:grid-cols-[260px_minmax(0,1fr)]">
        <aside className="h-fit rounded-2xl border border-docs-border bg-docs-panel p-5 shadow-glow lg:sticky lg:top-6">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-docs-accentSoft">lavoix docs</p>
          <h1 className="mt-2 text-2xl font-semibold">Live Documentation</h1>
          <nav className="mt-6 space-y-2">
            {sections.map((section) => (
              <a
                key={section}
                href="#"
                className="block rounded-lg border border-transparent px-3 py-2 text-sm text-docs-muted transition hover:border-docs-border hover:bg-docs-panelSoft hover:text-docs-text"
              >
                {section}
              </a>
            ))}
          </nav>
          <a
            href="https://github.com/Unchained-Labs/lavoix"
            target="_blank"
            rel="noreferrer"
            className="mt-6 inline-flex rounded-lg bg-docs-accent px-3 py-2 text-sm font-semibold text-white transition hover:opacity-90"
          >
            View Repository
          </a>
        </aside>

        <section className="rounded-2xl border border-docs-border bg-docs-panel p-8 shadow-glow">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-docs-accentSoft">GitBook-style landing</p>
          <h2 className="mt-3 text-4xl font-semibold leading-tight">Speech Workflows for Production Systems</h2>
          <p className="mt-4 max-w-3xl text-base leading-7 text-docs-muted">
            lavoix provides a modern voice layer for products that need robust speech input/output.
            This docs webapp is built with Vite, Node.js, React, TypeScript, and Tailwind CSS to keep
            authoring fast while shipping a polished technical documentation UX.
          </p>

          <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-3">
            {highlights.map((item) => (
              <article key={item.title} className="rounded-xl border border-docs-border bg-docs-panelSoft p-4">
                <h3 className="text-lg font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-docs-muted">{item.description}</p>
              </article>
            ))}
          </div>

          <div className="mt-10 rounded-xl border border-docs-border bg-docs-panelSoft p-5">
            <h3 className="text-xl font-semibold">Quick commands</h3>
            <pre className="mt-3 overflow-auto rounded-lg bg-docs-bg p-4 text-sm text-docs-accentSoft">
{`npm install
npm run dev
npm run build
npm run preview`}
            </pre>
          </div>
        </section>
      </div>
    </main>
  )
}

export default App
