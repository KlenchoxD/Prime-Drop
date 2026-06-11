/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Departamentos de Colombia con sus principales ciudades/municipios.
 * Usado en el selector de dirección del checkout.
 */
export const COLOMBIA_LOCATIONS: Record<string, string[]> = {
  'Amazonas': ['Leticia', 'Puerto Nariño'],
  'Antioquia': ['Medellín', 'Bello', 'Itagüí', 'Envigado', 'Apartadó', 'Rionegro', 'Sabaneta', 'Turbo', 'La Estrella', 'Caucasia'],
  'Arauca': ['Arauca', 'Saravena', 'Tame', 'Arauquita'],
  'Atlántico': ['Barranquilla', 'Soledad', 'Malambo', 'Sabanalarga', 'Puerto Colombia'],
  'Bolívar': ['Cartagena', 'Magangué', 'Turbaco', 'El Carmen de Bolívar', 'Arjona'],
  'Boyacá': ['Tunja', 'Duitama', 'Sogamoso', 'Chiquinquirá', 'Paipa'],
  'Caldas': ['Manizales', 'La Dorada', 'Chinchiná', 'Villamaría', 'Riosucio'],
  'Caquetá': ['Florencia', 'San Vicente del Caguán', 'Puerto Rico'],
  'Casanare': ['Yopal', 'Aguazul', 'Villanueva', 'Tauramena'],
  'Cauca': ['Popayán', 'Santander de Quilichao', 'Puerto Tejada', 'Patía'],
  'Cesar': ['Valledupar', 'Aguachica', 'Bosconia', 'Codazzi'],
  'Chocó': ['Quibdó', 'Istmina', 'Condoto'],
  'Córdoba': ['Montería', 'Cereté', 'Lorica', 'Sahagún', 'Planeta Rica'],
  'Cundinamarca': ['Soacha', 'Facatativá', 'Zipaquirá', 'Chía', 'Girardot', 'Fusagasugá', 'Mosquera', 'Madrid', 'Funza', 'Cajicá'],
  'Bogotá D.C.': ['Bogotá'],
  'Guainía': ['Inírida'],
  'Guaviare': ['San José del Guaviare'],
  'Huila': ['Neiva', 'Pitalito', 'Garzón', 'La Plata'],
  'La Guajira': ['Riohacha', 'Maicao', 'Uribia', 'Fonseca'],
  'Magdalena': ['Santa Marta', 'Ciénaga', 'Fundación', 'El Banco'],
  'Meta': ['Villavicencio', 'Acacías', 'Granada', 'Puerto López'],
  'Nariño': ['Pasto', 'Ipiales', 'Tumaco', 'Túquerres'],
  'Norte de Santander': ['Cúcuta', 'Ocaña', 'Pamplona', 'Villa del Rosario', 'Los Patios'],
  'Putumayo': ['Mocoa', 'Puerto Asís', 'Orito'],
  'Quindío': ['Armenia', 'Calarcá', 'La Tebaida', 'Montenegro'],
  'Risaralda': ['Pereira', 'Dosquebradas', 'Santa Rosa de Cabal', 'La Virginia'],
  'San Andrés y Providencia': ['San Andrés', 'Providencia'],
  'Santander': ['Bucaramanga', 'Floridablanca', 'Girón', 'Piedecuesta', 'Barrancabermeja', 'San Gil'],
  'Sucre': ['Sincelejo', 'Corozal', 'Sampués', 'San Marcos'],
  'Tolima': ['Ibagué', 'Espinal', 'Melgar', 'Honda', 'Líbano'],
  'Valle del Cauca': ['Cali', 'Palmira', 'Buenaventura', 'Tuluá', 'Cartago', 'Buga', 'Jamundí', 'Yumbo'],
  'Vaupés': ['Mitú'],
  'Vichada': ['Puerto Carreño'],
};

export const COLOMBIA_DEPARTMENTS = Object.keys(COLOMBIA_LOCATIONS).sort((a, b) =>
  a.localeCompare(b, 'es')
);
