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
scene.fog = new THREE.FogExp2(0xbfe3ff, 0.0016);

const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 500);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.NoToneMapping; // Fidelidad N64: colores sin mapeo tonal
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

// Pivote dinámico para rotación natural de la cabeza con el ratón
const headPivot = new THREE.Group();
headSceneGroup.add(headPivot);

// Iluminación cálida y halagadora de estudio fotográfico (elimina sombras tétricas y da vida)
const headAmbient = new THREE.AmbientLight(0xfff5ea, 1.7); // Luz ambiental cálida suave
headSceneGroup.add(headAmbient);

const headKeyLight = new THREE.DirectionalLight(0xfffaee, 1.8); // Luz principal frontal suave
headKeyLight.position.set(1.2, 102.5, 5.0);
scene.add(headKeyLight);

const headWarmFill = new THREE.PointLight(0xffeedb, 1.3, 25); // Relleno melocotón cálido lateral
headWarmFill.position.set(-3.0, 101.5, 3.5);
scene.add(headWarmFill);

const eyeCatchlight = new THREE.PointLight(0xffffff, 1.1, 15); // Destello blanco en los ojos (pupila viva)
eyeCatchlight.position.set(0.0, 100.3, 4.3);
scene.add(eyeCatchlight);

let bukeleHeadMesh = null;
const gltfLoader = new GLTFLoader();

// Carga de bukele_head.glb (Modelo fotorrealista Tripo optimizado y suavizado)
gltfLoader.load(
  'assets/models/bukele_head.glb',
  (gltf) => {
    bukeleHeadMesh = gltf.scene;

    // Suavizado total de normales y acabado de piel natural cálido
    bukeleHeadMesh.traverse((child) => {
      if (child.isMesh) {
        child.material.flatShading = false;
        child.material.roughness = 0.58; // Piel mate natural, elimina reflejos plásticos
        child.material.metalness = 0.0;
        child.material.needsUpdate = true;
        if (child.geometry) {
          child.geometry.computeVertexNormals();
        }
      }
    });

    bukeleHeadMesh.scale.set(1.45, 1.45, 1.45);
    bukeleHeadMesh.position.set(0, -0.2, 0);
    bukeleHeadMesh.rotation.y = -Math.PI / 2; // Orientar exactamente de frente a la cámara
    headPivot.add(bukeleHeadMesh);
    console.log('[GLTF] Cabeza oficial bukele_head.glb cargada con iluminacion calida y piel suave.');
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
player.position.set(0, 0, 8.8);

/* ==========================================================================
   5. ESCENARIO 3D (Pradera, Tubería N64 de Inicio, Colina y Plataformas)
   ========================================================================== */
const colliders = [];
const collisionMeshes = []; // Mallas contra las que se lanzan rayos (suelo / paredes)

// Tubería Verde N64 de Inicio (Donde el juego toma el relevo exacto de la cinemática)
function createWarpPipe(x, y, z) {
  const pipeGroup = new THREE.Group();

  // Parche circular de tierra/arena bajo la tubería (fiel a la escena del segundo 49)
  const dirtGeom = new THREE.CylinderGeometry(2.4, 2.7, 0.15, 32);
  const dirtMat = new THREE.MeshLambertMaterial({ color: 0xe5c07b });
  const dirt = new THREE.Mesh(dirtGeom, dirtMat);
  dirt.position.y = 0.08;
  dirt.receiveShadow = true;
  pipeGroup.add(dirt);

  const pipeMat = new THREE.MeshStandardMaterial({
    color: 0x22c55e,
    roughness: 0.35,
    metalness: 0.15
  });

  // Base / Cuerpo de la tubería
  const bodyGeom = new THREE.CylinderGeometry(1.25, 1.25, 1.8, 28);
  const body = new THREE.Mesh(bodyGeom, pipeMat);
  body.position.y = 0.9;
  body.castShadow = true;
  body.receiveShadow = true;
  pipeGroup.add(body);

  // Borde superior ensanchado de la tubería N64
  const rimGeom = new THREE.CylinderGeometry(1.52, 1.52, 0.65, 28);
  const rim = new THREE.Mesh(rimGeom, pipeMat);
  rim.position.y = 1.85;
  rim.castShadow = true;
  rim.receiveShadow = true;
  pipeGroup.add(rim);

  // Interior hueco oscuro
  const holeGeom = new THREE.CircleGeometry(1.22, 28);
  const holeMat = new THREE.MeshBasicMaterial({ color: 0x052e16 });
  const hole = new THREE.Mesh(holeGeom, holeMat);
  hole.rotation.x = -Math.PI / 2;
  hole.position.y = 2.18;
  pipeGroup.add(hole);

  pipeGroup.position.set(x, y, z);
  scene.add(pipeGroup);
  pipeGroup.updateMatrixWorld(true);
  pipeGroup.traverse((o) => { if (o.isMesh && o !== hole) collisionMeshes.push(o); });

  return pipeGroup;
}


// ---------------------------------------------------------------------------
// Peach's Castle Grounds: geometría extraída de la descompilación de SM64
// (levels/castle_grounds) con las texturas HD de RENDER96. 1 unidad SM64 = 0.01.
// ---------------------------------------------------------------------------
const SM64_SCALE = 0.01;
const CASTLE_SPAWN = new THREE.Vector3(-1328 * SM64_SCALE, 260 * SM64_SCALE, 4664 * SM64_SCALE);
const MOAT_WATER_Y = -81 * SM64_SCALE;
let castleLoaded = false;

// Cielo oceánico original (skybox "water"): cilindro que sigue a la cámara
const skyTex = new THREE.TextureLoader().load('assets/textures/sky/ocean_sky.jpg');
skyTex.colorSpace = THREE.SRGBColorSpace;
skyTex.wrapS = THREE.RepeatWrapping;
skyTex.repeat.set(3, 1);
const skyDome = new THREE.Mesh(
  new THREE.CylinderGeometry(300, 300, 628, 48, 1, true),
  new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false, depthWrite: false })
);
skyDome.renderOrder = -10;
skyDome.visible = false;
scene.add(skyDome);

