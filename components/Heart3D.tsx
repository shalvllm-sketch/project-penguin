"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Environment, Float } from "@react-three/drei";
import { useMemo, useRef } from "react";
import * as THREE from "three";

function HeartMesh() {
  const meshRef = useRef<THREE.Mesh>(null!);

  const geometry = useMemo(() => {
    const shape = new THREE.Shape();
    const x = 0, y = 0;
    shape.moveTo(x, y - 0.5);
    shape.bezierCurveTo(x, y - 0.5, x - 0.6, y - 1.2, x - 1.2, y - 0.6);
    shape.bezierCurveTo(x - 1.8, y, x - 1.6, y + 0.9, x - 0.9, y + 1.1);
    shape.bezierCurveTo(x - 0.4, y + 1.3, x - 0.1, y + 1.1, x, y + 0.7);
    shape.bezierCurveTo(x + 0.1, y + 1.1, x + 0.4, y + 1.3, x + 0.9, y + 1.1);
    shape.bezierCurveTo(x + 1.6, y + 0.9, x + 1.8, y, x + 1.2, y - 0.6);
    shape.bezierCurveTo(x + 0.6, y - 1.2, x, y - 0.5, x, y - 0.5);

    const geom = new THREE.ExtrudeGeometry(shape, {
      depth: 0.55,
      bevelEnabled: true,
      bevelSegments: 16,
      bevelSize: 0.28,
      bevelThickness: 0.28,
      curveSegments: 40,
    });
    geom.center();
    geom.rotateZ(Math.PI);
    return geom;
  }, []);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    meshRef.current.rotation.y = t * 0.18;
    meshRef.current.rotation.x = Math.sin(t * 0.3) * 0.08;
    const s = 1 + Math.sin(t * 1.4) * 0.012; // barely-there heartbeat
    meshRef.current.scale.set(s, s, s);
  });

  return (
    <mesh ref={meshRef} geometry={geometry} castShadow>
      <meshPhysicalMaterial
        color="#7a3f56"
        emissive="#3b1a26"
        emissiveIntensity={0.08}
        metalness={0.05}
        roughness={0.55}
        clearcoat={0.35}
        clearcoatRoughness={0.5}
        sheen={1}
        sheenColor="#c88a9c"
        sheenRoughness={0.6}
      />
    </mesh>
  );
}

export default function Heart3D() {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 42 }}
        dpr={[1, 2]}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.35} />
        <directionalLight position={[3, 4, 5]} intensity={1.4} color="#fff2e1" />
        <directionalLight position={[-4, -1, 2]} intensity={0.4} color="#c88a9c" />
        <pointLight position={[0, -3, 3]} intensity={0.35} color="#a85f76" />
        <Float speed={0.9} rotationIntensity={0.2} floatIntensity={0.4}>
          <HeartMesh />
        </Float>
        <Environment preset="apartment" background={false} />
      </Canvas>
    </div>
  );
}
