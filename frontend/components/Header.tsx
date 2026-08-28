"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Search, Heart, User, ShoppingBag, X } from "lucide-react";
import Image from "next/image";
import { useCart } from "@/components/CartProvider";
import { useAuth } from "@/components/AuthProvider";
import { useFavorites } from "@/components/FavoritesProvider";

const NAV = [
  { label: "ÜRÜNLER", href: "/urunler" },
  { label: "AKSESUAR", href: "/kategori/aksesuar" },
  { label: "MAĞAZALARIMIZ", href: "/magazalarimiz" },
  { label: "HAKKIMIZDA", href: "/hakkimizda" },
];

export default function Header() {
  const { user } = useAuth();
  const { productIds } = useFavorites();
  const { itemCount } = useCart();
  const router = useRouter();
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    router.push(`/arama?q=${encodeURIComponent(query.trim())}`);
    setSearchOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 flex items-center justify-between px-8 py-7 bg-cream border-b border-ink/10">
      <Link href="/" className="flex items-center">
        <Image src="/logo.png" alt="Akustik Kontrol" width={500} height={73} className="h-11 w-auto" />
      </Link>

      <nav className="hidden md:flex gap-8 text-sm font-medium tracking-wide text-ink">
        {NAV.map((item) => (
          <Link key={item.href} href={item.href} className="hover:text-burgundy transition-colors">
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="flex items-center gap-4 text-ink">
        <div className="relative flex items-center">
          {searchOpen && (
            <form onSubmit={handleSearchSubmit} className="absolute right-8 top-1/2 -translate-y-1/2 flex items-center">
              <input
                autoFocus
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ürün ara..."
                className="w-48 md:w-64 border border-ink/20 bg-white px-3 py-2 text-sm text-ink focus:outline-none focus:border-burgundy"
              />
            </form>
          )}
          <button
            aria-label={searchOpen ? "Aramayı kapat" : "Ara"}
            onClick={() => setSearchOpen((v) => !v)}
            className="relative z-10 hover:text-burgundy transition-colors"
          >
            {searchOpen ? <X size={20} /> : <Search size={20} />}
          </button>
        </div>

        <Link href="/favoriler" aria-label="Favoriler" className="relative hover:text-burgundy transition-colors">
          <Heart size={20} />
          {mounted && productIds.size > 0 && (
            <span className="absolute -top-2 -right-2 bg-gold text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
              {productIds.size}
            </span>
          )}
        </Link>

        <Link href={mounted && user ? "/hesabim" : "/giris"} aria-label="Hesabım" className="hover:text-burgundy transition-colors">
          <User size={20} />
        </Link>

        <Link href="/sepet" aria-label="Sepetim" className="relative hover:text-burgundy transition-colors">
          <ShoppingBag size={20} />
          {mounted && itemCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-gold text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
              {itemCount}
            </span>
          )}
        </Link>
      </div>
    </header>
  );
}