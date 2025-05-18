import { Button } from "../components/Button";
import { Mail } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-yellow-50 text-gray-900">
      {/* Hero */}
      <section className="container mx-auto px-6 py-24 text-center">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-5xl font-extrabold mb-4 tracking-tight"
        >
          The Dopamine Company
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
          className="text-xl mb-8"
        >
          Built by Fun, Powered by AI.
        </motion.p>
        <p className="max-w-2xl mx-auto text-lg mb-12">
          We craft fun, creative products while building <span className="font-semibold">Programmer.exe</span>—an AI‑powered tool that automates product creation so anyone can bring ideas to life in minutes.
        </p>

        <Button size="lg" className="gap-2" onClick={() => window.location.href = 'mailto:yashgargofficial@gmail.com'}>
          <Mail className="w-4 h-4" />
          Join the Team
        </Button>
      </section>

      {/* Features */}
      <section className="container mx-auto px-6 py-16 grid gap-12 md:grid-cols-3">
        <FeatureCard
          title="Programmer.exe"
          desc="Turn voice or text ideas into fully‑functional apps—zero coding required."
          icon="💻"
        />
        <FeatureCard
          title="Rapid Side‑Project Lab"
          desc="We launch playful products every month to push the limits of automation."
          icon="⚡"
        />
        <FeatureCard
          title="Open by Default"
          desc="Our tools & learnings are shared with the community to ignite creativity."
          icon="🤝"
        />
      </section>
    </main>
  );
}

function FeatureCard({
  title,
  desc,
  icon,
}
) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="rounded-2xl bg-white/70 backdrop-blur p-6 shadow-lg border border-white/60"
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-2xl font-semibold mb-2">{title}</h3>
      <p className="text-sm leading-relaxed">{desc}</p>
    </motion.div>
  );
}
