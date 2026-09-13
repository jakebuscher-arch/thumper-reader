/**
 * Master Application Controller for the Thumper 5-Book Interactive Reader
 * Verbatim text, center-justified verses, no picture captions, illuminated fairy tale styling.
 */
class ThumperApp {
  constructor() {
    this.books = window.THUMPER_COLLECTION || [];
    this.spreads = [];
    this.currentSpreadIndex = 0;
    this.mobileView = 'text'; // 'text' or 'art' for mobile view

    this.initSpreads();
    this.initDOM();
    this.initFlipEngine();
    this.renderTOC();
    
    // Check URL hash first (e.g. #spread=15)
    const hash = window.location.hash;
    const match = hash.match(/spread=(\d+)/);
    if (match) {
      this.currentSpreadIndex = Math.min(Math.max(0, parseInt(match[1])), this.spreads.length - 1);
    } else {
      // Restore saved reading position
      const saved = localStorage.getItem('thumper_reading_spread');
      if (saved !== null && !isNaN(parseInt(saved))) {
        this.currentSpreadIndex = Math.min(Math.max(0, parseInt(saved)), this.spreads.length - 1);
      }
    }

    this.renderCurrentSpread();
  }

  initSpreads() {
    this.spreads = [];
    let spreadCount = 0;
    this.books.forEach((book) => {
      book.pages.forEach((page) => {
        spreadCount++;
        this.spreads.push({
          bookNumber: book.bookNumber,
          bookTitle: book.title,
          bookTheme: book.theme,
          bookSubtitle: book.subtitle,
          borderTheme: book.borderTheme,
          pageData: page,
          spreadNumber: spreadCount
        });
      });
    });
    this.totalSpreads = this.spreads.length;
  }

