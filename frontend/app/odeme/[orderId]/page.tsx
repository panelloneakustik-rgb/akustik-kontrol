"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { initializePayment } from "@/lib/orders";

export default function PaymentPage() {
  const params = useParams<{ orderId: string }>();
  const orderId = Number(params.orderId);
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!orderId) return;

    initializePayment(orderId)
      .then(({ checkout_form_content }) => {
        if (!containerRef.current) return;
        containerRef.current.innerHTML = checkout_form_content;

        const scripts = containerRef.current.querySelectorAll("script");
        scripts.forEach((oldScript) => {
          const newScript = document.createElement("script");
          Array.from(oldScript.attributes).forEach((attr) =>
            newScript.setAttribute(attr.name, attr.value)
          );
          newScript.textContent = oldScript.textContent;
          oldScript.parentNode?.replaceChild(newScript, oldScript);
        });
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Ödeme başlatılamadı."))
      .finally(() => setLoading(false));
  }, [orderId]);

  return (
    <main className="px-8 py-16 max-w-lg mx-auto">
      <h1 className="font-display text-3xl text-ink mb-2 text-center">Ödeme</h1>
      {orderId ? (
        <p className="text-center text-ink/50 text-sm mb-8">Sipariş kodu: AK-{orderId}</p>
      ) : null}

      {loading && <p className="text-center text-ink/50 text-sm">Ödeme formu hazırlanıyor...</p>}
      {error && <p className="text-center text-burgundy text-sm">{error}</p>}

      <div ref={containerRef} id="iyzipay-checkout-form" className="responsive" />
    </main>
  );
}