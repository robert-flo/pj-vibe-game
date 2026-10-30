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

  // Héroe jugable (Desktop/assets2): cuerpo en Blender (bukele_body.glb) + cabeza real (bukele_head.glb)
  const heroPivot = new THREE.Group();   // el modelo mira a +X; se gira para mirar a +Z
  heroPivot.rotation.y = -Math.PI / 2;
  const heroRoot = new THREE.Group();
  heroPivot.add(heroRoot);
  group.add(heroPivot);
  group.userData.blenderModel = heroRoot;
  group.userData.limbs = {};

  gltfLoader.load('assets/models/bukele_body.glb', (gltf) => {
    gltf.scene.traverse((child) => {
      if (child.isMesh) { child.castShadow = true; child.receiveShadow = true; }
      if (['ArmL', 'ArmR', 'LegL', 'LegR'].includes(child.name)) group.userData.limbs[child.name] = child;
    });
    heroRoot.add(gltf.scene);
  }, undefined, (err) => console.warn('[GLTF] bukele_body.glb:', err));

  return group;
}

const player = createBukeleCharacter();
scene.add(player);
player.position.set(0, 0, 8.8);

// Carga única de bukele_head.glb (reutilizada en Escena 2 y clonada para el héroe en Gameplay)
gltfLoader.load(
  'assets/models/bukele_head.glb',
  (gltf) => {
    const rawHead = gltf.scene;
    rawHead.traverse((child) => {
      if (child.isMesh && child.geometry) {
        child.geometry.computeVertexNormals();
      }
    });

    // 1. Clon para el héroe jugable con recorte limpio de busto/cuello
    const heroHead = rawHead.clone(true);
    heroHead.traverse((child) => {
      if (!child.isMesh) return;
      child.castShadow = true;
      child.material = child.material.clone();
      child.material.flatShading = false;
      child.material.roughness = 0.6;
      child.material.metalness = 0;
      child.material.onBeforeCompile = (sh) => {
        sh.vertexShader = sh.vertexShader
          .replace('#include <common>', '#include <common>\nvarying vec3 vHeadPos;')
          .replace('#include <begin_vertex>', '#include <begin_vertex>\nvHeadPos = position;');
        sh.fragmentShader = sh.fragmentShader
          .replace('#include <common>', '#include <common>\nvarying vec3 vHeadPos;')
          .replace('#include <clipping_planes_fragment>', '#include <clipping_planes_fragment>\n' +
            'if (vHeadPos.y < -0.34 || (vHeadPos.y < -0.21 && vHeadPos.x < -0.04) || (vHeadPos.y < -0.19 && (abs(vHeadPos.z) > 0.13 || vHeadPos.x < -0.18 || vHeadPos.x > 0.23))) discard;');
      };
      child.material.needsUpdate = true;
    });
    const HS = 0.9;
    heroHead.scale.setScalar(HS);
    heroHead.position.set(0, 1.80, 0);
    player.userData.blenderModel.add(heroHead);

    // 2. Busto interactivo para Escena 2
    bukeleHeadMesh = rawHead;
    bukeleHeadMesh.traverse((child) => {
      if (child.isMesh) {
        child.material.flatShading = false;
        child.material.roughness = 0.58;
        child.material.metalness = 0.0;
        child.material.needsUpdate = true;
      }
    });
    bukeleHeadMesh.scale.set(1.45, 1.45, 1.45);
    bukeleHeadMesh.position.set(0, -0.2, 0);
    bukeleHeadMesh.rotation.y = -Math.PI / 2;
    headPivot.add(bukeleHeadMesh);
    console.log('[GLTF] Cabeza oficial bukele_head.glb cargada e instanciada.');
  },
  undefined,
  (err) => console.warn('[GLTF Error] bukele_head.glb:', err)
);

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
      const mname = old.name || '';
      const isShadowDecal = mname.includes('0900BC00');
      const isUntextured = mname.includes('untextured_shade') || !old.map;
      const mat = new THREE.MeshBasicMaterial({
        map: isUntextured ? null : (old.map || null),
        vertexColors: !!child.geometry.attributes.color,
        side: THREE.DoubleSide,
        transparent: isShadowDecal,
        alphaTest: (isShadowDecal || isUntextured) ? 0 : 0.5,
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
      if (!isShadowDecal) collisionMeshes.push(child);
    });
    scene.add(castle);
    castle.updateMatrixWorld(true);
    castleLoaded = true;
    placeBitcoinsOnPath();
    placeWoodenSignposts();
    if (currentScene === SCENE_6_GAMEPLAY) {
      const gy = sampleGround(player.position.x, player.position.z, player.position.y + 4.0);
      if (gy > -900) {
        player.position.y = gy;
        velocityY = 0;
        isGrounded = true;
      }
    }
    console.log('[GLTF] castle_grounds.glb cargado:', collisionMeshes.length, 'mallas');
  },
  undefined,
  (err) => console.warn('[GLTF Error] castle_grounds.glb:', err)
);

