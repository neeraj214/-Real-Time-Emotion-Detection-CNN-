import React from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  BarChart, Bar, Cell
} from 'recharts';

const EMOTION_COLORS = {
  'Angry': '#ef4444',    // red-500
  'Disgust': '#9333ea',  // purple-600
  'Fear': '#f97316',     // orange-500
  'Happy': '#22c55e',    // green-500
  'Sad': '#2563eb',      // blue-600
  'Surprise': '#eab308', // yellow-500
  'Neutral': '#94a3b8'   // slate-400
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 rounded-lg shadow-xl border border-slate-100 flex flex-col gap-1">
        <p className="font-medium text-slate-800 text-sm mb-1">{`Time: ${label}`}</p>
        {[...payload]
          .sort((a, b) => b.value - a.value)
          .slice(0, 3) // Only show top 3 for clarity
          .map((entry, index) => (
            <p key={index} className="text-sm flex items-center justify-between gap-4">
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></span>
                {entry.name}
              </span>
              <span className="font-bold">{(entry.value * 100).toFixed(0)}%</span>
            </p>
        ))}
      </div>
    );
  }
  return null;
};

const AnalyticsDashboard = ({ history, smoothedDistribution }) => {
  
  // Format data for the bar chart
  const barData = smoothedDistribution
    .map(dist => ({
      name: dist.name,
      confidence: dist.confidence * 100, // convert to percentage
      fill: EMOTION_COLORS[dist.name] || '#94a3b8'
    }))
    // Sort so highest is at the top/first
    .sort((a, b) => b.confidence - a.confidence);

  return (
    <div className="flex flex-col gap-6 w-full mt-6">
      
      {/* Emotion History Line Chart */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 w-full overflow-hidden">
        <div className="mb-4">
          <h3 className="text-lg font-bold text-slate-800">Emotion Timeline</h3>
          <p className="text-sm text-slate-500">Real-time confidence distribution over the last 15 frames</p>
        </div>
        
        <div className="h-64 w-full">
          {history.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={history}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis 
                  dataKey="time" 
                  tick={{ fontSize: 12, fill: '#64748b' }}
                  tickMargin={10}
                  axisLine={{ stroke: '#cbd5e1' }}
                  tickLine={false}
                />
                <YAxis 
                  domain={[0, 1]} 
                  tickFormatter={(val) => `${val * 100}%`}
                  tick={{ fontSize: 12, fill: '#64748b' }}
                  axisLine={false}
                  tickLine={false}
                  tickCount={5}
                />
                <Tooltip content={<CustomTooltip />} />
                
                {Object.keys(EMOTION_COLORS).map(emotion => (
                  <Line 
                    key={emotion}
                    type="monotone" 
                    dataKey={emotion} 
                    stroke={EMOTION_COLORS[emotion]} 
                    strokeWidth={3}
                    dot={false}
                    activeDot={{ r: 6, strokeWidth: 0 }}
                    isAnimationActive={false} // Disable animation for real-time performance
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full w-full flex items-center justify-center bg-slate-50 rounded-xl border border-dashed border-slate-300">
              <p className="text-slate-400 font-medium text-sm">Waiting for camera data...</p>
            </div>
          )}
        </div>
      </div>

      {/* Current Distribution Bar Chart */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 w-full">
        <div className="mb-4">
          <h3 className="text-lg font-bold text-slate-800">Current Distribution</h3>
          <p className="text-sm text-slate-500">Smoothed probability across all emotions</p>
        </div>
        
        <div className="h-48 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={barData}
              layout="vertical"
              margin={{ top: 0, right: 30, left: 20, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
              <XAxis 
                type="number" 
                domain={[0, 100]} 
                hide 
              />
              <YAxis 
                dataKey="name" 
                type="category" 
                axisLine={false} 
                tickLine={false}
                tick={{ fontSize: 13, fill: '#334155', fontWeight: 500 }}
                width={80}
              />
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)}%`, 'Confidence']}
                cursor={{ fill: 'transparent' }}
                contentStyle={{ borderRadius: '0.5rem', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Bar 
                dataKey="confidence" 
                radius={[0, 4, 4, 0]}
                barSize={20}
                isAnimationActive={false}
              >
                {barData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