gltfLoader.load(
  'assets/models/castle_grounds.glb',
  (gltf) => {
    const castle = gltf.scene;
    castle.traverse((child) => {
      if (!child.isMesh) return;
      const old = child.material;
      // SM64 no usa luces: textura x color de vértice (shade), sin iluminación
      const isShadowDecal = (old.name || '').includes('0900BC00'); // sombras IA16 (alpha suave)
      const mat = new THREE.MeshBasicMaterial({
        map: old.map || null,
        vertexColors: !!child.geometry.attributes.color,
        side: THREE.DoubleSide,
        transparent: isShadowDecal,
        alphaTest: isShadowDecal ? 0 : 0.5, // recortes 1-bit del N64 (vallas, árboles, ventanas)
        depthWrite: !isShadowDecal,
        polygonOffset: isShadowDecal,
        polygonOffsetFactor: -2
      });
      if (isShadowDecal) child.renderOrder = 1;
      if (mat.map) {
        mat.map.colorSpace = THREE.SRGBColorSpace;
        mat.map.anisotropy = 8;
      }
      child.material = mat;
      collisionMeshes.push(child);
    });
    scene.add(castle);
    castle.updateMatrixWorld(true);
    castleLoaded = true;
    placeBitcoinsOnPath();
    console.log('[GLTF] castle_grounds.glb cargado:', collisionMeshes.length, 'mallas');
  },
  undefined,
  (err) => console.warn('[GLTF Error] castle_grounds.glb:', err)
);

// Foso: dos planos de agua con la textura original (alpha 0x96)
function addWaterBox(x0, z0, x1, z1) {
  const w = (x1 - x0) * SM64_SCALE;
  const d = (z1 - z0) * SM64_SCALE;
  const tex = new THREE.TextureLoader().load('assets/textures/castle_grounds/water.png');
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(w / 10, d / 10);
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(w, d),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.59, depthWrite: false })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set(((x0 + x1) / 2) * SM64_SCALE, MOAT_WATER_Y, ((z0 + z1) / 2) * SM64_SCALE);
  scene.add(mesh);
  return mesh;
}
const moatWater = addWaterBox(-7129, -7222, 8253, -58);
const lakeWater = addWaterBox(1024, -58, 8230, 8137);

// Raycast hacia abajo para obtener la altura del suelo en (x, z) desde fromY
const groundRay = new THREE.Raycaster();
const RAY_DOWN = new THREE.Vector3(0, -1, 0);
const _rayOrigin = new THREE.Vector3();
function sampleGround(x, z, fromY) {
  _rayOrigin.set(x, fromY, z);
  groundRay.set(_rayOrigin, RAY_DOWN);
  groundRay.far = 400;
  const hits = groundRay.intersectObjects(collisionMeshes, false);
  return hits.length ? hits[0].point.y : -999;
}

