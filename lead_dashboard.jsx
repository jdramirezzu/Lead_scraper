/**
 * Simple dashboard component to query the FastAPI backend.
 * This version avoids external UI libraries so it can run directly
 * using React from a CDN and Babel.
 */
const { useState } = React;

function LeadDashboard() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('agencia de marketing');
  const [location, setLocation] = useState('Bogotá');
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/scrape?query=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`
      );
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
      alert('Error al obtener datos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Dashboard de Leads</h1>
      <div style={{ marginBottom: '10px' }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Categoría"
        />
        <input
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Ciudad"
          style={{ marginLeft: '4px' }}
        />
        <button onClick={fetchData} disabled={loading} style={{ marginLeft: '4px' }}>
          {loading ? 'Cargando...' : 'Buscar'}
        </button>
      </div>
      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Rating</th>
            <th>Reputación</th>
            <th>Score</th>
            <th>Segmento</th>
          </tr>
        </thead>
        <tbody>
          {data.map((lead, i) => (
            <tr key={i}>
              <td>{lead.name}</td>
              <td>{lead.phone || ''}</td>
              <td>{(lead.emails || []).join(', ')}</td>
              <td>{lead.rating || ''}</td>
              <td>{lead.reputacion || ''}</td>
              <td>{lead.lead_score || ''}</td>
              <td>{lead.segmento || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
