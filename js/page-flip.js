/**
 * Enhanced 3D Page-Turn and Swipe Engine
 * Handles touch gestures (tablet/phone swiping), click zones, keyboard shortcuts, and 3D curl physics.
 */
class PageFlipEngine {
  constructor(app) {
    this.app = app;
    this.isAnimating = false;
    this.touchStartX = 0;
    this.touchStartY = 0;
    this.touchEndX = 0;
    this.touchEndY = 0;
    this.minSwipeDistance = 40;

    this.initEvents();
  }

  initEvents() {
    const stage = document.getElementById('bookStage');
    const prevZone = document.getElementById('navPrev');
    const nextZone = document.getElementById('navNext');

    if (prevZone) prevZone.addEventListener('click', () => this.flipPrev());
    if (nextZone) nextZone.addEventListener('click', () => this.flipNext());

    // Keyboard controls
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        this.flipNext();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        this.flipPrev();
      } else if (e.key === 'Home') {
        e.preventDefault();
        this.app.goToSpread(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        this.app.goToSpread(this.app.totalSpreads - 1);
      }
    });

    // Touch events for tablets and mobile devices
    if (stage) {
      stage.addEventListener('touchstart', (e) => {
        this.touchStartX = e.changedTouches[0].screenX;
        this.touchStartY = e.changedTouches[0].screenY;
      }, { passive: true });

      stage.addEventListener('touchend', (e) => {
        this.touchEndX = e.changedTouches[0].screenX;
        this.touchEndY = e.changedTouches[0].screenY;
        this.handleGesture();
      }, { passive: true });
    }
  }

  handleGesture() {
    const deltaX = this.touchEndX - this.touchStartX;
    const deltaY = this.touchEndY - this.touchStartY;

    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) >= this.minSwipeDistance) {
      if (deltaX < 0) {
        this.flipNext();
      } else {
        this.flipPrev();
      }
    }
  }

  flipNext() {
    if (this.isAnimating) return;
    if (this.app.currentSpreadIndex >= this.app.totalSpreads - 1) return;

    this.isAnimating = true;
    if (window.pageAudio) window.pageAudio.playPageTurn();

    const flipLeaf = document.getElementById('pageFlipLeaf');
    if (flipLeaf) {
      flipLeaf.className = 'page-flip-leaf flipping-forward';
    }

    setTimeout(() => {
      this.app.goToSpread(this.app.currentSpreadIndex + 1);
      if (flipLeaf) {
        flipLeaf.className = 'page-flip-leaf';
      }
      this.isAnimating = false;
    }, 450);
  }

  flipPrev() {
    if (this.isAnimating) return;
    if (this.app.currentSpreadIndex <= 0) return;

    this.isAnimating = true;
    if (window.pageAudio) window.pageAudio.playPageTurn();

    const flipLeaf = document.getElementById('pageFlipLeaf');
    if (flipLeaf) {
      flipLeaf.className = 'page-flip-leaf flipping-backward';
    }

    setTimeout(() => {
      this.app.goToSpread(this.app.currentSpreadIndex - 1);
      if (flipLeaf) {
        flipLeaf.className = 'page-flip-leaf';
      }
      this.isAnimating = false;
    }, 450);
  }
}

window.PageFlipEngine = PageFlipEngine;