// Tubería de inicio (punto de aparición original de Mario 64 en los jardines)
const startWarpPipe = createWarpPipe(CASTLE_SPAWN.x, CASTLE_SPAWN.y, CASTLE_SPAWN.z);
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

// Bitcoins a lo largo del camino hacia el castillo (altura tomada del suelo real)
const COIN_PATH = [
  [-13.3, 38], [-10.5, 29], [-7, 21], [-3.5, 13], [0, 6],
  [0, 0.8], [0, -5], [0, -10.5], [0, -15.5]
];
function placeBitcoinsOnPath() {
  COIN_PATH.forEach(([x, z]) => {
    const gy = sampleGround(x, z, 20);
    if (gy > -900) createBitcoin(x, gy + 1.2, z);
  });
}

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

// El objetivo ahora es cruzar la puerta del castillo (sin estrella)
const star = { userData: { active: false, baseY: 0 }, position: new THREE.Vector3(), rotation: { y: 0 } };

/* ==========================================================================
   7. MÁQUINA DE ESTADOS DE ESCENAS
   ========================================================================== */
const SCENE_1_TITLE = 1;
const SCENE_2_HEAD = 2;
const SCENE_3_FILESELECT = 3;
const SCENE_4_LETTER = 4;
const SCENE_5_CINEMATIC = 5;
const SCENE_6_GAMEPLAY = 6;
const SCENE_VICTORY = 7;

let currentScene = SCENE_1_TITLE;
let scene2EnterTime = 0;

const headBgMosaic = document.getElementById('head-bg-mosaic');
const scene1Title = document.getElementById('scene-1-title');
const btnScene1Start = document.getElementById('btn-scene-1-start');

const scene2Overlay = document.getElementById('scene-2-overlay');
const btnScene2Start = document.getElementById('btn-scene-2-start');

const scene3FileSelect = document.getElementById('scene-3-fileselect');
const n64HandCursor = document.getElementById('n64-hand-cursor');

const sceneLetter = document.getElementById('scene-letter');
const audioLetter = document.getElementById('audio-letter');
const sceneCinematic = document.getElementById('scene-cinematic');
const cinematicVideo = document.getElementById('cinematic-video');
const btnSkipCinematic = document.getElementById('btn-skip-cinematic');

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

  currentScene = SCENE_2_HEAD;
  scene2EnterTime = performance.now();
  scene.background = null; // Canvas transparente para proyectar la cabeza sobre el mosaico
  scene1Title.classList.remove('active');
  headBgMosaic.classList.remove('hidden');
  scene2Overlay.classList.remove('hidden');
}

// Transición: Escena 2 -> Escena 3 (Pantalla SELECT FILE)
function goToScene3(force = false) {
  if (currentScene !== SCENE_2_HEAD) return;
  // Cooldown de 2.2 segundos para que el usuario pueda interactuar con el rostro 3D de Bukele
  if (!force && performance.now() - scene2EnterTime < 2200) return;

  audio.init();
  audio.playStartChime();

  currentScene = SCENE_3_FILESELECT;
  headBgMosaic.classList.add('hidden');
  scene2Overlay.classList.add('hidden');
  scene3FileSelect.classList.remove('hidden');
  n64HandCursor.classList.remove('hidden');

  // Posicionar la mano N64 inicialmente sobre el Slot BUKELE A como en Mario 64
  requestAnimationFrame(() => {
    const firstSlot = document.querySelector('.file-card');
    if (firstSlot && n64HandCursor) {
      const rect = firstSlot.getBoundingClientRect();
      n64HandCursor.style.left = (rect.left + 52) + 'px';
      n64HandCursor.style.top = (rect.top + 28) + 'px';
    }
  });
}

// Transición: Escena 3 -> Escena 4 (La Carta de Gabriela)
function goToSceneLetter() {
  if (currentScene !== SCENE_3_FILESELECT) return;

  audio.init();
  audio.playStartChime();

  currentScene = SCENE_4_LETTER;
  scene3FileSelect.classList.add('hidden');
  n64HandCursor.classList.add('hidden');
  sceneLetter.classList.remove('hidden');

  if (audioLetter) {
    audioLetter.currentTime = 0;
    audioLetter.play().catch((err) => console.log('[Audio] letter_bgm blocked:', err));
  }
}