// Foso y lago: planos de agua con la textura original (alpha 0x96)
function addWaterBox(x0, z0, x1, z1) {
  const w = (x1 - x0) * SM64_SCALE;
  const d = (z1 - z0) * SM64_SCALE;
  const tex = new THREE.TextureLoader().load('assets/textures/castle_grounds/water.png');
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(w / 10, d / 10);
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(w, d),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.62, depthWrite: false })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set(((x0 + x1) / 2) * SM64_SCALE, MOAT_WATER_Y, ((z0 + z1) / 2) * SM64_SCALE);
  scene.add(mesh);
  return { mesh, tex };
}
const moatWater = addWaterBox(-7129, -7222, 8253, -58);
const lakeWater = addWaterBox(1024, -58, 8230, 8137);

// Cascada oficial de Castle Grounds (extraída de movtext.inc.c)
const waterfallTex = new THREE.TextureLoader().load('assets/textures/castle_grounds/water.png');
waterfallTex.colorSpace = THREE.SRGBColorSpace;
waterfallTex.wrapS = waterfallTex.wrapT = THREE.RepeatWrapping;
(function buildCastleWaterfall() {
  const wfVerts = [
    [-4469, -800, -6413, 0, 0], [-5525, 1171, -7026, 2, 0], [-6292, 2028, -7463, 4, 0], [-7302, 2955, -7461, 6, 0],
    [-4883, -800, -5690, 0, 3], [-5547, 1110, -6097, 2, 3], [-6732, 2587, -6770, 4, 3], [-7603, 3004, -7160, 6, 3],
    [-5580, -800, -4740, 0, 6], [-6205, 1068, -5347, 2, 6], [-7249, 2566, -6192, 4, 6],
    [-6895, -800, -4714, 0, 9], [-7201, 1083, -5071, 2, 9], [-7578, 2042, -5766, 4, 9], [-8132, 2961, -6761, 6, 9]
  ];
  const wfIdx = [
    0,1,5, 0,5,4, 1,2,6, 1,6,5, 2,3,6, 3,7,6,
    4,5,9, 4,9,8, 5,6,9, 6,10,9, 6,7,10, 8,9,12,
    8,12,11, 9,10,13, 9,13,12, 10,7,14, 10,14,13
  ];
  const pos = new Float32Array(wfVerts.length * 3);
  const uvs = new Float32Array(wfVerts.length * 2);
  wfVerts.forEach(([x, y, z, s, t], i) => {
    pos[i * 3] = x * SM64_SCALE;
    pos[i * 3 + 1] = y * SM64_SCALE;
    pos[i * 3 + 2] = z * SM64_SCALE;
    uvs[i * 2] = t * 0.45;
    uvs[i * 2 + 1] = s * 0.65;
  });
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  geom.setIndex(wfIdx);
  const mesh = new THREE.Mesh(
    geom,
    new THREE.MeshBasicMaterial({ map: waterfallTex, transparent: true, opacity: 0.78, side: THREE.DoubleSide, depthWrite: false })
  );
  scene.add(mesh);
})();

// Banderas rojas ondeando en las 4 torres de Peach's Castle (script.c: bhvCastleFlagWaving)
const castleFlags = [];
(function buildCastleFlags() {
  const flagCoords = [
    [-3213, 3348, -3011],
    [ 3213, 3348, -3011],
    [-3835, 3348, -6647],
    [ 3835, 3348, -6647]
  ];
  const poleMat = new THREE.MeshBasicMaterial({ color: 0xd4d4d8 });
  const flagMat = new THREE.MeshBasicMaterial({ color: 0xdc2626, side: THREE.DoubleSide });
  flagCoords.forEach(([fx, fy, fz], idx) => {
    const g = new THREE.Group();
    g.position.set(fx * SM64_SCALE, fy * SM64_SCALE, fz * SM64_SCALE);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 4.2, 8), poleMat);
    pole.position.y = 1.6;
    g.add(pole);
    const clothGeom = new THREE.PlaneGeometry(3.6, 1.9, 8, 2);
    clothGeom.translate(1.8, 0, 0);
    const cloth = new THREE.Mesh(clothGeom, flagMat);
    cloth.position.y = 2.65;
    cloth.userData = { basePos: clothGeom.attributes.position.array.slice(), phase: idx * 1.3 };
    g.add(cloth);
    scene.add(g);
    castleFlags.push(cloth);
  });
})();

