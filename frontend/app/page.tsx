import Hero from "@/components/Hero";
import BestSellers from "@/components/BestSellers";
import { getBestsellers, getHeroSlides } from "@/lib/api";

export default async function HomePage() {
  let bestsellers: Awaited<ReturnType<typeof getBestsellers>> = [];
  let heroSlides: Awaited<ReturnType<typeof getHeroSlides>> = [];
  try {
    bestsellers = await getBestsellers();
  } catch {
    // Backend not reachable -- BestSellers shows its own empty state.
  }
  try {
    heroSlides = await getHeroSlides();
  } catch {
    // Backend not reachable -- Hero renders nothing rather than crash.
  }

  return (
    <>
      <Hero slides={heroSlides} />
      <BestSellers products={bestsellers} />
    </>
  );
}