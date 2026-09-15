import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-14 px-6 py-20 text-center">
      <Image
        src="/images/logo.png"
        alt="LOPSA"
        width={622}
        height={185}
        priority
        className="h-auto w-[280px] sm:w-[400px] md:w-[520px]"
      />

      <div className="flex flex-col items-center gap-8">
        <p className="text-2xl font-light uppercase tracking-[0.15em] sm:text-3xl md:text-4xl">
          <span className="text-neutral-900">Coming</span>{" "}
          <span className="text-slate-400">Soon</span>
        </p>

        <div className="flex flex-col items-center gap-2 text-base text-neutral-800 sm:text-lg">
          <p>+507 6604-4196</p>
          <a
            href="mailto:ventas@lopsa.com.pa"
            className="underline underline-offset-4 hover:text-neutral-500"
          >
            ventas@lopsa.com.pa
          </a>
          <p>Ciudad de Panamá, Panamá</p>
        </div>
      </div>
    </main>
  );
}
