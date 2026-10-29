import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

/* ==========================================================================
   1. SISTEMA DE AUDIO RETRO (Web Audio API Sintetizado)
   ========================================================================== */
class RetroAudio {
  constructor() {
    this.ctx = null;
    this.enabled = false;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
      this.enabled = true;
    } else if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Sonido de inicio N64 (Escena 1 -> Escena 2)
  playStartChime() {
    if (!this.enabled || !this.ctx) return;
    const t = this.ctx.currentTime;
    const chord = [523.25, 659.25, 783.99, 1046.50];
    chord.forEach((freq, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const start = t + i * 0.08;
      const duration = 0.35;

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, start);

      gain.gain.setValueAtTime(0.2, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(start);
      osc.stop(start + duration);
    });
  }

  // Sonido icónico "It's-a me!" / Entrada al castillo (Escena 2 -> Escena 3)
  playLetsGoChime() {
    if (!this.enabled || !this.ctx) return;
    const t = this.ctx.currentTime;
    // Dos tonos rápidos y fanfare ascendente
    const melody = [
      { f: 659.25, d: 0.12, offset: 0 },
      { f: 783.99, d: 0.12, offset: 0.12 },
      { f: 1046.50, d: 0.30, offset: 0.24 }
    ];
    melody.forEach((note) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const start = t + note.offset;

      osc.type = 'square';
      osc.frequency.setValueAtTime(note.f, start);

      gain.gain.setValueAtTime(0.18, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + note.d);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(start);
      osc.stop(start + note.d);
    });
  }

  playJump() {
    if (!this.enabled || !this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const t = this.ctx.currentTime;

    osc.type = 'square';
    osc.frequency.setValueAtTime(140, t);
    osc.frequency.exponentialRampToValueAtTime(320, t + 0.15);

    gain.gain.setValueAtTime(0.12, t);
    gain.gain.exponentialRampToValueAtTime(0.01, t + 0.15);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(t);
    osc.stop(t + 0.15);
  }

  playCoin() {
    if (!this.enabled || !this.ctx) return;
    const t = this.ctx.currentTime;
    
    const osc1 = this.ctx.createOscillator();
    const gain1 = this.ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(987.77, t);
    gain1.gain.setValueAtTime(0.15, t);
    gain1.gain.exponentialRampToValueAtTime(0.01, t + 0.08);
    osc1.connect(gain1);
    gain1.connect(this.ctx.destination);
    osc1.start(t);
    osc1.stop(t + 0.08);

    const osc2 = this.ctx.createOscillator();
    const gain2 = this.ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(1318.51, t + 0.08);
    gain2.gain.setValueAtTime(0.18, t + 0.08);
    gain2.gain.exponentialRampToValueAtTime(0.01, t + 0.3);
    osc2.connect(gain2);
    gain2.connect(this.ctx.destination);
    osc2.start(t + 0.08);
    osc2.stop(t + 0.3);
  }

  playVictory() {
    if (!this.enabled || !this.ctx) return;
    const t = this.ctx.currentTime;
    const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51];
    notes.forEach((freq, index) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const start = t + index * 0.13;
      const dur = index === 4 ? 0.7 : 0.12;

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, start);

      gain.gain.setValueAtTime(0.2, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + dur);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(start);
      osc.stop(start + dur);
    });
  }
}

const audio = new RetroAudio();

/* ==========================================================================
   2. CONFIGURACIÓN PRINCIPAL DE THREE.JS
   ========================================================================== */
const container = document.getElementById('game-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x7dd3fc);
scene.fog = new THREE.FogExp2(0x7dd3fc, 0.012);

const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 500);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

// Iluminación para Escena de Juego
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x44aa44, 0.7);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xfff7ed, 1.25);
dirLight.position.set(30, 60, 40);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.bias = -0.0005;
scene.add(dirLight);

/* ==========================================================================
   3. ESCENA 2: CABEZA 3D GIGANTE DE BUKELO (MARIO 64 HEAD HOMAGE)
   ========================================================================== */
const headSceneGroup = new THREE.Group();
headSceneGroup.position.set(0, 100, 0); // Ubicada en un espacio aislado de Three.js
scene.add(headSceneGroup);