// Los 26 árboles oficiales de Castle Grounds (collision.inc.c: special_bubble_tree)
const castleTrees = [];
const treeTrunks = [];
(function buildCastleTrees() {
  const treeCoords = [
    [-1333, 711, 1881], [-6220, 468, 3458], [-5069, 350, 3221], [-2566, 438, 2626],
    [-1900, 401, 2868], [ 6399, 494,-1680], [  767, 498, 2598], [ 1476, 189, 3280],
    [ 3153, 206,  469], [ 6178, 219,  167], [-6510, 260, 1411], [ 5457, 528,-3259],
    [ 5868, 698,-4453], [ 6408, 869,-5314], [-4711, 342,  433], [ 1132, 365, 1977],
    [-5506, 364, -661], [-6269, 402,-2145], [-5600, 440,-2627], [ 1919, 268, 1157],
    [-5957, 517,-3447], [-2021, 633, 1468], [ -109, 613, 3008], [ 5774, 413,-1114],
    [ 5954, 526,-2846], [-5204, 296,  811]
  ];
  const loader = new THREE.TextureLoader();
  const texL = loader.load('assets/textures/castle_grounds/tree_left_side.rgba16.png');
  const texR = loader.load('assets/textures/castle_grounds/tree_right_side.rgba16.png');
  [texL, texR].forEach((t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  });

  // Geometría exacta de tree_seg3_dl_0302FEE8 (2 triángulos unidos al centro)
  function makeHalfTri(x0, x1, u0, u1, tex) {
    const g = new THREE.BufferGeometry();
    const v = new Float32Array([
      x0, -0.09, 0,
      x1, -0.09, 0,
      0,   8.00, 0
    ]);
    const uv = new Float32Array([
      u0, 1 - (2012 / 32) / 64,
      u1, 1 - (2012 / 32) / 64,
      (x0 < 0 ? u1 : u0), 1 - (-712 / 32) / 64
    ]);
    g.setAttribute('position', new THREE.BufferAttribute(v, 3));
    g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    return new THREE.Mesh(
      g,
      new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.5, side: THREE.DoubleSide })
    );
  }
  const leftProto = makeHalfTri(-3.56, 0, (-796 / 32) / 32, (990 / 32) / 32, texL);
  const rightProto = makeHalfTri(0, 3.58, 0, (1756 / 32) / 32, texR);

  treeCoords.forEach(([tx, ty, tz]) => {
    const px = tx * SM64_SCALE;
    const py = ty * SM64_SCALE;
    const pz = tz * SM64_SCALE;
    const tg = new THREE.Group();
    tg.position.set(px, py, pz);
    tg.add(leftProto.clone(), rightProto.clone());
    scene.add(tg);
    castleTrees.push(tg);
    treeTrunks.push({ x: px, y: py, z: pz, r: 0.65 });
  });
})();

// Puertas Dobles Estelares de Peach's Castle (collision.inc.c: special_castle_door_warp)
const doorLeftPivot = new THREE.Group();
const doorRightPivot = new THREE.Group();
doorLeftPivot.position.set(-1.53, 8.03, -31.55);
doorRightPivot.position.set( 1.54, 8.03, -31.55);
scene.add(doorLeftPivot, doorRightPivot);

gltfLoader.load(
  'assets/models/castle_door.glb',
  (gltf) => {
    const proto = gltf.scene;
    proto.traverse((child) => {
      if (!child.isMesh) return;
      const old = child.material;
      const isUntextured = (old.name || '').includes('untextured_shade') || !old.map;
      const mat = new THREE.MeshBasicMaterial({
        map: isUntextured ? null : old.map,
        vertexColors: !!child.geometry.attributes.color,
        alphaTest: isUntextured ? 0 : 0.45,
        side: THREE.DoubleSide
      });
      if (mat.map) mat.map.colorSpace = THREE.SRGBColorSpace;
      child.material = mat;
    });
    const leftLeaf = proto.clone(true);
    const rightLeaf = proto.clone(true);
    rightLeaf.scale.x = -1; // Espejo simétrico con emblema de estrella mirando hacia +Z (puente)
    doorLeftPivot.add(leftLeaf);
    doorRightPivot.add(rightLeaf);
  },
  undefined,
  (err) => console.warn('[GLTF Error] castle_door.glb:', err)
);