// Transición: Escena 4 -> Escena 5 (Cinemática Lakitu volando al Castillo)
function goToSceneCinematic() {
  if (currentScene !== SCENE_4_LETTER) return;

  if (audioLetter) {
    audioLetter.pause();
  }

  currentScene = SCENE_5_CINEMATIC;
  sceneLetter.classList.add('hidden');
  sceneCinematic.classList.remove('hidden');

  if (cinematicVideo) {
    cinematicVideo.currentTime = 0;
    cinematicVideo.play().catch((err) => console.log('[Video] cinematic play blocked:', err));
  }
}

// Transición: Escena 5 -> Escena 6 (Gameplay 3D)
function goToSceneGameplay() {
  if (currentScene !== SCENE_5_CINEMATIC && currentScene !== SCENE_4_LETTER && currentScene !== SCENE_3_FILESELECT) return;

  if (audioLetter) audioLetter.pause();
  if (cinematicVideo) cinematicVideo.pause();

  audio.init();
  audio.playLetsGoChime();

  currentScene = SCENE_6_GAMEPLAY;
  scene.background = new THREE.Color(0x7dd3fc); // Fondo cielo diurno de pradera
  sceneLetter.classList.add('hidden');
  sceneCinematic.classList.add('hidden');
  scene3FileSelect.classList.add('hidden');
  n64HandCursor.classList.add('hidden');
  hud.classList.remove('hidden');
  controlsHint.classList.remove('hidden');
  skyDome.visible = true;

  // El relevo de la cinemática: Bukele aparece junto a la tubería verde N64
  respawnPlayer();
}

scene1Title.addEventListener('click', () => goToScene2());
btnScene1Start.addEventListener('click', (e) => {
  e.stopPropagation();
  goToScene2();
});

// En Escena 2, el botón Rainbow PRESS START pasa a SELECT FILE
btnScene2Start.addEventListener('click', (e) => {
  e.stopPropagation();
  goToScene3();
});

// En Escena 3, cualquier clic en la pantalla SELECT FILE avanza a la Carta de Gabriela
if (scene3FileSelect) {
  scene3FileSelect.addEventListener('click', () => {
    goToSceneLetter();
  });
}

// En Escena 4, clic en la Carta de Gabriela avanza a la cinemática
if (sceneLetter) {
  sceneLetter.addEventListener('click', () => {
    goToSceneCinematic();
  });
}

// En Escena 5, fin del video o clic en saltar avanza a Gameplay
if (cinematicVideo) {
  cinematicVideo.addEventListener('ended', () => {
    goToSceneGameplay();
  });
}
if (btnSkipCinematic) {
  btnSkipCinematic.addEventListener('click', (e) => {
    e.stopPropagation();
    goToSceneGameplay();
  });
}
if (sceneCinematic) {
  sceneCinematic.addEventListener('click', () => {
    goToSceneGameplay();
  });
}

btnRestart.addEventListener('click', () => location.reload());

// Soporte de navegación directa por parámetro URL (?scene=2, 3, letter/4, cinematic/5, gameplay/6)
const urlParams = new URLSearchParams(window.location.search);
const requestedScene = urlParams.get('scene');
if (requestedScene === '2') {
  setTimeout(() => goToScene2(), 100);
} else if (requestedScene === '3') {
  setTimeout(() => {
    goToScene2();
    setTimeout(() => goToScene3(true), 50);
  }, 100);
} else if (requestedScene === 'letter' || requestedScene === '4') {
  setTimeout(() => {
    goToScene2();
    goToScene3(true);
    setTimeout(() => goToSceneLetter(), 50);
  }, 100);
} else if (requestedScene === 'cinematic' || requestedScene === '5') {
  setTimeout(() => {
    goToScene2();
    goToScene3(true);
    goToSceneLetter();
    setTimeout(() => goToSceneCinematic(), 50);
  }, 100);
} else if (requestedScene === 'gameplay' || requestedScene === '6') {
  setTimeout(() => {
    goToScene2();
    goToScene3(true);
    goToSceneLetter();
    goToSceneCinematic();
    setTimeout(() => goToSceneGameplay(), 50);
  }, 100);
}

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
let previousMouseY = 0;

let mouseNormalizedX = 0;
let mouseNormalizedY = 0;

let headDragYaw = 0;
let headDragPitch = 0;

