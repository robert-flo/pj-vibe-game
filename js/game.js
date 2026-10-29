import * as THREE from 'three';

/* ==========================================================================
   1. SISTEMA DE AUDIO (Web Audio API Sintetizado)
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
    
    // Tono 1 (B5)
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

    // Tono 2 (E6)
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
    // Fanfarria clásica: Do5, Mi5, Sol5, Do6
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, index) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const start = t + index * 0.14;
      const dur = index === 3 ? 0.6 : 0.12;

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

// Iluminación
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x44aa44, 0.7);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xfff7ed, 1.2);
dirLight.position.set(30, 60, 40);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.near = 10;
dirLight.shadow.camera.far = 150;
const d = 50;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
dirLight.shadow.bias = -0.0005;
scene.add(dirLight);

/* ==========================================================================
   3. CONSTRUCCIÓN PROCEDURAL DE NAYIB BUKELE (3D Low-Poly)
   ========================================================================== */
function createBukeleCharacter() {
  const group = new THREE.Group();

  // Materiales
  const suitMat = new THREE.MeshLambertMaterial({ color: 0x1e293b }); // Traje Azul Marino Oscuro
  const shirtMat = new THREE.MeshLambertMaterial({ color: 0x0f172a }); // Camiseta negra
  const skinMat = new THREE.MeshLambertMaterial({ color: 0xe0ac69 }); // Tono de piel
  const hairMat = new THREE.MeshLambertMaterial({ color: 0x1c1917 }); // Cabello y barba negros
  const shoeMat = new THREE.MeshLambertMaterial({ color: 0x09090b }); // Zapatos oscuros
  const goldPinMat = new THREE.MeshLambertMaterial({ color: 0xf59e0b }); // Pin / Detalle

  // Torso / Saco
  const torsoGeom = new THREE.BoxGeometry(0.8, 1.0, 0.5);
  const torso = new THREE.Mesh(torsoGeom, suitMat);
  torso.position.y = 1.3;
  torso.castShadow = true;
  group.add(torso);

  // Cuello y camiseta interna
  const innerShirt = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.5, 0.52), shirtMat);
  innerShirt.position.set(0, 1.5, 0);
  group.add(innerShirt);

  // Pin dorado de solapa
  const pin = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.05), goldPinMat);
  pin.position.set(-0.25, 1.55, 0.26);
  group.add(pin);

  // Cabeza
  const headGeom = new THREE.BoxGeometry(0.55, 0.6, 0.55);
  const head = new THREE.Mesh(headGeom, skinMat);
  head.position.y = 2.05;
  head.castShadow = true;
  group.add(head);

  // Cabello peinado hacia atrás (volumen superior y posterior)
  const hairTop = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.22, 0.58), hairMat);
  hairTop.position.set(0, 2.36, -0.02);
  hairTop.castShadow = true;
  group.add(hairTop);

  const hairBack = new THREE.Mesh(new THREE.BoxGeometry(0.57, 0.45, 0.15), hairMat);
  hairBack.position.set(0, 2.1, -0.26);
  group.add(hairBack);

  // Barba y bigote característicos recortados
  const beardJaw = new THREE.Mesh(new THREE.BoxGeometry(0.57, 0.25, 0.35), hairMat);
  beardJaw.position.set(0, 1.88, 0.12);
  group.add(beardJaw);

  const mustache = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.08, 0.1), hairMat);
  mustache.position.set(0, 2.0, 0.28);
  group.add(mustache);

  // Ojos
  const eyeMat = new THREE.MeshBasicMaterial({ color: 0x1c1917 });
  const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.06, 0.05), eyeMat);
  eyeL.position.set(-0.15, 2.12, 0.28);
  const eyeR = eyeL.clone();
  eyeR.position.x = 0.15;
  group.add(eyeL);
  group.add(eyeR);

  // Piernas
  const legGeom = new THREE.BoxGeometry(0.3, 0.7, 0.35);
  const leftLeg = new THREE.Mesh(legGeom, suitMat);
  leftLeg.position.set(-0.22, 0.6, 0);
  leftLeg.castShadow = true;
  group.add(leftLeg);

  const rightLeg = new THREE.Mesh(legGeom, suitMat);
  rightLeg.position.set(0.22, 0.6, 0);
  rightLeg.castShadow = true;
  group.add(rightLeg);

  // Zapatos
  const shoeGeom = new THREE.BoxGeometry(0.32, 0.2, 0.45);
  const leftShoe = new THREE.Mesh(shoeGeom, shoeMat);
  leftShoe.position.set(-0.22, 0.1, 0.05);
  leftShoe.castShadow = true;
  group.add(leftShoe);

  const rightShoe = new THREE.Mesh(shoeGeom, shoeMat);
  rightShoe.position.set(0.22, 0.1, 0.05);
  rightShoe.castShadow = true;
  group.add(rightShoe);

  // Brazos
  const armGeom = new THREE.BoxGeometry(0.22, 0.75, 0.25);
  const leftArm = new THREE.Mesh(armGeom, suitMat);
  leftArm.position.set(-0.52, 1.35, 0);
  leftArm.castShadow = true;
  group.add(leftArm);

  const rightArm = new THREE.Mesh(armGeom, suitMat);
  rightArm.position.set(0.52, 1.35, 0);
  rightArm.castShadow = true;
  group.add(rightArm);

  // Sombra circular proyectada en el suelo
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
    leftArm,
    rightArm,
    leftLeg,
    rightLeg,
    leftShoe,
    rightShoe,
    dropShadow
  };

  return group;
}