// Carteles cómicos de madera (wooden_signpost.glb) a lo largo del recorrido
const signposts = [];
const SIGN_DEFINITIONS = [
  {
    x: -15.66, z: 35.03, yaw: 0.35,
    title: '🪧 Decreto Presidencial N.° 64',
    text: '«Bienvenido a los Jardines Reales. Queda estrictamente prohibido perder vidas; aquí todos los Bitcoins son de curso legal.»'
  },
  {
    x: -5.80, z: 16.50, yaw: 0.45,
    title: '🪧 Ministerio de Obras Públicas 64',
    text: '«Puente Real recién pavimentado con texturas HD. Cero baches, cero tortugas Koopa, 100% iluminado.»'
  },
  {
    x: 1.95, z: -2.20, yaw: -0.35,
    title: '🪧 Guardia del Castillo',
    text: '«La Primera Dama Gabriela te espera cruzando las Puertas Estelares al fondo del puente. ¡Sigue los Bitcoins!»'
  },
  {
    x: 17.40, z: 25.00, yaw: -Math.PI / 2,
    title: '🪧 Mirador de la Laguna',
    text: '«Zona ecológica protegida: prohibido lanzar pingüinos o nadar de traje formal en el foso del castillo.»'
  }
];

function placeWoodenSignposts() {
  gltfLoader.load(
    'assets/models/wooden_signpost.glb',
    (gltf) => {
      const proto = gltf.scene;
      proto.traverse((c) => {
        if (!c.isMesh) return;
        const mat = new THREE.MeshBasicMaterial({
          map: c.material.map || null,
          vertexColors: !!c.geometry.attributes.color,
          side: THREE.DoubleSide
        });
        if (mat.map) mat.map.colorSpace = THREE.SRGBColorSpace;
        c.material = mat;
      });
      SIGN_DEFINITIONS.forEach((def) => {
        const gy = sampleGround(def.x, def.z, 12.0);
        if (gy < -900) return;
        const sg = proto.clone(true);
        sg.position.set(def.x, gy, def.z);
        sg.rotation.y = def.yaw;
        scene.add(sg);
        signposts.push({ x: def.x, y: gy, z: def.z, title: def.title, text: def.text });
      });
    },
    undefined,
    (err) => console.warn('[GLTF Error] wooden_signpost.glb:', err)
  );
}

// Raycast hacia abajo para obtener la altura del suelo caminable en (x, z) desde fromY
const groundRay = new THREE.Raycaster();
const RAY_DOWN = new THREE.Vector3(0, -1, 0);
const _rayOrigin = new THREE.Vector3();
const _worldNormal = new THREE.Vector3();
function sampleGround(x, z, fromY) {
  _rayOrigin.set(x, fromY, z);
  groundRay.set(_rayOrigin, RAY_DOWN);
  groundRay.far = 400;
  const hits = groundRay.intersectObjects(collisionMeshes, false);
  for (const h of hits) {
    if (!h.face) return h.point.y;
    _worldNormal.copy(h.face.normal).transformDirection(h.object.matrixWorld);
    if (Math.abs(_worldNormal.y) > 0.42) {
      return h.point.y;
    }
  }
  return -999;
}

// Tubería de inicio (punto de aparición original de Mario 64 en los jardines)
const startWarpPipe = createWarpPipe(CASTLE_SPAWN.x, CASTLE_SPAWN.y, CASTLE_SPAWN.z);
/* ==========================================================================
   6. COLECCIONABLES (Bitcoins con Símbolo ₿ en Relieve)
   ========================================================================== */
const coins = [];
let collectedCoins = 0;

