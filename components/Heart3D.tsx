"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Environment, Float, MeshDistortMaterial } from "@react-three/drei";
import { useMemo, useRef } from "react";
import * as THREE from "three";

function HeartMesh() {
  const meshRef = useRef<THREE.Mesh>(null!);

  const geometry = useMemo(() => {
    const shape = new THREE.Shape();
    // Heart curve — traced in 2D, then extruded
    const x = 0, y = 0;
    shape.moveTo(x, y - 0.5);
    shape.bezierCurveTo(x, y - 0.5, x - 0.6, y - 1.2, x - 1.2, y - 0.6);
    shape.bezierCurveTo(x - 1.8, y, x - 1.6, y + 0.9, x - 0.9, y + 1.1);
    shape.bezierCurveTo(x - 0.4, y + 1.3, x - 0.1, y + 1.1, x, y + 0.7);
    shape.bezierCurveTo(x + 0.1, y + 1.1, x + 0.4, y + 1.3, x + 0.9, y + 1.1);
    shape.bezierCurveTo(x + 1.6, y + 0.9, x + 1.8, y, x + 1.2, y - 0.6);
    shape.bezierCurveTo(x + 0.6, y - 1.2, x, y - 0.5, x, y - 0.5);

    const geom = new THREE.ExtrudeGeometry(shape, {
      depth: 0.6,
      bevelEnabled: true,
      bevelSegments: 12,
      bevelSize: 0.25,
      bevelThickness: 0.25,
      curveSegments: 32,
    });
    geom.center();
    geom.rotateZ(Math.PI); // point down
    return geom;
  }, []);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    meshRef.current.rotation.y = t * 0.4;
    meshRef.current.rotation.x = Math.sin(t * 0.5) * 0.15;
    const s = 1 + Math.sin(t * 2.2) * 0.03; // heartbeat pulse
    meshRef.current.scale.set(s, s, s);
  });

  return (
    <mesh ref={meshRef} geometry={geometry} castShadow>
      <MeshDistortMaterial
        color="#ff6f9c"
        emissive="#ff2d7f"
        emissiveIntensity={0.15}
        metalness={0.15}
        roughness={0.18}
        distort={0.15}
        speed={1.6}
      />
    </mesh>
  );
}

export default function Heart3D() {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        dpr={[1, 2]}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.5} />
        <directionalLight position={[3, 3, 4]} intensity={1.2} color="#ffe4ed" />
        <directionalLight position={[-3, -2, 3]} intensity={0.5} color="#ffd0bd" />
        <pointLight position={[0, 0, 3]} intensity={0.8} color="#ff9dbc" />
        <Float speed={1.8} rotationIntensity={0.4} floatIntensity={0.8}>
          <HeartMesh />
        </Float>
        <Environment preset="sunset" background={false} />
      </Canvas>
    </div>
  );
}
