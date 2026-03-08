import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, Brain, Cpu, ArrowRight, Shield, Zap, Smile, Activity } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';

const FloatingIcon = ({ icon: Icon, delay, className }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ 
      opacity: [0.4, 0.8, 0.4],
      y: [0, -20, 0],
      rotate: [0, 10, -10, 0]
    }}
    transition={{ 
      duration: 5, 
      repeat: Infinity, 
      delay: delay,
      ease: "easeInOut"
    }}
    className={`absolute p-4 bg-white/40 backdrop-blur-sm rounded-2xl border border-white/20 shadow-soft ${className}`}
  >
    <Icon className="text-primary/60" size={32} />
  </motion.div>
);

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-[calc(100vh-64px)] flex flex-col items-center justify-center overflow-hidden bg-slate-50">
      {/* Background Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/30 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-200/30 blur-[120px] rounded-full" />
      </div>

      {/* Floating Elements */}
      <FloatingIcon icon={Camera} delay={0} className="top-20 left-[15%] hidden lg:block" />
      <FloatingIcon icon={Brain} delay={2} className="bottom-40 left-[10%] hidden lg:block" />
      <FloatingIcon icon={Cpu} delay={1} className="top-40 right-[15%] hidden lg:block" />
      <FloatingIcon icon={Smile} delay={3} className="bottom-20 right-[10%] hidden lg:block" />

      <main className="relative z-10 max-w-4xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100 text-primary text-xs font-bold mb-6 tracking-wide uppercase">
            <Zap size={14} fill="currentColor" />
            AI-Powered Recognition
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight mb-6 leading-[1.1]">
            Real-Time Facial <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-600">
              Emotion Recognition
            </span>
          </h1>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed"
          >
            Detect human emotions instantly using our advanced AI-powered computer vision system. Experience seamless real-time analysis through your webcam.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <button 
              onClick={() => navigate('/detect')}
              className="group btn-primary px-8 py-4 text-lg flex items-center gap-2 shadow-lg shadow-indigo-200"
            >
              Start Detection
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="px-8 py-4 text-lg font-medium text-slate-600 hover:text-slate-900 transition-colors flex items-center gap-2">
              Learn More
            </button>
          </motion.div>
        </motion.div>
      </main>

      {/* Feature Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 w-full">
        <div className="text-center mb-16">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-3xl md:text-4xl font-bold text-slate-900 mb-4"
          >
            Powerful Features for Modern AI
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-slate-600 max-w-2xl mx-auto"
          >
            Our emotion detection system is built with cutting-edge technology to provide fast, accurate, and private results.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard 
            icon={Zap}
            title="Real-Time Detection"
            description="Process video streams instantly with sub-millisecond latency for live emotion tracking."
            accentColor="bg-amber-500"
          />
          <FeatureCard 
            icon={Brain}
            title="AI-Powered CNN Model"
            description="Leveraging deep convolutional neural networks trained on thousands of facial expressions."
            accentColor="bg-indigo-600"
          />
          <FeatureCard 
            icon={Activity}
            title="Optimized Performance"
            description="Smooth high-FPS detection optimized for both desktop and mobile processor architectures."
            accentColor="bg-blue-500"
          />
        </div>
      </section>
    </div>
  );
};

export default Home;
