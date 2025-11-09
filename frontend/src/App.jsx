
import React, { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || ''  // same origin on Render

function Navbar() {
  return (
    <header className="bg-fitgreen text-white p-4 shadow">
      <h1 className="text-2xl font-bold">Recetario Fit</h1>
      <p className="opacity-80 text-sm">Cookies • Brownies • Muffins • PDFs</p>
    </header>
  )
}

function RecipeCard({ r }) {
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
      <h3 className="text-xl font-semibold">{r.title}</h3>
      <p className="text-sm text-gray-600 mb-2 capitalize">{r.category}</p>
      <h4 className="font-medium">Ingredientes</h4>
      <ul className="list-disc list-inside mb-2">
        {r.ingredients.map((i, idx) => <li key={idx}>{i}</li>)}
      </ul>
      <h4 className="font-medium">Pasos</h4>
      <p className="whitespace-pre-wrap">{r.steps}</p>
    </div>
  )
}

function UploadPDF({ onUploaded }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    if (!file) { setError('Elegí un PDF.'); return }
    const form = new FormData()
    form.append('title', title)
    form.append('description', description)
    form.append('file', file)
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/pdfs`, {
        method: 'POST',
        body: form
      })
      if (!res.ok) throw new Error('Error al subir el PDF.')
      await res.json()
      setTitle(''); setDescription(''); setFile(null)
      onUploaded && onUploaded()
      alert('PDF subido con éxito')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit} className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold mb-2">Subir receta en PDF</h3>
      <input
        className="w-full border rounded p-2 mb-2"
        placeholder="Título"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        className="w-full border rounded p-2 mb-2"
        placeholder="Descripción (opcional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-2"
        required
      />
      {error && <p className="text-red-600 text-sm mb-2">{error}</p>}
      <button disabled={loading} className="bg-fitgreen text-white px-4 py-2 rounded-xl">
        {loading ? 'Subiendo...' : 'Subir PDF'}
      </button>
    </form>
  )
}

function PDFsList() {
  const [pdfs, setPdfs] = useState([])
  const load = async () => {
    const res = await fetch(`${API_BASE}/api/pdfs`)
    const data = await res.json()
    setPdfs(data)
  }
  useEffect(() => { load() }, [])
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold mb-2">Recetas en PDF</h3>
      <ul className="space-y-2">
        {pdfs.map(p => (
          <li key={p.id} className="flex items-center justify-between">
            <div>
              <p className="font-medium">{p.title}</p>
              <p className="text-sm text-gray-600">{p.description}</p>
            </div>
            <a className="text-fitgreen underline" href={`${API_BASE}/api/pdfs/${p.id}`}>
              Descargar
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default function App() {
  const [recipes, setRecipes] = useState([])
  const load = async () => {
    const res = await fetch(`${API_BASE}/api/recipes`)
    const data = await res.json()
    setRecipes(data)
  }
  useEffect(() => { load() }, [])

  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="max-w-5xl mx-auto p-4 space-y-4">
        <div className="grid md:grid-cols-3 gap-4">
          {recipes.map(r => <RecipeCard key={r.id} r={r} />)}
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          <UploadPDF onUploaded={load} />
          <PDFsList />
        </div>
      </main>
      <footer className="text-center text-xs text-gray-600 py-6">
        © {new Date().getFullYear()} Recetario Fit
      </footer>
    </div>
  )
}
