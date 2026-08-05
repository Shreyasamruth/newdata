document.addEventListener('DOMContentLoaded', () => {
  
  // ====================================================================
  // 1. THREE.JS VIBRANT 3D GRAPHICS SCENE (3D SHIELD, RINGS & GEOMETRY)
  // ====================================================================
  const canvas = document.getElementById('canvas3d');
  if (canvas && typeof THREE !== 'undefined') {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x0052ff, 3, 50);
    pointLight1.position.set(5, 5, 5);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x00b4d8, 3, 50);
    pointLight2.position.set(-5, -5, 5);
    scene.add(pointLight2);

    // Central 3D Security Shield Core
    const coreGroup = new THREE.Group();

    const innerGeo = new THREE.IcosahedronGeometry(1.6, 2);
    const innerMat = new THREE.MeshPhongMaterial({
      color: 0x0052ff,
      emissive: 0x0022aa,
      shininess: 90,
      transparent: true,
      opacity: 0.7,
      wireframe: false
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    coreGroup.add(innerMesh);

    const outerGeo = new THREE.IcosahedronGeometry(2.1, 1);
    const outerMat = new THREE.MeshBasicMaterial({
      color: 0x00b4d8,
      wireframe: true,
      transparent: true,
      opacity: 0.4
    });
    const outerMesh = new THREE.Mesh(outerGeo, outerMat);
    coreGroup.add(outerMesh);

    // 3D Rotating Encryption Rings
    const ring1Geo = new THREE.TorusGeometry(3.2, 0.04, 16, 100);
    const ring1Mat = new THREE.MeshPhongMaterial({
      color: 0x0066ff,
      emissive: 0x0044cc,
      shininess: 100
    });
    const ring1Mesh = new THREE.Mesh(ring1Geo, ring1Mat);
    ring1Mesh.rotation.x = Math.PI / 3;
    coreGroup.add(ring1Mesh);

    const ring2Geo = new THREE.TorusGeometry(4.0, 0.03, 16, 100);
    const ring2Mat = new THREE.MeshPhongMaterial({
      color: 0x4338ca,
      emissive: 0x2211aa,
      shininess: 100
    });
    const ring2Mesh = new THREE.Mesh(ring2Geo, ring2Mat);
    ring2Mesh.rotation.y = Math.PI / 4;
    coreGroup.add(ring2Mesh);

    scene.add(coreGroup);

    // Orbiting 3D Security Floating Geometry Nodes
    const floatingNodes = [];
    const nodeCount = 24;

    for (let i = 0; i < nodeCount; i++) {
      const geoType = i % 2 === 0 ? new THREE.OctahedronGeometry(0.25) : new THREE.TetrahedronGeometry(0.3);
      const nodeMat = new THREE.MeshPhongMaterial({
        color: i % 3 === 0 ? 0x0052ff : (i % 3 === 1 ? 0x00b4d8 : 0x4338ca),
        emissive: 0x001166,
        shininess: 80,
        flatShading: true
      });
      const nodeMesh = new THREE.Mesh(geoType, nodeMat);

      const radius = 5 + Math.random() * 5;
      const theta = Math.random() * Math.PI * 2;
      const phi = (Math.random() - 0.5) * Math.PI;

      nodeMesh.position.set(
        radius * Math.cos(theta) * Math.cos(phi),
        radius * Math.sin(phi),
        radius * Math.sin(theta) * Math.cos(phi)
      );

      nodeMesh.userData = {
        orbitRadius: radius,
        speed: (Math.random() * 0.008 + 0.003) * (i % 2 === 0 ? 1 : -1),
        theta: theta,
        phi: phi,
        rotSpeedX: Math.random() * 0.02,
        rotSpeedY: Math.random() * 0.02
      };

      floatingNodes.push(nodeMesh);
      scene.add(nodeMesh);
    }

    // Background 3D Laser Starfield Particle Cloud
    const particleCount = 400;
    const posArray = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i++) {
      posArray[i] = (Math.random() - 0.5) * 25;
    }

    const particlesGeo = new THREE.BufferGeometry();
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMat = new THREE.PointsMaterial({
      size: 0.06,
      color: 0x0066ff,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });

    const particleMesh = new THREE.Points(particlesGeo, particlesMat);
    scene.add(particleMesh);

    camera.position.z = 8;

    // Interactive Mouse Tracking
    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = (e.clientX - window.innerWidth / 2) * 0.0005;
      mouseY = (e.clientY - window.innerHeight / 2) * 0.0005;
    });

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Render Loop
    const animate3D = () => {
      requestAnimationFrame(animate3D);

      coreGroup.rotation.y += 0.004;
      coreGroup.rotation.x += 0.002;
      ring1Mesh.rotation.z += 0.003;
      ring2Mesh.rotation.z -= 0.002;
      particleMesh.rotation.y -= 0.0005;

      floatingNodes.forEach(node => {
        node.userData.theta += node.userData.speed;
        node.position.x = node.userData.orbitRadius * Math.cos(node.userData.theta) * Math.cos(node.userData.phi);
        node.position.z = node.userData.orbitRadius * Math.sin(node.userData.theta) * Math.cos(node.userData.phi);
        
        node.rotation.x += node.userData.rotSpeedX;
        node.rotation.y += node.userData.rotSpeedY;
      });

      camera.position.x += (mouseX * 8 - camera.position.x) * 0.05;
      camera.position.y += (-mouseY * 8 - camera.position.y) * 0.05;
      camera.lookAt(scene.position);

      renderer.render(scene, camera);
    };

    animate3D();
  }

  // ==========================================
  // 2. 3D CARD TILT PARALLAX EFFECT
  // ==========================================
  const cards = document.querySelectorAll('.glass-card-techie');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -6;
      const rotateY = ((x - centerX) / centerX) * 6;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(8px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)`;
    });
  });

  // =========================================================
  // 3. ADVANCED VOICE CLASSIFIER (CASE, SYMBOLS & DIGITS)
  // =========================================================
  function parseVoicePassword(rawText) {
    if (!rawText) return '';
    
    // 1. Pre-clean: strip automatic browser speech punctuation
    let text = rawText.trim().replace(/,/g, ' ').replace(/\./g, ' ').replace(/["']/g, '');

    // 2. Handle Case Modifiers (e.g. 'capital p' -> 'P', 'uppercase a' -> 'A', 'lowercase b' -> 'b')
    text = text.replace(/\b(?:capital|uppercase)\s+([a-z])\b/gi, (match, char) => char.toUpperCase());
    text = text.replace(/\b(?:lowercase)\s+([a-z])\b/gi, (match, char) => char.toLowerCase());

    // 3. Multi-word & Compound Symbol Mappings
    const symbolPhrases = [
      { pattern: /\bat\s*rate\b|\bat\s*sign\b|\bat\s*symbol\b|\batrate\b/gi, replace: '@' },
      { pattern: /\bexclamation\s*mark\b|\bexclamation\s*point\b|\bexclamation\s*sign\b|\bexclamationmark\b/gi, replace: '!' },
      { pattern: /\bquestion\s*mark\b|\bquestion\s*sign\b|\bquestionmark\b/gi, replace: '?' },
      { pattern: /\bdollar\s*sign\b|\bdollars\s*sign\b|\bdollarsign\b/gi, replace: '$' },
      { pattern: /\bpercent\s*sign\b|\bpercentage\s*sign\b|\bpercentsign\b/gi, replace: '%' },
      { pattern: /\bnumber\s*sign\b|\bpound\s*sign\b|\bhash\s*tag\b|\bhash\s*mark\b|\bhashtag\b|\bhashmark\b/gi, replace: '#' },
      { pattern: /\band\s*sign\b|\bampersand\s*sign\b|\bampersandsign\b/gi, replace: '&' },
      { pattern: /\bstar\s*sign\b|\basterisk\s*sign\b|\bstar\s*mark\b|\bstarsign\b|\basterisksign\b/gi, replace: '*' },
      { pattern: /\bunder\s*score\b|\bunder\s*line\b|\bunderscore\b|\bunderline\b/gi, replace: '_' },
      { pattern: /\bminus\s*sign\b|\bdash\s*sign\b|\bhyphen\s*sign\b|\bminussign\b|\bdashsign\b/gi, replace: '-' },
      { pattern: /\bplus\s*sign\b|\bplussign\b/gi, replace: '+' },
      { pattern: /\bequal\s*sign\b|\bequals\s*to\b|\bequalsign\b|\bequalsto\b/gi, replace: '=' },
      { pattern: /\bfull\s*stop\b|\bdot\s*sign\b|\bfullstop\b|\bdotsign\b/gi, replace: '.' },
      { pattern: /\bforward\s*slash\b|\bforwardslash\b/gi, replace: '/' },
      { pattern: /\bback\s*slash\b|\bbackslash\b/gi, replace: '\\' }
    ];

    symbolPhrases.forEach(item => {
      text = text.replace(item.pattern, item.replace);
    });

    // 4. Single-word Symbol Mappings
    const singleSymbols = [
      { pattern: /\bat\b/gi, replace: '@' },
      { pattern: /\bhash\b/gi, replace: '#' },
      { pattern: /\bdollar\b|\bdollars\b/gi, replace: '$' },
      { pattern: /\bpercent\b/gi, replace: '%' },
      { pattern: /\bampersand\b/gi, replace: '&' },
      { pattern: /\bstar\b|\basterisk\b/gi, replace: '*' },
      { pattern: /\bexclamation\b/gi, replace: '!' },
      { pattern: /\bquestion\b/gi, replace: '?' },
      { pattern: /\bdash\b|\bhyphen\b|\bminus\b/gi, replace: '-' },
      { pattern: /\bplus\b/gi, replace: '+' },
      { pattern: /\bequals\b/gi, replace: '=' },
      { pattern: /\bdot\b|\bperiod\b/gi, replace: '.' },
      { pattern: /\bslash\b/gi, replace: '/' }
    ];

    singleSymbols.forEach(item => {
      text = text.replace(item.pattern, item.replace);
    });

    // 5. Spoken Numbers Mapping
    const numberWords = {
      'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
      'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
      'ten': '10', 'eleven': '11', 'twelve': '12'
    };

    for (let word in numberWords) {
      const reg = new RegExp(`\\b${word}\\b`, 'gi');
      text = text.replace(reg, numberWords[word]);
    }

    // 6. Clean all spaces
    return text.replace(/\s+/g, '');
  }

  // ==========================================
  // 4. DASHBOARD FUNCTIONALITY & API LOGIC
  // ==========================================
  const passwordInput = document.getElementById('passwordInput');
  const toggleVisibilityBtn = document.getElementById('toggleVisibilityBtn');
  const voiceInputBtn = document.getElementById('voiceInputBtn');
  const strengthMeterFill = document.getElementById('strengthMeterFill');
  const strengthText = document.getElementById('strengthText');
  const healthScoreVal = document.getElementById('healthScoreVal');
  const entropyVal = document.getElementById('entropyVal');
  const mlLabelVal = document.getElementById('mlLabelVal');
  
  const crackOnline = document.getElementById('crackOnline');
  const crackFast = document.getElementById('crackFast');
  const crackSlow = document.getElementById('crackSlow');
  const crackGpu = document.getElementById('crackGpu');
  
  const recommendationsList = document.getElementById('recommendationsList');
  const exportPdfBtn = document.getElementById('exportPdfBtn');

  // Generator Elements
  const genCategory = document.getElementById('genCategory');
  const genLength = document.getElementById('genLength');
  const genLengthVal = document.getElementById('genLengthVal');
  const generatedResult = document.getElementById('generatedResult');
  const generateBtn = document.getElementById('generateBtn');
  const copyGenBtn = document.getElementById('copyGenBtn');

  let currentAnalysisData = null;
  let chartInstance = null;

  // Initialize Doughnut Chart
  const featChartCanvas = document.getElementById('featureChart');
  if (featChartCanvas) {
    const ctx = featChartCanvas.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Uppercase', 'Lowercase', 'Digits', 'Symbols'],
        datasets: [{
          data: [0, 0, 0, 0],
          backgroundColor: ['#0052ff', '#00b4d8', '#f59e0b', '#ef4444'],
          borderWidth: 3,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: '#334155', font: { family: 'Outfit', size: 12, weight: 600 } } }
        }
      }
    });
  }

  // Debounced input handler for real-time analysis
  let debounceTimer = null;
  passwordInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(analyzeCurrentPassword, 200);
  });

  async function analyzeCurrentPassword() {
    const password = passwordInput.value;
    if (!password) {
      resetDashboard();
      return;
    }

    try {
      const res = await fetch('/api/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });

      if (!res.ok) return;

      const data = await res.json();
      currentAnalysisData = data;
      updateDashboardUI(data);

    } catch (err) {
      console.error("Analysis request failed:", err);
    }
  }

  function updateDashboardUI(data) {
    const score = data.health_score.score;
    const color = data.health_score.color;
    const cat = data.health_score.category;

    // 1. Strength Meter Bar
    strengthMeterFill.style.width = `${score}%`;
    strengthMeterFill.style.backgroundColor = color;
    strengthText.innerText = `${cat} (${score}%)`;
    strengthText.style.color = color;

    // 2. Metrics
    healthScoreVal.innerText = `${score} / 100`;
    healthScoreVal.style.color = color;
    entropyVal.innerText = `${data.entropy_bits} bits`;
    mlLabelVal.innerText = data.ml_prediction.predicted_label;

    // 3. Crack Times
    crackOnline.innerText = data.crack_times.online_attack;
    crackFast.innerText = data.crack_times.fast_hash;
    crackSlow.innerText = data.crack_times.slow_hash;
    crackGpu.innerText = data.crack_times.gpu_cluster;

    // 4. Feature Chart Update
    if (chartInstance) {
      const feat = data.features;
      chartInstance.data.datasets[0].data = [
        feat.num_uppercase,
        feat.num_lowercase,
        feat.num_digits,
        feat.num_symbols
      ];
      chartInstance.update();
    }

    // 5. Recommendations List
    recommendationsList.innerHTML = '';
    if (data.recommendations && data.recommendations.length > 0) {
      data.recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'rec-item-techie';
        div.innerText = rec;
        recommendationsList.appendChild(div);
      });
    }
  }

  function resetDashboard() {
    strengthMeterFill.style.width = '0%';
    strengthText.innerText = 'Weak';
    strengthText.style.color = 'var(--tech-red)';
    healthScoreVal.innerText = '0 / 100';
    entropyVal.innerText = '0 bits';
    mlLabelVal.innerText = '-';
    
    crackOnline.innerText = 'Instant';
    crackFast.innerText = 'Instant';
    crackSlow.innerText = 'Instant';
    crackGpu.innerText = 'Instant';

    if (chartInstance) {
      chartInstance.data.datasets[0].data = [0, 0, 0, 0];
      chartInstance.update();
    }

    recommendationsList.innerHTML = '<div class="rec-item-techie">Enter a password above to execute real-time security defect audit.</div>';
    currentAnalysisData = null;
  }

  // Toggle Visibility Button
  toggleVisibilityBtn.addEventListener('click', () => {
    const isPass = passwordInput.type === 'password';
    passwordInput.type = isPass ? 'text' : 'password';
    toggleVisibilityBtn.innerHTML = isPass ? '<i class="fa-solid fa-eye-slash"></i>' : '<i class="fa-solid fa-eye"></i>';
  });

  // =============================================================
  // ADVANCED SPEECH RECOGNITION (VOICE CLASSIFIER INTEGRATED)
  // =============================================================
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.lang = 'en-US';

    let isListening = false;

    voiceInputBtn.addEventListener('click', () => {
      if (isListening) {
        recognition.stop();
        return;
      }

      try {
        recognition.start();
        isListening = true;
        voiceInputBtn.style.color = '#ef4444';
        voiceInputBtn.title = 'Listening... Speak your password clearly';
        passwordInput.placeholder = 'Listening... Speak password (e.g. "capital P a s s w o r d at rate 1 2 3")...';
      } catch (e) {
        console.error("Could not start recognition:", e);
      }
    });

    recognition.onstart = () => {
      isListening = true;
      voiceInputBtn.style.color = '#ef4444';
    };

    recognition.onresult = (event) => {
      isListening = false;
      voiceInputBtn.style.color = '';
      voiceInputBtn.title = 'Voice Input (Speech-to-Text)';
      passwordInput.placeholder = 'Enter password to inspect...';

      if (!event.results || !event.results[0] || !event.results[0][0]) return;

      const rawTranscript = event.results[0][0].transcript;
      console.log('Voice Raw Transcript:', rawTranscript);

      const parsedPassword = parseVoicePassword(rawTranscript);
      console.log('Voice Classified Password:', parsedPassword);

      if (parsedPassword) {
        passwordInput.value = parsedPassword;
        analyzeCurrentPassword();
      }
    };

    recognition.onerror = (event) => {
      isListening = false;
      voiceInputBtn.style.color = '';
      voiceInputBtn.title = 'Voice Input (Speech-to-Text)';
      passwordInput.placeholder = 'Enter password to inspect...';
      
      console.warn('Speech recognition error event:', event.error);
      if (event.error === 'not-allowed') {
        alert('Microphone Access Denied!\n\nPlease allow microphone permissions in your browser address bar to use voice input.');
      }
    };

    recognition.onend = () => {
      isListening = false;
      voiceInputBtn.style.color = '';
      voiceInputBtn.title = 'Voice Input (Speech-to-Text)';
      passwordInput.placeholder = 'Enter password to inspect...';
    };
  } else {
    voiceInputBtn.addEventListener('click', () => {
      alert('Speech Recognition is not supported by your browser.\n\nPlease use Google Chrome or Microsoft Edge for voice input.');
    });
  }

  // AI Password Generator Handlers
  genLength.addEventListener('input', () => {
    genLengthVal.innerText = genLength.value;
  });

  generateBtn.addEventListener('click', async () => {
    const category = genCategory.value;
    const length = parseInt(genLength.value);

    try {
      const res = await fetch('/api/v1/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, length })
      });

      if (!res.ok) return;

      const data = await res.json();
      generatedResult.value = data.generated_password;

      // Automatically inspect the generated password in analyzer
      passwordInput.value = data.generated_password;
      analyzeCurrentPassword();

    } catch (err) {
      console.error("Generator request failed:", err);
    }
  });

  copyGenBtn.addEventListener('click', () => {
    if (!generatedResult.value) return;
    navigator.clipboard.writeText(generatedResult.value);
    copyGenBtn.innerHTML = '<i class="fa-solid fa-check text-success"></i>';
    setTimeout(() => {
      copyGenBtn.innerHTML = '<i class="fa-solid fa-copy"></i>';
    }, 1500);
  });

  // PDF Export Trigger
  exportPdfBtn.addEventListener('click', async () => {
    if (!currentAnalysisData) {
      alert("Please enter a password to analyze before exporting PDF report.");
      return;
    }

    try {
      const res = await fetch('/api/v1/export-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentAnalysisData)
      });

      if (!res.ok) return;

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Security_Audit_Report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error("Export PDF failed:", err);
    }
  });
});