// Iluminación de estudio estilo Mario 64 para la cabeza
const headLightFront = new THREE.DirectionalLight(0xffffff, 1.8);
headLightFront.position.set(0, 102, 6);
scene.add(headLightFront);

const headLightFill = new THREE.PointLight(0x93c5fd, 2.5, 20);
headLightFill.position.set(-4, 101, 3);
scene.add(headLightFill);

let bukeleHeadMesh = null;
const gltfLoader = new GLTFLoader();

// Carga de bukele_head.glb desde Blender
gltfLoader.load(
  'assets/models/bukele_head.glb',
  (gltf) => {
    bukeleHeadMesh = gltf.scene;
    bukeleHeadMesh.scale.set(1.4, 1.4, 1.4);
    bukeleHeadMesh.position.set(0, 0, 0);
    bukeleHeadMesh.rotation.y = Math.PI; // Mirando hacia la cámara
    headSceneGroup.add(bukeleHeadMesh);
    console.log('[GLTF] Cabeza oficial bukele_head.glb cargada.');
  },
  undefined,
  (err) => console.warn('[GLTF Error] bukele_head.glb:', err)
);

/* ==========================================================================
   4. NAYIB BUKELE: MODELO 3D DE CUERPO ENTERO PARA GAMEPLAY
   ========================================================================== */
function createBukeleCharacter() {
  const group = new THREE.Group();

  const shadowGeom = new THREE.CircleGeometry(0.65, 24);
  const shadowMat = new THREE.MeshBasicMaterial({
    color: 0x000000,
    transparent: true,
    opacity: 0.35,
    depthWrite: false
  });
  const dropShadow = new THREE.Mesh(shadowGeom, shadowMat);
  dropShadow.rotation.x = -Math.PI / 2;
  dropShadow.position.y = 0.02;
  scene.add(dropShadow);

  group.userData = {
    dropShadow,
    blenderModel: null
  };

  // Carga de bukele.glb (modelo ceremonial completo de Blender)
  gltfLoader.load(
    'assets/models/bukele.glb',
    (gltf) => {
      const bukeleMesh = gltf.scene;
      bukeleMesh.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });
      group.add(bukeleMesh);
      group.userData.blenderModel = bukeleMesh;
      console.log('[GLTF] Modelo ceremonial bukele.glb activo.');
    },
    undefined,
    (err) => console.warn('[GLTF Fallback] bukele.glb:', err)
  );

  return group;
}

const player = createBukeleCharacter();
scene.add(player);
player.position.set(0, 0, 10);

/* ==========================================================================
   5. ESCENARIO 3D (Pradera, Colina, Plataformas y Nubes)
   ========================================================================== */
const colliders = [];

// Suelo Principal
const groundGeom = new THREE.CylinderGeometry(45, 48, 4, 48);
const groundMat = new THREE.MeshLambertMaterial({ color: 0x4ade80 });
const ground = new THREE.Mesh(groundGeom, groundMat);
ground.position.y = -2;
ground.receiveShadow = true;
scene.add(ground);
colliders.push({ type: 'ground', y: 0, radius: 45 });

// Colina
function createHill() {
  const hillGroup = new THREE.Group();
  const hillMat = new THREE.MeshLambertMaterial({ color: 0x22c55e });

  const tiers = [
    { radiusTop: 18, radiusBottom: 22, height: 3.5, y: 1.75 },
    { radiusTop: 12, radiusBottom: 16, height: 3.5, y: 5.25 },
    { radiusTop: 6, radiusBottom: 9, height: 3.5, y: 8.75 }
  ];

  tiers.forEach((t) => {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(t.radiusTop, t.radiusBottom, t.height, 28), hillMat);
    mesh.position.set(0, t.y, -16);
    mesh.receiveShadow = true;
    mesh.castShadow = true;
    hillGroup.add(mesh);

    colliders.push({
      type: 'box',
      minX: -t.radiusTop,
      maxX: t.radiusTop,
      minZ: -16 - t.radiusTop,
      maxZ: -16 + t.radiusTop,
      topY: t.y + t.height / 2
    });
  });

  scene.add(hillGroup);
}
createHill();

