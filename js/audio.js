/**
 * Procedural Paper Page-Turn Audio Synthesizer
 * Uses Web Audio API to create authentic, subtle paper rustle without external files.
 */
class PageAudio {
  constructor() {
    this.ctx = null;
    this.muted = false;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playPageTurn() {
    if (this.muted) return;
    try {
      this.init();
      if (!this.ctx) return;

      const now = this.ctx.currentTime;

      // 1. Noise buffer to simulate the friction of turning paper
      const bufferSize = this.ctx.sampleRate * 0.28; // ~280ms
      const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        output[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.45));
      }

      const whiteNoise = this.ctx.createBufferSource();
      whiteNoise.buffer = noiseBuffer;

      // 2. Bandpass filter to sculpt the frequency into a crisp parchment rustle
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1400, now);
      filter.frequency.exponentialRampToValueAtTime(800, now + 0.25);
      filter.Q.setValueAtTime(2.2, now);

      // 3. Gain envelope for gentle entry and whispery taper
      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(0.18, now + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.27);

      whiteNoise.connect(filter);
      filter.connect(gain);
      gain.connect(this.ctx.destination);

      whiteNoise.start(now);
      whiteNoise.stop(now + 0.28);
    } catch (e) {
      // Audio autoplay policy or browser restriction
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }
}

window.pageAudio = new PageAudio();
