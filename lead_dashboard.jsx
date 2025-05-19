import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell } from '@/components/ui/table';

export default function LeadDashboard() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('agencia de marketing');
  const [location, setLocation] = useState('Bogotá');
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/scrape?query=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard de Leads</h1>

      <div className="mb-4 flex gap-2">
        <Input value={query} onChange={e => setQuery(e.target.value)} placeholder="Categoría" />
        <Input value={location} onChange={e => setLocation(e.target.value)} placeholder="Ciudad" />
        <Button onClick={fetchData} disabled={loading}>{loading ? 'Cargando...' : 'Buscar'}</Button>
      </div>

      <Card>
        <CardContent>
          <Table>
            <TableHead>
              <TableRow>
                <TableHeaderCell>Nombre</TableHeaderCell>
                <TableHeaderCell>Teléfono</TableHeaderCell>
                <TableHeaderCell>Email</TableHeaderCell>
                <TableHeaderCell>Rating</TableHeaderCell>
                <TableHeaderCell>Reputación</TableHeaderCell>
                <TableHeaderCell>Score</TableHeaderCell>
                <TableHeaderCell>Segmento</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((lead, i) => (
                <TableRow key={i}>
                  <TableCell>{lead.name}</TableCell>
                  <TableCell>{lead.phone}</TableCell>
                  <TableCell>{lead.emails?.join(', ')}</TableCell>
                  <TableCell>{lead.rating}</TableCell>
                  <TableCell>{lead.reputacion}</TableCell>
                  <TableCell>{lead.lead_score}</TableCell>
                  <TableCell>{lead.segmento}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
