import ProductDetailClient from "@/components/ProductDetailClient";
import { getProducts } from "@/lib/api";

export async function generateStaticParams() {
  const products = await getProducts().catch(() => []);
  const slugs = products.map((p) => ({ slug: p.slug }));
  if (!slugs.some((s) => s.slug === "placeholder")) {
    slugs.push({ slug: "placeholder" });
  }
  return slugs;
}

export default function ProductDetailPage() {
  return <ProductDetailClient />;
}