window.addEventListener('keydown', (e) => {
  keys[e.code] = true;
  audio.init();

  if (currentScene === SCENE_1_TITLE && (e.code === 'Space' || e.code === 'Enter')) {
    goToScene2();
    return;
  }
  // En Escena 2, únicamente Enter (no Space) avanza si ya pasaron al menos 2.2s
  if (currentScene === SCENE_2_HEAD && e.code === 'Enter' && !e.repeat) {
    goToScene3();
    return;
  }
  // En Escena 3, cualquier tecla Enter o Espacio avanza a la Carta de Gabriela
  if (currentScene === SCENE_3_FILESELECT && (e.code === 'Space' || e.code === 'Enter')) {
    goToSceneLetter();
    return;
  }
  // En Escena 4 (Carta), avanzar a la Cinemática
  if (currentScene === SCENE_4_LETTER && (e.code === 'Space' || e.code === 'Enter')) {
    goToSceneCinematic();
    return;
  }
  // En Escena 5 (Cinemática), saltar directo a Gameplay
  if (currentScene === SCENE_5_CINEMATIC && (e.code === 'Space' || e.code === 'Enter' || e.code === 'Escape')) {
    goToSceneGameplay();
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

  // Seguimiento del cursor de mano 3D en Escena 3 (Pantalla SELECT FILE)
  if (currentScene === SCENE_3_FILESELECT && n64HandCursor) {
    n64HandCursor.style.left = e.clientX + 'px';
    n64HandCursor.style.top = e.clientY + 'px';
  }

  // Interacción de arrastre en Escena 2 estilo Mario 64
  if (isDragging && currentScene === SCENE_2_HEAD) {
    const deltaX = e.clientX - previousMouseX;
    const deltaY = e.clientY - previousMouseY;
    headDragYaw += deltaX * 0.006;
    headDragPitch += deltaY * 0.006;
    previousMouseX = e.clientX;
    previousMouseY = e.clientY;
  }

  if (isDragging && currentScene === SCENE_6_GAMEPLAY) {
    const deltaX = e.clientX - previousMouseX;
    cameraAngle -= deltaX * 0.005;
    previousMouseX = e.clientX;
  }
});

window.addEventListener('mousedown', (e) => {
  if (e.button === 0) {
    isDragging = true;
    previousMouseX = e.clientX;
    previousMouseY = e.clientY;
    audio.init();

    // Avance secuencial por clic
    if (currentScene === SCENE_1_TITLE) {
      goToScene2();
    } else if (currentScene === SCENE_3_FILESELECT) {
      goToSceneLetter();
    } else if (currentScene === SCENE_4_LETTER) {
      goToSceneCinematic();
    } else if (currentScene === SCENE_5_CINEMATIC) {
      goToSceneGameplay();
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


const STEP_HEIGHT = 0.8;
const PLAYER_RADIUS = 0.45;
const wallRay = new THREE.Raycaster();
const _wallDir = new THREE.Vector3();
const _wallOrigin = new THREE.Vector3();

// Devuelve true si hay una pared (normal casi horizontal) en la dirección dada
function wallAhead(dx, dz) {
  const len = Math.hypot(dx, dz);
  if (len < 1e-6) return false;
  _wallDir.set(dx / len, 0, dz / len);
  for (const h of [STEP_HEIGHT + 0.1, 1.4]) {
    _wallOrigin.set(player.position.x, player.position.y + h, player.position.z);
    wallRay.set(_wallOrigin, _wallDir);
    wallRay.far = len + PLAYER_RADIUS;
    const hits = wallRay.intersectObjects(collisionMeshes, false);
    if (hits.length && hits[0].face && Math.abs(hits[0].face.normal.y) < 0.55) return true;
  }
  return false;
}

// Movimiento con deslizamiento sobre paredes (ejes por separado)
function moveWithCollision(dx, dz) {
  if (!wallAhead(dx, dz)) {
    player.position.x += dx;
    player.position.z += dz;
    return;
  }
  if (!wallAhead(dx, 0)) player.position.x += dx;
  else if (!wallAhead(0, dz)) player.position.z += dz;
}

function respawnPlayer() {
  // Aparece junto a la tubería, mirando hacia el castillo (como en el juego original)
  player.position.set(CASTLE_SPAWN.x, CASTLE_SPAWN.y + 0.2, CASTLE_SPAWN.z - 3.2);
  player.rotation.y = Math.PI;
  velocityY = 0;
  isGrounded = false;
  cameraAngle = 0;
}

function updatePhysics(delta) {
  if (currentScene !== SCENE_6_GAMEPLAY) return;

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

    moveWithCollision(moveVector.x * SPEED * delta, moveVector.z * SPEED * delta);

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

  velocityY = Math.max(velocityY + GRAVITY * delta, -45);
  player.position.y += velocityY * delta;

  // Suelo real del castillo (raycast sobre la malla), con pegado a pendientes
  let currentGroundY = sampleGround(player.position.x, player.position.z, player.position.y + STEP_HEIGHT);
  if (currentGroundY > -900 && player.position.y <= currentGroundY && velocityY <= 0) {
    player.position.y = currentGroundY;
    velocityY = 0;
    isGrounded = true;
  } else if (isGrounded && currentGroundY > -900 && velocityY <= 0 && player.position.y - currentGroundY < 0.35) {
    player.position.y = currentGroundY;
  } else {
    isGrounded = false;
  }

  // Caer al foso: reaparece en la tubería
  if (player.position.y < MOAT_WATER_Y - 0.9 || player.position.y < -15) {
    respawnPlayer();
    currentGroundY = player.position.y;
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

  // Fin del juego: Bukele cruza la puerta del castillo
  if (castleLoaded && currentScene === SCENE_6_GAMEPLAY &&
      Math.abs(player.position.x) < 4.5 && player.position.z < -1.2 && player.position.z > -8 &&
      player.position.y > 4.5) {
    triggerVictory();
  }

  // Contacto con la Estrella (desactivada)
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
    camera.position.set(0, 100, 3.8);
    camera.lookAt(0, 100, 0);

    // Animación interactiva: rotación natural y fluida con seguimiento de ratón
    if (headPivot && bukeleHeadMesh) {
      // Retorno elástico al soltar el clic
      if (!isDragging) {
        headDragYaw = THREE.MathUtils.lerp(headDragYaw, 0, 8 * delta);
        headDragPitch = THREE.MathUtils.lerp(headDragPitch, 0, 8 * delta);
      }

      const targetRotY = mouseNormalizedX * 0.85 + headDragYaw;
      const targetRotX = mouseNormalizedY * 0.45 + headDragPitch;
      const targetRotZ = -mouseNormalizedX * 0.12;

      headPivot.rotation.y = THREE.MathUtils.lerp(headPivot.rotation.y, targetRotY, 10 * delta);
      headPivot.rotation.x = THREE.MathUtils.lerp(headPivot.rotation.x, targetRotX, 10 * delta);
      headPivot.rotation.z = THREE.MathUtils.lerp(headPivot.rotation.z, targetRotZ, 10 * delta);

      headPivot.position.y = Math.sin(clock.elapsedTime * 2.5) * 0.04;
    }
    return;
  }

  if (currentScene === SCENE_3_FILESELECT || currentScene === SCENE_4_LETTER || currentScene === SCENE_5_CINEMATIC) {
    // Escenas 2D / cinemáticas: la cámara 3D se mantiene en reposo
    return;
  }

  // Escena 6: Cámara de Gameplay en 3ª persona
  const cameraDistance = currentScene === SCENE_VICTORY ? 5.5 : 8.5;
  const cameraHeight = currentScene === SCENE_VICTORY ? 2.5 : 4.0;

  const targetX = player.position.x + Math.sin(cameraAngle) * cameraDistance;
  const targetZ = player.position.z + Math.cos(cameraAngle) * cameraDistance;
  const targetY = player.position.y + cameraHeight;

  camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetX, 8 * delta);
  camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetY, 8 * delta);
  camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZ, 8 * delta);

  camera.lookAt(player.position.x, player.position.y + 1.5, player.position.z);

  // Cámara de depuración para capturas: ?cam=x,y,z,tx,ty,tz
  const dbg = new URLSearchParams(window.location.search).get('cam');
  if (dbg) {
    const c = dbg.split(',').map(Number);
    camera.position.set(c[0], c[1], c[2]);
    camera.lookAt(c[3], c[4], c[5]);
  }
}

function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);

  if (currentScene >= SCENE_6_GAMEPLAY) {
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

  }

  updatePhysics(delta);
  updateCamera(delta);
  if (skyDome.visible) skyDome.position.set(camera.position.x, camera.position.y + 6, camera.position.z);

  renderer.render(scene, camera);
}

animate();