const player = createBukeleCharacter();
scene.add(player);
player.position.set(0, 0, 10);

/* ==========================================================================
   4. CONSTRUCCIÓN DEL ESCENARIO (Pradera, Colina y Plataformas)
   ========================================================================== */
const colliders = []; // Elementos contra los que se puede colisionar o pisar

// 1. Suelo Principal (Pradera verde circular)
const groundGeom = new THREE.CylinderGeometry(45, 48, 4, 48);
const groundMat = new THREE.MeshLambertMaterial({ color: 0x4ade80 }); // Verde vibrante
const ground = new THREE.Mesh(groundGeom, groundMat);
ground.position.y = -2;
ground.receiveShadow = true;
scene.add(ground);
colliders.push({ type: 'ground', y: 0, radius: 45 });

// 2. Colina Escalable / Pirámide de la Cumbre
function createHill() {
  const hillGroup = new THREE.Group();
  const hillMat = new THREE.MeshLambertMaterial({ color: 0x22c55e });

  // Niveles de la colina
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

// 3. Plataformas flotantes escalonadas
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

// Escalones para subir a la colina
addPlatform(0, 1.8, -4, 4, 3);
addPlatform(8, 3.8, -8, 3.5, 3.5);
addPlatform(-8, 5.8, -12, 3.5, 3.5);
addPlatform(0, 7.8, -14, 3.5, 3);

// 4. Árboles y decoración low-poly
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

// 5. Nubes flotantes
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
   5. COLECCIONABLES (Bitcoins y La Estrella)
   ========================================================================== */
const coins = [];
let collectedCoins = 0;
const totalCoins = 5;

// Crear Moneda Bitcoin
function createBitcoin(x, y, z) {
  const coinGroup = new THREE.Group();

  // Disco dorado
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

  // Borde exterior
  const rimGeom = new THREE.TorusGeometry(0.75, 0.06, 12, 32);
  const rim = new THREE.Mesh(rimGeom, discMat);
  coinGroup.add(rim);

  coinGroup.position.set(x, y, z);
  coinGroup.userData = { baseY: y, active: true };
  scene.add(coinGroup);
  coins.push(coinGroup);
}

// Ubicaciones de los 5 Bitcoins
createBitcoin(0, 1.2, 5);      // Inicio
createBitcoin(0, 3.2, -4);     // Primer escalón
createBitcoin(8, 5.2, -8);     // Plataforma derecha
createBitcoin(-8, 7.2, -12);   // Plataforma izquierda
createBitcoin(0, 9.2, -14);    // Entrada a la cima

// Crear la Estrella Dorada (Objetivo de la Victoria)
function createStar() {
  const starGroup = new THREE.Group();

  // Geometría de estrella de 5 puntas
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

  // Luz dorada resplandeciente
  const starLight = new THREE.PointLight(0xfef08a, 2.0, 15);
  starGroup.add(starLight);

  starGroup.position.set(0, 12.0, -16);
  starGroup.userData = { baseY: 12.0, active: true };
  scene.add(starGroup);

  return starGroup;
}

const star = createStar();

/* ==========================================================================
   6. CONTROLES, FÍSICAS Y CÁMARA
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

let gameActive = false;
let victoryTriggered = false;

// Eventos de teclado
window.addEventListener('keydown', (e) => {
  keys[e.code] = true;
  audio.init();

  if (e.code === 'KeyQ') cameraAngle += 0.08;
  if (e.code === 'KeyE') cameraAngle -= 0.08;
});

window.addEventListener('keyup', (e) => {
  keys[e.code] = false;
});

// Control de cámara con ratón
window.addEventListener('mousedown', (e) => {
  if (e.button === 0) {
    isDragging = true;
    previousMouseX = e.clientX;
    audio.init();
  }
});

window.addEventListener('mouseup', () => {
  isDragging = false;
});

window.addEventListener('mousemove', (e) => {
  if (isDragging && gameActive) {
    const deltaX = e.clientX - previousMouseX;
    cameraAngle -= deltaX * 0.005;
    previousMouseX = e.clientX;
  }
});

// UI Event Listeners
const btnStart = document.getElementById('btn-start');
const startOverlay = document.getElementById('start-overlay');
const victoryModal = document.getElementById('victory-modal');
const btnRestart = document.getElementById('btn-restart');
const coinCountEl = document.getElementById('coin-count');
const finalCoinsEl = document.getElementById('final-coins');

btnStart.addEventListener('click', () => {
  audio.init();
  startOverlay.classList.remove('active');
  gameActive = true;
});

btnRestart.addEventListener('click', () => {
  location.reload();
});

// Redimensionar pantalla
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

/* ==========================================================================
   7. BUCLE PRINCIPAL DE JUEGO
   ========================================================================== */
const clock = new THREE.Clock();
let walkCycle = 0;

function updatePhysics(delta) {
  if (!gameActive || victoryTriggered) return;

  // 1. Vector de movimiento relativo a la cámara
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

    // Rotar suavemente el personaje en la dirección del movimiento
    const targetRotation = Math.atan2(moveVector.x, moveVector.z);
    player.rotation.y = THREE.MathUtils.lerp(player.rotation.y, targetRotation, 14 * delta);

    // Animación de caminar (oscilación de brazos y piernas)
    walkCycle += delta * 12;
    const swing = Math.sin(walkCycle) * 0.6;
    player.userData.leftArm.rotation.x = swing;
    player.userData.rightArm.rotation.x = -swing;
    player.userData.leftLeg.rotation.x = -swing * 0.8;
    player.userData.rightLeg.rotation.x = swing * 0.8;
    player.userData.leftShoe.rotation.x = -swing * 0.8;
    player.userData.rightShoe.rotation.x = swing * 0.8;
  } else {
    // Postura neutra
    player.userData.leftArm.rotation.x = THREE.MathUtils.lerp(player.userData.leftArm.rotation.x, 0, 10 * delta);
    player.userData.rightArm.rotation.x = THREE.MathUtils.lerp(player.userData.rightArm.rotation.x, 0, 10 * delta);
    player.userData.leftLeg.rotation.x = THREE.MathUtils.lerp(player.userData.leftLeg.rotation.x, 0, 10 * delta);
    player.userData.rightLeg.rotation.x = THREE.MathUtils.lerp(player.userData.rightLeg.rotation.x, 0, 10 * delta);
  }

  // 2. Salto y Gravedad
  if (keys['Space'] && isGrounded) {
    velocityY = JUMP_FORCE;
    isGrounded = false;
    audio.playJump();
  }

  velocityY += GRAVITY * delta;
  player.position.y += velocityY * delta;

  // 3. Detección de suelo / colisión con plataformas
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
        // Solo aterrizar si viene desde arriba
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

  // Protección contra caídas al vacío (Respawn)
  if (player.position.y < -15) {
    player.position.set(0, 1, 10);
    velocityY = 0;
  }

  // Actualizar sombra proyectada
  player.userData.dropShadow.position.x = player.position.x;
  player.userData.dropShadow.position.z = player.position.z;
  player.userData.dropShadow.position.y = currentGroundY + 0.03;
  const shadowScale = Math.max(0.2, 1 - (player.position.y - currentGroundY) * 0.1);
  player.userData.dropShadow.scale.set(shadowScale, shadowScale, 1);

  // 4. Recolección de Bitcoins
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

  // 5. Contacto con la Estrella Dorada (¡Victoria!)
  if (star.userData.active) {
    const distToStar = player.position.distanceTo(star.position);
    if (distToStar < 2.0) {
      triggerVictory();
    }
  }
}

