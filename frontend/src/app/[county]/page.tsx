import { redirect } from 'next/navigation';
import { Metadata } from 'next';

// Map of county slugs to proper names and search terms
const COUNTY_MAP: Record<string, { name: string; search: string }> = {
  'timisoara': { name: 'Timișoara', search: 'Timișoara' },
  'timis': { name: 'Timiș', search: 'Timiș' },
  'judetul-timis': { name: 'Județul Timiș', search: 'Timiș' },
  'bucuresti': { name: 'București', search: 'București' },
  'cluj': { name: 'Cluj', search: 'Cluj' },
  'cluj-napoca': { name: 'Cluj-Napoca', search: 'Cluj-Napoca' },
  'brasov': { name: 'Brașov', search: 'Brașov' },
  'constanta': { name: 'Constanța', search: 'Constanța' },
  'iasi': { name: 'Iași', search: 'Iași' },
  'sibiu': { name: 'Sibiu', search: 'Sibiu' },
  'oradea': { name: 'Oradea', search: 'Oradea' },
  'arad': { name: 'Arad', search: 'Arad' },
  'craiova': { name: 'Craiova', search: 'Craiova' },
  'galati': { name: 'Galați', search: 'Galați' },
  'ploiesti': { name: 'Ploiești', search: 'Ploiești' },
  'pitesti': { name: 'Pitești', search: 'Pitești' },
  'bacau': { name: 'Bacău', search: 'Bacău' },
  'targu-mures': { name: 'Târgu Mureș', search: 'Târgu Mureș' },
  'baia-mare': { name: 'Baia Mare', search: 'Baia Mare' },
  'buzau': { name: 'Buzău', search: 'Buzău' },
  'botosani': { name: 'Botoșani', search: 'Botoșani' },
  'suceava': { name: 'Suceava', search: 'Suceava' },
  'piatra-neamt': { name: 'Piatra Neamț', search: 'Piatra Neamț' },
  'deva': { name: 'Deva', search: 'Deva' },
  'hunedoara': { name: 'Hunedoara', search: 'Hunedoara' },
  'alba-iulia': { name: 'Alba Iulia', search: 'Alba Iulia' },
  'resita': { name: 'Reșița', search: 'Reșița' },
  'satu-mare': { name: 'Satu Mare', search: 'Satu Mare' },
  'ramnicu-valcea': { name: 'Râmnicu Vâlcea', search: 'Râmnicu Vâlcea' },
  'focsani': { name: 'Focșani', search: 'Focșani' },
  'bistrita': { name: 'Bistrița', search: 'Bistrița' },
  'tulcea': { name: 'Tulcea', search: 'Tulcea' },
  'calarasi': { name: 'Călărași', search: 'Călărași' },
  'giurgiu': { name: 'Giurgiu', search: 'Giurgiu' },
  'slobozia': { name: 'Slobozia', search: 'Slobozia' },
  'alexandria': { name: 'Alexandria', search: 'Alexandria' },
  'zalau': { name: 'Zalău', search: 'Zalău' },
  'drobeta-turnu-severin': { name: 'Drobeta-Turnu Severin', search: 'Drobeta-Turnu Severin' },
  'targoviste': { name: 'Târgoviște', search: 'Târgoviște' },
  'sfantu-gheorghe': { name: 'Sfântu Gheorghe', search: 'Sfântu Gheorghe' },
  'miercurea-ciuc': { name: 'Miercurea Ciuc', search: 'Miercurea Ciuc' },
  'vaslui': { name: 'Vaslui', search: 'Vaslui' },
};

interface Props {
  params: Promise<{ county: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { county } = await params;
  const location = COUNTY_MAP[county.toLowerCase()];
  
  if (!location) {
    return {
      title: 'Pagină Negăsită',
    };
  }
  
  return {
    title: `Servicii Funerare ${location.name} - Director Național`,
    description: `Găsește servicii funerare în ${location.name}. Director complet cu firme de pompe funebre, transport funerar și servicii complete de înmormântare.`,
  };
}

export default async function CountyPage({ params }: Props) {
  const { county } = await params;
  const location = COUNTY_MAP[county.toLowerCase()];
  
  if (location) {
    // Redirect to homepage with search query
    redirect(`/?search=${encodeURIComponent(location.search)}`);
  }
  
  // If not a known location, show 404
  redirect('/');
}
