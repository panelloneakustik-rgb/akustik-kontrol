"use client";

import { useEffect, useState } from "react";
import Hero from "./Hero";
import BestSellers from "./BestSellers";
import { getBestsellers, getHeroSlides, type HeroSlide, type Product } from "@/lib/api";

export default function HomeClient() {
  const [bestsellers, setBestsellers] = useState<Product[]>([]);
  const [heroSlides, setHeroSlides] = useState<HeroSlide[]>([]);

  useEffect(() => {
    getBestsellers()
      .then(setBestsellers)
      .catch(() => {});
    getHeroSlides()
      .then(setHeroSlides)
      .catch(() => {});
  }, []);

  return (
    <>
      <Hero slides={heroSlides} />
      <BestSellers products={bestsellers} />
    </>
  );
}
