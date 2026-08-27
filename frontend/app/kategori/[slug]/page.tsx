import Link from "next/link";
import { getCategories, getProducts } from "@/lib/api";
import ProductCard from "@/components/ProductCard";

export async function generateStaticParams() {
  const categories = await getCategories().catch(() => []);
  return categories.map((c) => ({ slug: c.slug }));
}

export default async function CategoryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  const [categories, products] = await Promise.all([
    getCategories().catch(() => []),
    getProducts(slug).catch(() => []),
  ]);

  const category = categories.find((c) => c.slug === slug);
  const title = category?.name ?? slug;

  return (
    <main className="px-8 py-10 max-w-6xl mx-auto">
      <nav className="text-xs text-ink/50 mb-6">
        <Link href="/" className="hover:text-burgundy">Ana Sayfa</Link>
        <span className="mx-2">/</span>
        <span className="text-ink">{title}</span>
      </nav>

      <h1 className="font-display text-3xl text-ink mb-8">{title}</h1>

      {products.length === 0 ? (
        <p className="text-ink/50 text-sm">Bu kategoride henüz ürün bulunmuyor.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      )}
    </main>
  );
}