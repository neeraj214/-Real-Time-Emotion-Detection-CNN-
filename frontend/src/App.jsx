import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Camera, Smile, Shield, Activity } from 'lucide-react'

const Home = () => (
  <div className="min-h-screen p-8 max-w-6xl mx-auto">
    <header className="flex justify-between items-center mb-12">
      <div className="flex items-center gap-2">
        <div className="bg-primary p-2 rounded-lg text-white">
          <Activity size={24} />
        </div>
        <h1 className="text-xl font-bold tracking-tight">SenseAI</h1>
      </div>
      <nav className="flex gap-6 text-sm font-medium text-slate-600">
        <a href="#" className="hover:text-primary">Dashboard</a>
        <a href="#" className="hover:text-primary">History</a>
        <a href="#" className="hover:text-primary">Settings</a>
      </nav>
    </header>

    <main className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-5xl font-extrabold leading-tight mb-6">
          Real-Time Facial <span className="text-primary">Emotion</span> Recognition
        </h2>
        <p className="text-lg text-slate-600 mb-8 max-w-md">
          Detect human emotions from live webcam video using our advanced CNN model. Professional AI insights at your fingertips.
        </p>
        <div className="flex gap-4">
          <button className="btn-primary flex items-center gap-2">
            <Camera size={20} />
            Launch Camera
          </button>
          <button className="px-6 py-2.5 rounded-xl font-medium border border-slate-200 hover:bg-slate-50 transition-colors">
            Learn More
          </button>
        </div>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="glass-card p-1 aspect-video relative overflow-hidden group"
      >
        <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/10 to-blue-500/10 z-0" />
        <div className="relative z-10 w-full h-full bg-slate-50 flex items-center justify-center rounded-2xl border border-dashed border-slate-300">
          <div className="text-center">
            <div className="bg-white p-4 rounded-full shadow-soft inline-block mb-4 text-slate-400 group-hover:text-primary transition-colors">
              <Camera size={48} />
            </div>
            <p className="text-slate-500 font-medium">Camera Preview</p>
          </div>
        </div>
        
        {/* Mock UI Elements */}
        <div className="absolute top-4 right-4 flex gap-2">
          <div className="bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg flex items-center gap-2 text-xs font-bold text-slate-700 shadow-sm border border-slate-200">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            LIVE
          </div>
        </div>
      </motion.div>
    </main>

    <section className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
      {[
        { icon: Smile, title: "Emotion Detection", desc: "Detects 7 different facial expressions in real-time." },
        { icon: Shield, title: "Privacy First", desc: "Processing is done locally on your device for maximum privacy." },
        { icon: Activity, title: "High Performance", desc: "Optimized CNN model ensures smooth high FPS detection." }
      ].map((feature, i) => (
        <motion.div 
          key={i}
          whileHover={{ y: -5 }}
          className="glass-card p-6"
        >
          <div className="text-primary mb-4">
            <feature.icon size={28} />
          </div>
          <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
          <p className="text-slate-600 text-sm leading-relaxed">{feature.desc}</p>
        </motion.div>
      ))}
    </section>
  </div>
)

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  )
}

export default App
