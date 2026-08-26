import { useEffect, useState } from 'react'
import './App.css'

const fallbackImage = '/legacy/static/images/food-fallback.svg'
const foodImages = {
  'Challapunukulu': 'https://upload.wikimedia.org/wikipedia/commons/d/da/Punugulu_2.jpg',
  'Mirchi Bajji': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Stuffed_mirchi_bajji_%2816164286908%29.jpg',
  'Onion Bonda': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Bonda2.jpg',
  'Banana Bajji': 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Banana_fritters.jpg',
  'Onion Pakodi': 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG',
  'Maramaralu Mirchi': 'https://upload.wikimedia.org/wikipedia/commons/2/22/Bhel_puri_Snack.jpg',
  'Maramaralu with Kaju Mirchi': 'https://upload.wikimedia.org/wikipedia/commons/b/be/BHEL_PURI_HOMEMADE_KOTA_032.jpg',
  'Tomato Mirchi': 'https://upload.wikimedia.org/wikipedia/commons/4/46/Bengali_Dal_Pakora_RedLentilFritter.JPG',
  'Bottani Chaat': 'https://upload.wikimedia.org/wikipedia/commons/a/a1/Spicy_Chana_Dal_Chaat_-_Western_India.jpg',
  'Chanagapindi Pakodi': 'https://upload.wikimedia.org/wikipedia/commons/8/88/Pakora_%286005558506%29.jpg',
  'Egg Bajji': 'https://upload.wikimedia.org/wikipedia/commons/2/27/Anda_Pakora.JPG',
  'Bread Bajji': 'https://upload.wikimedia.org/wikipedia/commons/0/0c/Bread_Pakora_%28Bread_Pakoda%29.jpg',
  'Samosa Big': 'https://upload.wikimedia.org/wikipedia/commons/9/95/Samosa_with_sweet_chutney.jpg',
  'Family Combo': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Bonda2.jpg',
  'Friends Combo': 'https://upload.wikimedia.org/wikipedia/commons/a/a1/Spicy_Chana_Dal_Chaat_-_Western_India.jpg',
  'Bajji Lovers': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Stuffed_mirchi_bajji_%2816164286908%29.jpg',
  'Bonda Blast': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Bonda2.jpg',
  'Mega Combo': 'https://upload.wikimedia.org/wikipedia/commons/9/95/Samosa_with_sweet_chutney.jpg',
}

function imageFor(product) {
  const mappedImage = Object.entries(foodImages).find(([name]) => product.name.includes(name))?.[1]
  return mappedImage || (product.image?.startsWith('http') ? product.image : fallbackImage)
}

function App() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('')
  const [sort, setSort] = useState('newest')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/categories')
      .then((response) => response.json())
      .then(setCategories)
      .catch(() => setError('The catalog categories could not be loaded.'))
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({ sort })
    if (query.trim()) params.set('q', query.trim())
    if (category) params.set('category', category)

    setLoading(true)
    fetch(`/api/products?${params}`)
      .then((response) => {
        if (!response.ok) throw new Error('Catalog request failed')
        return response.json()
      })
      .then((items) => {
        setProducts(items)
        setError('')
      })
      .catch(() => setError('The catalog is unavailable. Start the Django API and try again.'))
      .finally(() => setLoading(false))
  }, [category, query, sort])

  return (
    <main className="storefront">
      <nav className="nav-shell">
        <a className="brand" href="/">SPICY <span>ADDA</span></a>
        <span className="nav-note">Street food, delivered with attitude</span>
        <a className="cart-link" href="http://127.0.0.1:5000/cart">Cart <span>0</span></a>
      </nav>

      <header className="hero-panel">
        <p className="eyebrow">Fresh from the adda</p>
        <h1>Big flavor.<br /><em>Zero boring.</em></h1>
        <p className="hero-copy">Craveable Indian snacks, spicy combos, and sweet little detours for every mood.</p>
      </header>

      <section className="catalog" aria-label="Product catalog">
        <div className="catalog-tools">
          <div>
            <p className="section-kicker">The menu</p>
            <h2>Pick your pleasure</h2>
          </div>
          <div className="filters">
            <input aria-label="Search products" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search the menu" />
            <select aria-label="Filter by category" value={category} onChange={(event) => setCategory(event.target.value)}>
              <option value="">All categories</option>
              {categories.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
            </select>
            <select aria-label="Sort products" value={sort} onChange={(event) => setSort(event.target.value)}>
              <option value="newest">Newest first</option>
              <option value="price_asc">Price: low to high</option>
              <option value="price_desc">Price: high to low</option>
            </select>
          </div>
        </div>

        {error && <p className="status error">{error}</p>}
        {loading ? <p className="status">Loading the good stuff...</p> : (
          <div className="product-grid">
            {products.map((product) => (
              <article className="product-card" key={product.id}>
                <div className="product-image">
                  <span className="spice-mark">{product.category || 'SPECIAL'}</span>
                  <img src={imageFor(product)} alt={product.name} onError={(event) => { event.currentTarget.src = fallbackImage }} />
                </div>
                <div className="product-info">
                  <div className="product-heading"><h3>{product.name}</h3><strong>₹{product.price}</strong></div>
                  <p>{product.description}</p>
                  <div className="product-footer"><span>{product.stock} left today</span><button type="button">Add to cart</button></div>
                </div>
              </article>
            ))}
          </div>
        )}
        {!loading && !products.length && !error && <p className="status">No dishes match that search.</p>}
      </section>
    </main>
  )
}

export default App