function triggerVictory() {
  victoryTriggered = true;
  star.userData.active = false;
  audio.playVictory();

  // Animación de celebración: Nayib alza el brazo
  player.rotation.y = cameraAngle + Math.PI;
  player.userData.rightArm.rotation.x = -Math.PI * 0.85;

  finalCoinsEl.innerText = collectedCoins;
  setTimeout(() => {
    victoryModal.classList.add('active');
  }, 900);
}

function updateCamera(delta) {
  // Posicionar cámara detrás del personaje según cameraAngle
  const cameraDistance = victoryTriggered ? 5.5 : 8.5;
  const cameraHeight = victoryTriggered ? 2.5 : 4.0;

  const targetX = player.position.x + Math.sin(cameraAngle) * cameraDistance;
  const targetZ = player.position.z + Math.cos(cameraAngle) * cameraDistance;
  const targetY = player.position.y + cameraHeight;

  camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetX, 8 * delta);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetY, 8 * delta);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZ, 8 * delta);

  const lookTarget = new THREE.Vector3(player.position.x, player.position.y + 1.5, player.position.z);
  camera.lookAt(lookTarget);
}

function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);

  // Animación ambiental: rotación de monedas
  coins.forEach((coin) => {
    if (coin.userData.active) {
      coin.rotation.y += delta * 2.5;
      coin.position.y = coin.userData.baseY + Math.sin(clock.elapsedTime * 3) * 0.15;
    }
  });

  // Animación de la Estrella
  if (star.userData.active) {
    star.rotation.y += delta * 2.0;
    star.position.y = star.userData.baseY + Math.sin(clock.elapsedTime * 2.5) * 0.25;
  }

  // Movimiento suave de nubes
  clouds.forEach((cloud, i) => {
    cloud.position.x += delta * (0.8 + i * 0.2);
    if (cloud.position.x > 50) cloud.position.x = -50;
  });

  updatePhysics(delta);
  updateCamera(delta);

  renderer.render(scene, camera);
}

// Iniciar bucle
animate();