// Plataformas
const platformMat = new THREE.MeshLambertMaterial({ color: 0xfbbf24 });
const brickBorderMat = new THREE.MeshLambertMaterial({ color: 0xd97706 });

function addPlatform(x, y, z, w, d) {
  const platGroup = new THREE.Group();
  const plat = new THREE.Mesh(new THREE.BoxGeometry(w, 0.6, d), platformMat);
  plat.castShadow = true;
  plat.receiveShadow = true;
  platGroup.add(plat);

  const border = new THREE.Mesh(new THREE.BoxGeometry(w + 0.1, 0.2, d + 0.1), brickBorderMat);
  border.position.y = -0.2;
  platGroup.add(border);

  platGroup.position.set(x, y, z);
  scene.add(platGroup);

  colliders.push({
    type: 'box',
    minX: x - w / 2,
    maxX: x + w / 2,
    minZ: z - d / 2,
    maxZ: z + d / 2,
    topY: y + 0.3
  });
}

addPlatform(0, 1.8, -4, 4, 3);
addPlatform(8, 3.8, -8, 3.5, 3.5);
addPlatform(-8, 5.8, -12, 3.5, 3.5);
addPlatform(0, 7.8, -14, 3.5, 3);

// Árboles
function addTree(x, z) {
  const tree = new THREE.Group();
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.5, 2.2, 8), new THREE.MeshLambertMaterial({ color: 0x78350f }));
  trunk.position.y = 1.1;
  trunk.castShadow = true;
  tree.add(trunk);

  const foliageMat = new THREE.MeshLambertMaterial({ color: 0x15803d });
  const f1 = new THREE.Mesh(new THREE.ConeGeometry(2.2, 2.5, 8), foliageMat);
  f1.position.y = 2.8;
  f1.castShadow = true;
  tree.add(f1);

  const f2 = new THREE.Mesh(new THREE.ConeGeometry(1.6, 2.0, 8), foliageMat);
  f2.position.y = 4.0;
  f2.castShadow = true;
  tree.add(f2);

  tree.position.set(x, 0, z);
  scene.add(tree);
}

addTree(-16, 5);
addTree(18, 8);
addTree(-14, -8);
addTree(17, -10);
addTree(-20, 18);
addTree(22, 16);

// Nubes
const clouds = [];
function addCloud(x, y, z) {
  const cloud = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 });
  const count = 4 + Math.floor(Math.random() * 3);
  for (let i = 0; i < count; i++) {
    const r = 2.0 + Math.random() * 1.5;
    const puff = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 1), mat);
    puff.position.set((i - count / 2) * 2, Math.random() * 0.8, (Math.random() - 0.5) * 1.5);
    cloud.add(puff);
  }
  cloud.position.set(x, y, z);
  scene.add(cloud);
  clouds.push(cloud);
}

addCloud(-25, 22, -20);
addCloud(30, 26, -10);
addCloud(-10, 24, 25);
addCloud(15, 20, 30);

/* ==========================================================================
   6. COLECCIONABLES (Bitcoins y La Estrella)
   ========================================================================== */
const coins = [];
let collectedCoins = 0;

function createBitcoin(x, y, z) {
  const coinGroup = new THREE.Group();
  const discGeom = new THREE.CylinderGeometry(0.75, 0.75, 0.15, 24);
  const discMat = new THREE.MeshStandardMaterial({
    color: 0xf59e0b,
    metalness: 0.85,
    roughness: 0.25,
    emissive: 0x78350f
  });
  const disc = new THREE.Mesh(discGeom, discMat);
  disc.rotation.x = Math.PI / 2;
  disc.castShadow = true;
  coinGroup.add(disc);

  const rimGeom = new THREE.TorusGeometry(0.75, 0.06, 12, 32);
  const rim = new THREE.Mesh(rimGeom, discMat);
  coinGroup.add(rim);

  coinGroup.position.set(x, y, z);
  coinGroup.userData = { baseY: y, active: true };
  scene.add(coinGroup);
  coins.push(coinGroup);
}

