import Link from "next/link";
import { getCategories, getProducts } from "@/lib/api";
import ProductCard from "@/components/ProductCard";

export default async function AllProductsPage() {
  const categories = await getCategories().catch(() => []);

  const sections = await Promise.all(
    categories.map(async (cat) => ({
      category: cat,
      products: await getProducts(cat.slug).catch(() => []),
    }))
  );

  const nonEmptySections = sections.filter((s) => s.products.length > 0);

  return (
    <main className="px-8 py-10 max-w-6xl mx-auto">
      <nav className="text-xs text-ink/50 mb-6">
        <Link href="/" className="hover:text-burgundy">Ana Sayfa</Link>
        <span className="mx-2">/</span>
        <span className="text-ink">Ürünler</span>
      </nav>

      <h1 className="font-display text-3xl text-ink mb-10">Tüm Ürünler</h1>

      {nonEmptySections.length === 0 ? (
        <p className="text-ink/50 text-sm">Henüz ürün bulunmuyor.</p>
      ) : (
        nonEmptySections.map(({ category, products }) => (
          <section key={category.id} className="mb-16">
            <div className="flex items-baseline justify-between mb-6 border-b border-ink/10 pb-3">
              <h2 className="font-display text-2xl text-ink">{category.name}</h2>
              <Link
                href={`/kategori/${category.slug}`}
                className="text-xs text-burgundy hover:underline"
              >
                Tümünü Gör
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.slice(0, 3).map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </section>
        ))
      )}
    </main>
  );
}