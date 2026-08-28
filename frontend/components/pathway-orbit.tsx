"use client";

import { motion } from "motion/react";

export function PathwayOrbit() {
  return (
    <div className="orbit-card" aria-label="Animated diagnostic pathway visualization">
      <div className="orbit-copy">
        <span className="eyebrow">Progressive pathway</span>
        <h2>Evidence, refined over time.</h2>
        <p>
          Each stage can update priority—up or down—while keeping clinician
          judgment in control.
        </p>
      </div>
      <div className="orbital-scene">
        <motion.div className="orbit-spin wide-spin" animate={{ rotate: 360 }} transition={{ duration: 20, repeat: Infinity, ease: "linear" }}>
          <div className="orbit-ring ring-one" />
        </motion.div>
        <motion.div className="orbit-spin inner-spin" animate={{ rotate: -360 }} transition={{ duration: 13, repeat: Infinity, ease: "linear" }}>
          <div className="orbit-ring ring-two" />
        </motion.div>
        <motion.div className="core-orb" animate={{ rotate: 360, y: [0, -7, 0], scale: [1, 1.035, 1] }} transition={{ rotate: { duration: 11, repeat: Infinity, ease: "linear" }, y: { duration: 3.6, repeat: Infinity, ease: "easeInOut" }, scale: { duration: 3.6, repeat: Infinity, ease: "easeInOut" } }}>
          <span className="core-glow" />
          <i className="surface-mark mark-one" />
          <i className="surface-mark mark-two" />
          <i className="surface-mark mark-three" />
        </motion.div>
        <i className="node node-a" />
        <i className="node node-b" />
        <i className="node node-c" />
        <i className="node node-d" />
        <div className="orbit-label l-a">Screen</div>
        <div className="orbit-label l-b">Blood</div>
        <div className="orbit-label l-c">MRI</div>
        <div className="orbit-label l-d">PET</div>
      </div>
    </div>
  );
}