createBitcoin(0, 1.2, 5);
createBitcoin(0, 3.2, -4);
createBitcoin(8, 5.2, -8);
createBitcoin(-8, 7.2, -12);
createBitcoin(0, 9.2, -14);

function createStar() {
  const starGroup = new THREE.Group();
  const shape = new THREE.Shape();
  const outerR = 1.2;
  const innerR = 0.5;
  const points = 5;

  for (let i = 0; i < points * 2; i++) {
    const r = i % 2 === 0 ? outerR : innerR;
    const a = (i / (points * 2)) * Math.PI * 2 - Math.PI / 2;
    const x = Math.cos(a) * r;
    const y = Math.sin(a) * r;
    if (i === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  }
  shape.closePath();

  const extrudeSettings = { depth: 0.35, bevelEnabled: true, bevelSegments: 3, steps: 1, bevelSize: 0.1, bevelThickness: 0.1 };
  const starGeom = new THREE.ExtrudeGeometry(shape, extrudeSettings);
  starGeom.center();

  const starMat = new THREE.MeshStandardMaterial({
    color: 0xfacc15,
    metalness: 0.6,
    roughness: 0.2,
    emissive: 0xeab308,
    emissiveIntensity: 0.6
  });

  const starMesh = new THREE.Mesh(starGeom, starMat);
  starMesh.castShadow = true;
  starGroup.add(starMesh);

  const starLight = new THREE.PointLight(0xfef08a, 2.0, 15);
  starGroup.add(starLight);

  starGroup.position.set(0, 12.0, -16);
  starGroup.userData = { baseY: 12.0, active: true };
  scene.add(starGroup);

  return starGroup;
}

const star = createStar();

/* ==========================================================================
   7. MÁQUINA DE ESTADOS DE ESCENAS
   ========================================================================== */
const SCENE_1_TITLE = 1;
const SCENE_2_HEAD = 2;
const SCENE_3_GAMEPLAY = 3;
const SCENE_VICTORY = 4;

let currentScene = SCENE_1_TITLE;

const scene1Title = document.getElementById('scene-1-title');
const btnScene1Start = document.getElementById('btn-scene-1-start');

const scene2Head = document.getElementById('scene-2-head');
const btnScene2Start = document.getElementById('btn-scene-2-start');

const hud = document.getElementById('hud');
const controlsHint = document.getElementById('controls-hint');
const victoryModal = document.getElementById('victory-modal');
const btnRestart = document.getElementById('btn-restart');
const coinCountEl = document.getElementById('coin-count');
const finalCoinsEl = document.getElementById('final-coins');

// Transición: Escena 1 -> Escena 2 (Cabeza 3D)
function goToScene2() {
  if (currentScene !== SCENE_1_TITLE) return;
  audio.init();
  audio.playStartChime();

  scene1Title.classList.remove('active');
  setTimeout(() => {
    scene2Head.classList.remove('hidden');
    currentScene = SCENE_2_HEAD;
  }, 400);
}

// Transición: Escena 2 -> Escena 3 (Gameplay)
function goToScene3() {
  if (currentScene !== SCENE_2_HEAD) return;
  audio.init();
  audio.playLetsGoChime();

  scene2Head.classList.add('hidden');
  hud.classList.remove('hidden');
  controlsHint.classList.remove('hidden');

  currentScene = SCENE_3_GAMEPLAY;
}

btnScene1Start.addEventListener('click', goToScene2);
btnScene2Start.addEventListener('click', goToScene3);
btnRestart.addEventListener('click', () => location.reload());

/* ==========================================================================
   8. CONTROLES Y SEGUIMIENTO DEL CURSOR (HEAD TRACKING)
   ========================================================================== */
const keys = {};
let isGrounded = false;
let velocityY = 0;
const GRAVITY = -34;
const JUMP_FORCE = 13.5;
const SPEED = 9.0;

let cameraAngle = 0;
let isDragging = false;
let previousMouseX = 0;

let mouseNormalizedX = 0;
let mouseNormalizedY = 0;

window.addEventListener('keydown', (e) => {
  keys[e.code] = true;
  audio.init();

  if (currentScene === SCENE_1_TITLE && (e.code === 'Space' || e.code === 'Enter')) {
    goToScene2();
    return;
  }
  if (currentScene === SCENE_2_HEAD && (e.code === 'Space' || e.code === 'Enter')) {
    goToScene3();
    return;
  }

  if (e.code === 'KeyQ') cameraAngle += 0.08;
  if (e.code === 'KeyE') cameraAngle -= 0.08;
});

window.addEventListener('keyup', (e) => {
  keys[e.code] = false;
});

window.addEventListener('mousemove', (e) => {
  mouseNormalizedX = (e.clientX / window.innerWidth - 0.5) * 2;
  mouseNormalizedY = (e.clientY / window.innerHeight - 0.5) * 2;

  if (isDragging && currentScene === SCENE_3_GAMEPLAY) {
    const deltaX = e.clientX - previousMouseX;
    cameraAngle -= deltaX * 0.005;
    previousMouseX = e.clientX;
  }
});

window.addEventListener('mousedown', (e) => {
  if (e.button === 0) {
    isDragging = true;
    previousMouseX = e.clientX;
    audio.init();

    if (currentScene === SCENE_1_TITLE) {
      goToScene2();
    } else if (currentScene === SCENE_2_HEAD) {
      goToScene3();
    }
  }
});

window.addEventListener('mouseup', () => {
  isDragging = false;
});

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

/* ==========================================================================
   9. BUCLE PRINCIPAL DE ANIMACIÓN Y FÍSICAS
   ========================================================================== */
const clock = new THREE.Clock();
let walkCycle = 0;

function updatePhysics(delta) {
  if (currentScene !== SCENE_3_GAMEPLAY) return;

  let moveX = 0;
  let moveZ = 0;

  if (keys['KeyW'] || keys['ArrowUp']) moveZ -= 1;
  if (keys['KeyS'] || keys['ArrowDown']) moveZ += 1;
  if (keys['KeyA'] || keys['ArrowLeft']) moveX -= 1;
  if (keys['KeyD'] || keys['ArrowRight']) moveX += 1;

  const isMoving = moveX !== 0 || moveZ !== 0;

  if (isMoving) {
    const moveVector = new THREE.Vector3(moveX, 0, moveZ).normalize();
    moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraAngle);

    player.position.x += moveVector.x * SPEED * delta;
    player.position.z += moveVector.z * SPEED * delta;

    const targetRotation = Math.atan2(moveVector.x, moveVector.z);
    player.rotation.y = THREE.MathUtils.lerp(player.rotation.y, targetRotation, 14 * delta);

    walkCycle += delta * 12;
    if (player.userData.blenderModel) {
      player.userData.blenderModel.position.y = Math.abs(Math.sin(walkCycle * 2)) * 0.12;
      player.userData.blenderModel.rotation.z = Math.sin(walkCycle) * 0.05;
    }
  } else {
    if (player.userData.blenderModel) {
      player.userData.blenderModel.position.y = THREE.MathUtils.lerp(player.userData.blenderModel.position.y, 0, 10 * delta);
      player.userData.blenderModel.rotation.z = THREE.MathUtils.lerp(player.userData.blenderModel.rotation.z, 0, 10 * delta);
    }
  }

  // Salto y Gravedad
  if (keys['Space'] && isGrounded) {
    velocityY = JUMP_FORCE;
    isGrounded = false;
    audio.playJump();
  }

  velocityY += GRAVITY * delta;
  player.position.y += velocityY * delta;

  // Colisiones con plataformas y terreno
  let currentGroundY = -999;

  colliders.forEach((col) => {
    if (col.type === 'ground') {
      const distFromCenter = Math.hypot(player.position.x, player.position.z);
      if (distFromCenter <= col.radius) {
        currentGroundY = Math.max(currentGroundY, col.y);
      }
    } else if (col.type === 'box') {
      if (
        player.position.x >= col.minX - 0.4 &&
        player.position.x <= col.maxX + 0.4 &&
        player.position.z >= col.minZ - 0.4 &&
        player.position.z <= col.maxZ + 0.4
      ) {
        if (player.position.y >= col.topY - 0.6) {
          currentGroundY = Math.max(currentGroundY, col.topY);
        }
      }
    }
  });

  if (player.position.y <= currentGroundY) {
    player.position.y = currentGroundY;
    velocityY = 0;
    isGrounded = true;
  } else {
    isGrounded = false;
  }

  if (player.position.y < -15) {
    player.position.set(0, 1, 10);
    velocityY = 0;
  }

  player.userData.dropShadow.position.x = player.position.x;
  player.userData.dropShadow.position.z = player.position.z;
  player.userData.dropShadow.position.y = currentGroundY + 0.03;
  const shadowScale = Math.max(0.2, 1 - (player.position.y - currentGroundY) * 0.1);
  player.userData.dropShadow.scale.set(shadowScale, shadowScale, 1);

  // Recolección de Bitcoins
  coins.forEach((coin) => {
    if (!coin.userData.active) return;
    const dist = player.position.distanceTo(coin.position);
    if (dist < 1.4) {
      coin.userData.active = false;
      scene.remove(coin);
      collectedCoins++;
      coinCountEl.innerText = collectedCoins;
      audio.playCoin();
    }
  });

  // Contacto con la Estrella
  if (star.userData.active) {
    const distToStar = player.position.distanceTo(star.position);
    if (distToStar < 2.0) {
      triggerVictory();
    }
  }
}