function createBitcoinFaceTexture() {
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = 256;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(96, 84, 14, 128, 128, 124);
  grad.addColorStop(0, '#fef08a');
  grad.addColorStop(0.45, '#f59e0b');
  grad.addColorStop(1, '#b45309');
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(128, 128, 124, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = '#fde047';
  ctx.lineWidth = 10;
  ctx.beginPath();
  ctx.arc(128, 128, 106, 0, Math.PI * 2);
  ctx.stroke();

  ctx.save();
  ctx.translate(128, 128);
  ctx.rotate(-Math.PI / 2);
  ctx.fillStyle = '#78350f';
  ctx.font = 'bold 142px Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('₿', 4, 8);

  ctx.fillStyle = '#fef9c3';
  ctx.fillText('₿', -1, 3);
  ctx.restore();

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
const bitcoinFaceTex = createBitcoinFaceTexture();

function createBitcoin(x, y, z) {
  const coinGroup = new THREE.Group();
  const edgeMat = new THREE.MeshStandardMaterial({
    color: 0xf59e0b,
    metalness: 0.85,
    roughness: 0.22,
    emissive: 0x78350f,
    emissiveIntensity: 0.35
  });
  const faceMat = new THREE.MeshStandardMaterial({
    map: bitcoinFaceTex,
    metalness: 0.65,
    roughness: 0.28,
    emissive: 0x78350f,
    emissiveIntensity: 0.25
  });
  const discGeom = new THREE.CylinderGeometry(0.68, 0.68, 0.14, 28);
  const disc = new THREE.Mesh(discGeom, [edgeMat, faceMat, faceMat]);
  disc.rotation.x = Math.PI / 2;
  disc.castShadow = true;
  coinGroup.add(disc);

  const rimGeom = new THREE.TorusGeometry(0.68, 0.055, 12, 32);
  const rim = new THREE.Mesh(rimGeom, edgeMat);
  coinGroup.add(rim);

  coinGroup.position.set(x, y, z);
  coinGroup.userData = { baseY: y, active: true };
  scene.add(coinGroup);
  coins.push(coinGroup);
}

// 10 Bitcoins guiando desde la tubería verde, subiendo la colina y cruzando el puente hasta las puertas del castillo
const COIN_PATH = [
  [-13.0, 38.0], [-10.8, 30.0], [-8.0, 22.0], [-4.5, 14.0], [-1.5, 6.5],
  [0.0, 0.5], [0.0, -6.0], [0.0, -12.5], [0.0, -19.0], [0.0, -25.5]
];
function placeBitcoinsOnPath() {
  const totalEl = document.getElementById('coin-total');
  const finalTotalEl = document.getElementById('final-coins-total');
  if (totalEl) totalEl.innerText = COIN_PATH.length;
  if (finalTotalEl) finalTotalEl.innerText = COIN_PATH.length;
  COIN_PATH.forEach(([x, z]) => {
    const gy = sampleGround(x, z, 10.2);
    if (gy > -900) createBitcoin(x, gy + 1.15, z);
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
const SCENE_DOOR_OPENING = 65;
const SCENE_VICTORY = 7;

let currentScene = SCENE_1_TITLE;
let scene2EnterTime = 0;
let gameplayStartTime = 0;
let doorAnimElapsed = 0;
let doorAnimStartTime = 0;

// Audio auténtico renderizado desde la ROM original de Super Mario 64 del usuario
const bgmCastleGrounds = new Audio('assets/audio/sm64/castle_grounds_bgm.mp3');
bgmCastleGrounds.loop = true;
bgmCastleGrounds.volume = 0.42;

const sfxCoin = new Audio('assets/audio/sm64/coin.mp3');
sfxCoin.volume = 0.65;

const sfxDoorOpen = new Audio('assets/audio/sm64/door_open.mp3');
sfxDoorOpen.volume = 0.80;

const sfxHereWeGo = new Audio('assets/audio/sm64/mario_0C.mp3');
sfxHereWeGo.volume = 0.85;

const sfxStarFanfare = new Audio('assets/audio/sm64/star_fanfare.mp3');
sfxStarFanfare.volume = 0.72;

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
const signDialogEl = document.getElementById('sign-dialog');
const signDialogTitleEl = signDialogEl ? signDialogEl.querySelector('.sign-dialog-title') : null;
const signDialogTextEl = document.getElementById('sign-dialog-text');
const victoryModal = document.getElementById('victory-modal');
const btnRestart = document.getElementById('btn-restart');
const coinCountEl = document.getElementById('coin-count');
const finalCoinsEl = document.getElementById('final-coins');
const finalTimeEl = document.getElementById('final-time');

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
  sfxHereWeGo.currentTime = 0;
  sfxHereWeGo.play().catch(() => audio.playLetsGoChime());
  bgmCastleGrounds.currentTime = 0;
  bgmCastleGrounds.play().catch(() => {});

  currentScene = SCENE_6_GAMEPLAY;
  gameplayStartTime = performance.now();
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

// Devuelve true si hay una pared o tronco de árbol en la dirección dada
function wallAhead(dx, dz) {
  const len = Math.hypot(dx, dz);
  if (len < 1e-6) return false;
  const nx = player.position.x + dx;
  const nz = player.position.z + dz;
  for (const tr of treeTrunks) {
    if (Math.abs(player.position.y - tr.y) < 6.5 && Math.hypot(nx - tr.x, nz - tr.z) < tr.r + PLAYER_RADIUS) {
      return true;
    }
  }
  _wallDir.set(dx / len, 0, dz / len);
  for (const h of [STEP_HEIGHT + 0.1, 1.4]) {
    _wallOrigin.set(player.position.x, player.position.y + h, player.position.z);
    wallRay.set(_wallOrigin, _wallDir);
    wallRay.far = len + PLAYER_RADIUS;
    const hits = wallRay.intersectObjects(collisionMeshes, false);
    if (hits.length && hits[0].face) {
      _worldNormal.copy(hits[0].face.normal).transformDirection(hits[0].object.matrixWorld);
      if (Math.abs(_worldNormal.y) < 0.55) return true;
    }
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
  const dbgPos = new URLSearchParams(window.location.search).get('pos');
  if (dbgPos) {
    const [px, py, pz] = dbgPos.split(',').map(Number);
    player.position.set(px, py, pz);
  } else {
    player.position.set(CASTLE_SPAWN.x, CASTLE_SPAWN.y + 0.2, CASTLE_SPAWN.z - 3.2);
  }
  player.rotation.y = Math.PI;
  velocityY = 0;
  isGrounded = false;
  cameraAngle = 0;
}

// Voces originales de salto de SM64 (Wah!, Hoo!, Yah!, Hoo-hoo!, Yahoo!)
const jumpVoices = [
  'assets/audio/sm64/mario_yah.mp3',
  'assets/audio/sm64/mario_01.mp3',
  'assets/audio/sm64/mario_00.mp3',
  'assets/audio/sm64/mario_hoohoo.mp3',
  'assets/audio/sm64/mario_04.mp3'
].map((src) => {
  const a = new Audio(src);
  a.volume = 0.72;
  return a;
});
let jumpVoiceIdx = 0;
function playMarioVoice() {
  if (bgmCastleGrounds.paused && currentScene === SCENE_6_GAMEPLAY) {
    bgmCastleGrounds.play().catch(() => {});
  }
  const a = jumpVoices[jumpVoiceIdx++ % jumpVoices.length];
  a.currentTime = 0;
  a.play().catch(() => audio.playJump());
}

function playCoinSound() {
  const c = sfxCoin.cloneNode();
  c.volume = 0.65;
  c.play().catch(() => audio.playCoin());
}

function formatElapsedTime(ms) {
  const totalSec = Math.max(0, Math.floor(ms / 1000));
  const mins = String(Math.floor(totalSec / 60)).padStart(2, '0');
  const secs = String(totalSec % 60).padStart(2, '0');
  return `${mins}:${secs}`;
}

function animateLimbs(swing) {
  const l = player.userData.limbs;
  if (!l || !l.LegL) return;
  const k = isGrounded ? 1 : 0.2;
  l.LegL.rotation.z = THREE.MathUtils.lerp(l.LegL.rotation.z, swing * k, 0.4);
  l.LegR.rotation.z = THREE.MathUtils.lerp(l.LegR.rotation.z, -swing * k, 0.4);
  l.ArmL.rotation.z = THREE.MathUtils.lerp(l.ArmL.rotation.z, -swing * 0.8 * k, 0.4);
  l.ArmR.rotation.z = THREE.MathUtils.lerp(l.ArmR.rotation.z, swing * 0.8 * k, 0.4);
}

function updateSignpostDialog() {
  if (!signDialogEl || currentScene !== SCENE_6_GAMEPLAY) {
    if (signDialogEl) signDialogEl.classList.add('hidden');
    return;
  }
  let nearest = null;
  let bestDist = 3.8;
  for (const s of signposts) {
    const d = Math.hypot(player.position.x - s.x, player.position.z - s.z);
    if (d < bestDist && Math.abs(player.position.y - s.y) < 2.8) {
      bestDist = d;
      nearest = s;
    }
  }
  if (nearest) {
    if (signDialogTitleEl) signDialogTitleEl.innerText = nearest.title;
    if (signDialogTextEl) signDialogTextEl.innerText = nearest.text;
    signDialogEl.classList.remove('hidden');
  } else {
    signDialogEl.classList.add('hidden');
  }
}

function updatePhysics(delta) {
  if (currentScene === SCENE_DOOR_OPENING) {
    doorAnimElapsed = (Date.now() - doorAnimStartTime) / 1000;
    const openT = Math.min(1, doorAnimElapsed / 1.15);
    const eased = 1 - Math.pow(1 - openT, 3);
    // Las dos hojas estelares se abren hacia el pórtico (+Z) como en Super Mario 64
    doorLeftPivot.rotation.y = -eased * 1.62;
    doorRightPivot.rotation.y = eased * 1.62;

    if (doorAnimElapsed < 0.45) {
      const standT = Math.min(1, doorAnimElapsed / 0.45);
      player.position.x = THREE.MathUtils.lerp(player.position.x, 0, standT);
      player.position.z = THREE.MathUtils.lerp(player.position.z, -29.2, standT);
      player.rotation.y = Math.PI;
      animateLimbs(0);
    } else {
      const walkT = Math.min(1, (doorAnimElapsed - 0.45) / 1.30);
      player.position.x = THREE.MathUtils.lerp(player.position.x, 0, 0.35);
      player.position.z = THREE.MathUtils.lerp(-29.2, -31.85, walkT);
      player.rotation.y = Math.PI;
      const wc = (doorAnimElapsed - 0.45) * 11;
      animateLimbs(Math.sin(wc) * 0.85);
      if (player.userData.blenderModel) {
        player.userData.blenderModel.position.y = Math.abs(Math.sin(wc * 2)) * 0.1;
      }
    }
    player.userData.dropShadow.position.set(player.position.x, 8.06, player.position.z);

    if (doorAnimElapsed >= 1.75) {
      triggerVictory();
    }
    return;
  }

  if (currentScene !== SCENE_6_GAMEPLAY || !castleLoaded) return;

  let moveX = 0;
  let moveZ = 0;

  if (keys['KeyW'] || keys['ArrowUp']) moveZ -= 1;
  if (keys['KeyS'] || keys['ArrowDown']) moveZ += 1;
  if (keys['KeyA'] || keys['ArrowLeft']) moveX -= 1;
  if (keys['KeyD'] || keys['ArrowRight']) moveX += 1;

  const isMoving = moveX !== 0 || moveZ !== 0;

  if (isMoving) {
    if (bgmCastleGrounds.paused) {
      bgmCastleGrounds.play().catch(() => {});
    }
    const moveVector = new THREE.Vector3(moveX, 0, moveZ).normalize();
    moveVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraAngle);

    moveWithCollision(moveVector.x * SPEED * delta, moveVector.z * SPEED * delta);

    const targetRotation = Math.atan2(moveVector.x, moveVector.z);
    player.rotation.y = THREE.MathUtils.lerp(player.rotation.y, targetRotation, 14 * delta);

    walkCycle += delta * 12;
    animateLimbs(Math.sin(walkCycle) * 0.9);
    if (player.userData.blenderModel) {
      player.userData.blenderModel.position.y = Math.abs(Math.sin(walkCycle * 2)) * 0.12;
      player.userData.blenderModel.rotation.z = Math.sin(walkCycle) * 0.05;
    }
  } else {
    animateLimbs(0);
    if (player.userData.blenderModel) {
      player.userData.blenderModel.position.y = THREE.MathUtils.lerp(player.userData.blenderModel.position.y, 0, 10 * delta);
      player.userData.blenderModel.rotation.z = THREE.MathUtils.lerp(player.userData.blenderModel.rotation.z, 0, 10 * delta);
    }
  }

  // Salto y Gravedad
  if (keys['Space'] && isGrounded) {
    velocityY = JUMP_FORCE;
    isGrounded = false;
    playMarioVoice();
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

  updateSignpostDialog();

  // Recolección de Bitcoins
  coins.forEach((coin) => {
    if (!coin.userData.active) return;
    const dist = player.position.distanceTo(coin.position);
    if (dist < 1.45) {
      coin.userData.active = false;
      scene.remove(coin);
      collectedCoins++;
      coinCountEl.innerText = collectedCoins;
      playCoinSound();
    }
  });

  // Llegada a las Puertas Dobles Estelares de Peach's Castle (Z = -31.55, Y = 8.03)
  if (castleLoaded && currentScene === SCENE_6_GAMEPLAY &&
      Math.abs(player.position.x) < 2.25 && player.position.z < -28.8 && player.position.z > -32.2 &&
      player.position.y > 7.2) {
    startDoorOpeningSequence();
  }
}

function startDoorOpeningSequence() {
  if (currentScene !== SCENE_6_GAMEPLAY || !castleLoaded) return;
  currentScene = SCENE_DOOR_OPENING;
  doorAnimElapsed = 0;
  doorAnimStartTime = Date.now();
  const doorTimer = setInterval(() => {
    if (currentScene !== SCENE_DOOR_OPENING) {
      clearInterval(doorTimer);
      return;
    }
    updatePhysics(0.05);
    updateCamera(0.05);
    renderer.render(scene, camera);
  }, 50);
  coins.forEach((c) => {
    if (c.userData.active && c.position.z < -21.5) c.visible = false;
  });
  if (signDialogEl) signDialogEl.classList.add('hidden');
  controlsHint.classList.add('hidden');
  bgmCastleGrounds.pause();

  sfxDoorOpen.currentTime = 0;
  sfxDoorOpen.play().catch(() => {});
}

function triggerVictory() {
  if (currentScene === SCENE_VICTORY) return;
  currentScene = SCENE_VICTORY;
  star.userData.active = false;
  bgmCastleGrounds.pause();

  sfxHereWeGo.currentTime = 0;
  sfxHereWeGo.play().catch(() => {});
  sfxStarFanfare.currentTime = 0;
  sfxStarFanfare.play().catch(() => audio.playVictory());

  animateLimbs(0);
  const elapsedMs = gameplayStartTime > 0 ? (performance.now() - gameplayStartTime) : 0;
  finalCoinsEl.innerText = collectedCoins;
  if (finalTimeEl) finalTimeEl.innerText = formatElapsedTime(elapsedMs);
  setTimeout(() => {
    victoryModal.classList.add('active');
  }, 850);
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

  // Cámara cinemática frente al pórtico real al abrir las puertas del castillo
  if (currentScene === SCENE_DOOR_OPENING || currentScene === SCENE_VICTORY) {
    const camAlpha = Math.min(1, Math.max(6 * delta, 0.35));
    camera.position.x = THREE.MathUtils.lerp(camera.position.x, 0, camAlpha);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, 10.1, camAlpha);
    camera.position.z = THREE.MathUtils.lerp(camera.position.z, -23.2, camAlpha);
    camera.lookAt(0, 9.3, -31.55);
  } else {
    // Escena 6: Cámara de Gameplay en 3ª persona
    const cameraDistance = 8.5;
    const cameraHeight = 4.0;

    const targetX = player.position.x + Math.sin(cameraAngle) * cameraDistance;
    const targetZ = player.position.z + Math.cos(cameraAngle) * cameraDistance;
    const targetY = player.position.y + cameraHeight;

    camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetX, 8 * delta);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetY, 8 * delta);
    camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZ, 8 * delta);

    camera.lookAt(player.position.x, player.position.y + 1.5, player.position.z);
  }

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
  const t = clock.elapsedTime;

  if (currentScene >= SCENE_6_GAMEPLAY) {
    coins.forEach((coin) => {
      if (coin.userData.active) {
        coin.rotation.y += delta * 2.5;
        coin.position.y = coin.userData.baseY + Math.sin(t * 3) * 0.15;
      }
    });

    // Animación continua de cascada, agua del foso y banderas de las torres
    waterfallTex.offset.y -= delta * 1.35;
    moatWater.tex.offset.x += delta * 0.06;
    moatWater.tex.offset.y += delta * 0.04;
    lakeWater.tex.offset.x -= delta * 0.05;

    castleFlags.forEach((cloth) => {
      const posAttr = cloth.geometry.attributes.position;
      const base = cloth.userData.basePos;
      const ph = cloth.userData.phase;
      for (let i = 0; i < posAttr.count; i++) {
        const bx = base[i * 3];
        const amp = (bx / 3.6) * 0.42;
        posAttr.array[i * 3 + 2] = Math.sin(t * 5.2 - bx * 1.6 + ph) * amp;
      }
      posAttr.needsUpdate = true;
    });
  }

  updatePhysics(delta);
  updateCamera(delta);

  // Billboard en eje Y para los 26 árboles oficiales (fiel a GEO_BILLBOARD de SM64)
  if (currentScene >= SCENE_6_GAMEPLAY) {
    for (const tg of castleTrees) {
      tg.rotation.y = Math.atan2(camera.position.x - tg.position.x, camera.position.z - tg.position.z);
    }
  }

  if (skyDome.visible) skyDome.position.set(camera.position.x, camera.position.y + 6, camera.position.z);

  renderer.render(scene, camera);
}

animate();