  initDOM() {
    this.bookContainer = document.getElementById('bookContainer');
    this.leftPageEl = document.getElementById('leftPage');
    this.rightPageEl = document.getElementById('rightPage');
    this.bookLabelEl = document.getElementById('currentBookLabel');
    this.pageIndicatorEl = document.getElementById('pageIndicator');
    this.progressSlider = document.getElementById('progressSlider');
    this.tocDrawer = document.getElementById('tocDrawer');
    this.tocOverlay = document.getElementById('tocOverlay');
    this.btnPrev = document.getElementById('btnPrev');
    this.btnNext = document.getElementById('btnNext');
    this.btnTOC = document.getElementById('btnTOC');
    this.btnCloseTOC = document.getElementById('btnCloseTOC');
    this.btnFullscreen = document.getElementById('btnFullscreen');
    this.btnMobileSwitch = document.getElementById('btnMobileSwitch');

    if (this.progressSlider) {
      this.progressSlider.min = 0;
      this.progressSlider.max = this.totalSpreads - 1;
      this.progressSlider.addEventListener('input', (e) => {
        this.goToSpread(parseInt(e.target.value));
      });
    }

    if (this.btnPrev) this.btnPrev.addEventListener('click', () => this.flipEngine.flipPrev());
    if (this.btnNext) this.btnNext.addEventListener('click', () => this.flipEngine.flipNext());

    if (this.btnTOC) this.btnTOC.addEventListener('click', () => this.openTOC());
    if (this.btnCloseTOC) this.btnCloseTOC.addEventListener('click', () => this.closeTOC());
    if (this.tocOverlay) this.tocOverlay.addEventListener('click', () => this.closeTOC());

    if (this.btnFullscreen) {
      this.btnFullscreen.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
          this.btnFullscreen.innerHTML = '⤓ Normal';
        } else {
          document.exitFullscreen().catch(() => {});
          this.btnFullscreen.innerHTML = '⛶ Fullscreen';
        }
      });
    }

    if (this.btnMobileSwitch) {
      this.btnMobileSwitch.addEventListener('click', () => {
        this.toggleMobileView();
      });
    }

    window.addEventListener('hashchange', () => {
      const match = window.location.hash.match(/spread=(\d+)/);
      if (match) {
        this.goToSpread(parseInt(match[1]));
      }
    });
  }

  initFlipEngine() {
    this.flipEngine = new window.PageFlipEngine(this);
  }

  toggleMobileView() {
    if (this.mobileView === 'text') {
      this.mobileView = 'art';
      this.bookContainer.classList.remove('show-text');
      this.bookContainer.classList.add('show-art');
      this.btnMobileSwitch.innerHTML = '📜 View Words';
    } else {
      this.mobileView = 'text';
      this.bookContainer.classList.remove('show-art');
      this.bookContainer.classList.add('show-text');
      this.btnMobileSwitch.innerHTML = '🖼️ View Art';
    }
  }

  goToSpread(index) {
    if (index < 0 || index >= this.totalSpreads) return;
    this.currentSpreadIndex = index;
    localStorage.setItem('thumper_reading_spread', index);
    window.location.hash = `spread=${index}`;
    this.renderCurrentSpread();
  }

  renderCurrentSpread() {
    const spread = this.spreads[this.currentSpreadIndex];
    if (!spread) return;

    const page = spread.pageData;
    const bnum = spread.bookNumber;

    // Update Top & Bottom Toolbar Labels
    if (this.bookLabelEl) {
      this.bookLabelEl.innerText = `Book ${bnum}: ${spread.bookTitle}`;
    }
    if (this.pageIndicatorEl) {
      this.pageIndicatorEl.innerText = `Spread ${spread.spreadNumber} of ${this.totalSpreads}`;
    }
    if (this.progressSlider) {
      this.progressSlider.value = this.currentSpreadIndex;
    }

    // Set Book Theme Attributes
    this.bookContainer.setAttribute('data-book', bnum);

    // Dynamic Clean SVG Border for Current Book
    const borderFile = `assets/borders/border-book-${bnum}.svg`;

    // -------------------------------------------------------------
    // RENDER LEFT PAGE (CENTER-JUSTIFIED VERSES & ILLUMINATED INITIAL)
    // -------------------------------------------------------------
    let verseHtml = '';
    let globalLineIdx = 0;
    let isFirstLine = true;

    page.stanzas.forEach((stanza) => {
      verseHtml += `<div class="stanza">`;
      stanza.lines.forEach((line) => {
        const speaker = page.speakerBefore ? page.speakerBefore[String(globalLineIdx)] : null;
        if (speaker) {
          verseHtml += `<div class="speaker-badge">${this.escapeHtml(speaker)}</div>`;
        }

        if (isFirstLine) {
          isFirstLine = false;
          const initialLetter = page.initialLetter;
          const restOfFirstLine = page.firstLineRest;
          const prefix = page.initialPrefix || '';
          
          const firstSpaceIdx = restOfFirstLine.indexOf(' ');
          let firstWordRest = '';
          let remainingLine = '';
          if (firstSpaceIdx !== -1) {
            firstWordRest = restOfFirstLine.substring(0, firstSpaceIdx);
            remainingLine = restOfFirstLine.substring(firstSpaceIdx + 1);
          } else {
            firstWordRest = restOfFirstLine;
            remainingLine = '';
          }

          verseHtml += `
            <div class="verse-line first-verse-line">
              ${prefix ? `<span class="first-line-prefix">${this.escapeHtml(prefix)}</span>` : ''}
              <span class="illuminated-cap"><span class="cap-letter">${initialLetter}</span></span><span class="first-word-rest">${this.escapeHtml(firstWordRest)}</span>${remainingLine ? ` <span class="first-line-remaining">${this.escapeHtml(remainingLine)}</span>` : ''}
            </div>
          `;
        } else {
          verseHtml += `<div class="verse-line">${this.escapeHtml(line)}</div>`;
        }

        globalLineIdx++;
      });
      verseHtml += `</div>`;
    });

    this.leftPageEl.innerHTML = `
      <img src="${borderFile}" class="page-border-overlay" alt="" />
      <div class="page-content">
        <div class="page-header">
          <div class="chapter-number">Chapter ${page.chapter}</div>
          <div class="chapter-title">${this.escapeHtml(page.chapterTitle)}</div>
        </div>

        <div class="page-verse-container">
          ${verseHtml}
        </div>

        <div class="page-footer">
          <span class="folio-book-label">${this.escapeHtml(spread.bookTitle)}</span>
          <span class="folio-number">${spread.spreadNumber * 2 - 1}</span>
        </div>
      </div>
    `;

    // -------------------------------------------------------------
    // RENDER RIGHT PAGE (PICTURE ONLY — NO TEXT OR CAPTIONS UNDERNEATH)
    // -------------------------------------------------------------
    const ill = page.illustration;
    this.rightPageEl.innerHTML = `
      <img src="${borderFile}" class="page-border-overlay" alt="" />
      <div class="page-content">
        <div class="art-plate-container">
          <div class="art-image-frame">
            <img src="${ill.image}" alt="Story Illustration" loading="eager" />
          </div>
        </div>

        <div class="page-footer">
          <span class="folio-book-label">Book ${bnum}</span>
          <span class="folio-number">${spread.spreadNumber * 2}</span>
        </div>
      </div>
    `;

    // Ensure mobile view class
    if (window.innerWidth <= 900) {
      this.bookContainer.classList.remove('show-text', 'show-art');
      this.bookContainer.classList.add(this.mobileView === 'text' ? 'show-text' : 'show-art');
    }

    this.highlightActiveTOC();
  }

  renderTOC() {
    const listEl = document.getElementById('tocContent');
    if (!listEl) return;

    let html = '';
    this.books.forEach((book) => {
      html += `
        <div class="toc-book-section">
          <div class="toc-book-header">BOOK ${book.bookNumber}</div>
          <div class="toc-book-title">${this.escapeHtml(book.title)}</div>
          <ul class="toc-page-list">
      `;

      book.pages.forEach((page) => {
        const spreadIdx = this.spreads.findIndex(s => s.pageData.id === page.id);
        html += `
          <li class="toc-item" data-index="${spreadIdx}" onclick="window.thumperApp.goToSpread(${spreadIdx}); window.thumperApp.closeTOC();">
            <span class="toc-item-title">${this.escapeHtml(page.chapterTitle)} · Spread ${spreadIdx + 1}</span>
            <span class="toc-item-num">p. ${spreadIdx * 2 + 1}</span>
          </li>
        `;
      });

      html += `
          </ul>
        </div>
      `;
    });

    listEl.innerHTML = html;
  }

  highlightActiveTOC() {
    const items = document.querySelectorAll('.toc-item');
    items.forEach((it) => {
      const idx = parseInt(it.getAttribute('data-index'));
      it.classList.toggle('active', idx === this.currentSpreadIndex);
    });
  }

  openTOC() {
    if (this.tocDrawer) this.tocDrawer.classList.add('open');
    if (this.tocOverlay) this.tocOverlay.classList.add('open');
  }

  closeTOC() {
    if (this.tocDrawer) this.tocDrawer.classList.remove('open');
    if (this.tocOverlay) this.tocOverlay.classList.remove('open');
  }

  escapeHtml(text) {
    if (!text) return '';
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.thumperApp = new ThumperApp();
});
