import Link from "next/link";
import { searchProducts } from "@/lib/api";
import ProductCard from "@/components/ProductCard";

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const query = q ?? "";
  const products = query.trim() ? await searchProducts(query).catch(() => []) : [];

  return (
    <main className="px-8 py-10 max-w-6xl mx-auto">
      <nav className="text-xs text-ink/50 mb-6">
        <Link href="/" className="hover:text-burgundy">Ana Sayfa</Link>
        <span className="mx-2">/</span>
        <span className="text-ink">Arama</span>
      </nav>

      <h1 className="font-display text-3xl text-ink mb-2">Arama Sonuçları</h1>
      {query.trim() && (
        <p className="text-sm text-ink/60 mb-8">
          &ldquo;{query}&rdquo; için {products.length} sonuç bulundu.
        </p>
      )}

      {!query.trim() ? (
        <p className="text-ink/50 text-sm">Aramak istediğiniz ürünü yukarıdaki arama kutusuna yazın.</p>
      ) : products.length === 0 ? (
        <p className="text-ink/50 text-sm">Aramanızla eşleşen ürün bulunamadı.</p>
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