function triggerVictory() {
  currentScene = SCENE_VICTORY;
  star.userData.active = false;
  audio.playVictory();

  player.rotation.y = cameraAngle + Math.PI;
  finalCoinsEl.innerText = collectedCoins;
  setTimeout(() => {
    victoryModal.classList.add('active');
  }, 900);
}

function updateCamera(delta) {
  if (currentScene === SCENE_1_TITLE) {
    // Escena 1: Vista general
    camera.position.set(0, 3, 16);
    camera.lookAt(0, 2, 0);
    return;
  }

  if (currentScene === SCENE_2_HEAD) {
    // Escena 2: Enfocando la cabeza gigante 3D aislada
    camera.position.set(0, 100, 4.2);
    camera.lookAt(0, 100, 0);

    // Animación interactiva: la cabeza de Bukele sigue al ratón
    if (bukeleHeadMesh) {
      const targetRotY = Math.PI + mouseNormalizedX * 0.65;
      const targetRotX = mouseNormalizedY * 0.45;
      bukeleHeadMesh.rotation.y = THREE.MathUtils.lerp(bukeleHeadMesh.rotation.y, targetRotY, 8 * delta);
      bukeleHeadMesh.rotation.x = THREE.MathUtils.lerp(bukeleHeadMesh.rotation.x, targetRotX, 8 * delta);
      bukeleHeadMesh.position.y = Math.sin(clock.elapsedTime * 2) * 0.08;
    }
    return;
  }

  // Escena 3: Cámara de Gameplay en 3ª persona
  const cameraDistance = currentScene === SCENE_VICTORY ? 5.5 : 8.5;
  const cameraHeight = currentScene === SCENE_VICTORY ? 2.5 : 4.0;

  const targetX = player.position.x + Math.sin(cameraAngle) * cameraDistance;
  const targetZ = player.position.z + Math.cos(cameraAngle) * cameraDistance;
  const targetY = player.position.y + cameraHeight;

  camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetX, 8 * delta);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetY, 8 * delta);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZ, 8 * delta);

  camera.lookAt(player.position.x, player.position.y + 1.5, player.position.z);
}

function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);

  if (currentScene >= SCENE_3_GAMEPLAY) {
    coins.forEach((coin) => {
      if (coin.userData.active) {
        coin.rotation.y += delta * 2.5;
        coin.position.y = coin.userData.baseY + Math.sin(clock.elapsedTime * 3) * 0.15;
      }
    });

    if (star.userData.active) {
      star.rotation.y += delta * 2.0;
      star.position.y = star.userData.baseY + Math.sin(clock.elapsedTime * 2.5) * 0.25;
    }

    clouds.forEach((cloud, i) => {
      cloud.position.x += delta * (0.8 + i * 0.2);
      if (cloud.position.x > 50) cloud.position.x = -50;
    });
  }

  updatePhysics(delta);
  updateCamera(delta);

  renderer.render(scene, camera);
}

animate();
