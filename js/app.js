/**
 * Master Application Controller for the Thumper 5-Book Interactive Reader
 * Verbatim text, center-justified verses, no picture captions, illuminated fairy tale styling.
 */
class ThumperApp {
  constructor() {
    this.books = window.THUMPER_COLLECTION || [];
    this.spreads = [];
    this.currentSpreadIndex = 0;
    this.phoneSubPage = 0; // 0 = Words (.left-page), 1 = Art (.right-page)

    this.initSpreads();
    this.initDOM();
    this.initFlipEngine();
    this.renderTOC();
    
    // Check URL hash first (e.g. #spread=15 or #spread=15&page=art)
    const hash = window.location.hash;
    const match = hash.match(/spread=(\d+)/);
    const pageMatch = hash.match(/page=(text|art)/);
    if (match) {
      this.currentSpreadIndex = Math.min(Math.max(0, parseInt(match[1])), this.spreads.length - 1);
      if (pageMatch && pageMatch[1] === 'art') {
        this.phoneSubPage = 1;
      }
    } else {
      // Restore saved reading position
      const saved = localStorage.getItem('thumper_reading_spread');
      if (saved !== null && !isNaN(parseInt(saved))) {
        this.currentSpreadIndex = Math.min(Math.max(0, parseInt(saved)), this.spreads.length - 1);
      }
    }

    this.renderCurrentSpread();
  }

  isPhone() {
    return window.innerWidth <= 680;
  }

  canAdvanceNext() {
    if (this.isPhone()) {
      return (this.currentSpreadIndex < this.totalSpreads - 1) || (this.phoneSubPage === 0);
    }
    return this.currentSpreadIndex < this.totalSpreads - 1;
  }

  canAdvancePrev() {
    if (this.isPhone()) {
      return (this.currentSpreadIndex > 0) || (this.phoneSubPage === 1);
    }
    return this.currentSpreadIndex > 0;
  }

  nextPage() {
    if (this.isPhone()) {
      if (this.phoneSubPage === 0) {
        this.phoneSubPage = 1;
        this.updateLocationHash();
        this.renderCurrentSpread();
        return true;
      } else {
        if (this.currentSpreadIndex < this.totalSpreads - 1) {
          this.currentSpreadIndex++;
          this.phoneSubPage = 0;
          this.updateLocationHash();
          this.renderCurrentSpread();
          return true;
        }
        return false;
      }
    } else {
      if (this.currentSpreadIndex < this.totalSpreads - 1) {
        this.currentSpreadIndex++;
        this.updateLocationHash();
        this.renderCurrentSpread();
        return true;
      }
      return false;
    }
  }

  prevPage() {
    if (this.isPhone()) {
      if (this.phoneSubPage === 1) {
        this.phoneSubPage = 0;
        this.updateLocationHash();
        this.renderCurrentSpread();
        return true;
      } else {
        if (this.currentSpreadIndex > 0) {
          this.currentSpreadIndex--;
          this.phoneSubPage = 1;
          this.updateLocationHash();
          this.renderCurrentSpread();
          return true;
        }
        return false;
      }
    } else {
      if (this.currentSpreadIndex > 0) {
        this.currentSpreadIndex--;
        this.updateLocationHash();
        this.renderCurrentSpread();
        return true;
      }
      return false;
    }
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

    this.updateSliderRange();

    if (this.progressSlider) {
      this.progressSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (this.isPhone()) {
          const spread = Math.floor(val / 2);
          const sub = val % 2;
          this.goToSpread(spread, sub);
        } else {
          this.goToSpread(val, 0);
        }
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

    window.addEventListener('hashchange', () => {
      const match = window.location.hash.match(/spread=(\d+)/);
      const pageMatch = window.location.hash.match(/page=(text|art)/);
      if (match) {
        const idx = parseInt(match[1]);
        const sub = pageMatch && pageMatch[1] === 'art' ? 1 : 0;
        this.goToSpread(idx, sub);
      }
    });

    window.addEventListener('resize', () => {
      this.updateSliderRange();
      this.renderCurrentSpread();
      this.fitVerseText();
    });
  }

  initFlipEngine() {
    this.flipEngine = new window.PageFlipEngine(this);
  }

  updateSliderRange() {
    if (!this.progressSlider) return;
    if (this.isPhone()) {
      this.progressSlider.min = 0;
      this.progressSlider.max = this.totalSpreads * 2 - 1;
      this.progressSlider.value = this.currentSpreadIndex * 2 + this.phoneSubPage;
    } else {
      this.progressSlider.min = 0;
      this.progressSlider.max = this.totalSpreads - 1;
      this.progressSlider.value = this.currentSpreadIndex;
    }
  }

  updateLocationHash() {
    if (this.isPhone()) {
      window.location.hash = `spread=${this.currentSpreadIndex}&page=${this.phoneSubPage === 0 ? 'text' : 'art'}`;
    } else {
      window.location.hash = `spread=${this.currentSpreadIndex}`;
    }
  }

  goToSpread(index, subPage = 0) {
    if (index < 0 || index >= this.totalSpreads) return;
    this.currentSpreadIndex = index;
    this.phoneSubPage = subPage;
    localStorage.setItem('thumper_reading_spread', index);
    this.updateLocationHash();
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
    
    this.updateSliderRange();

    if (this.pageIndicatorEl) {
      if (this.isPhone()) {
        const pageNum = this.currentSpreadIndex * 2 + this.phoneSubPage + 1;
        const totalPages = this.totalSpreads * 2;
        const pageType = this.phoneSubPage === 0 ? 'Words' : 'Art';
        this.pageIndicatorEl.innerText = `Page ${pageNum} of ${totalPages} · ${pageType}`;
      } else {
        this.pageIndicatorEl.innerText = `Spread ${spread.spreadNumber} of ${this.totalSpreads}`;
      }
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

    page.stanzas.forEach((stanza, stanzaIdx) => {
      verseHtml += `<div class="stanza">`;
      stanza.lines.forEach((line, lineIdx) => {
        const speaker = page.speakerBefore ? page.speakerBefore[String(globalLineIdx)] : null;
        if (speaker && !speaker.toLowerCase().includes('narrator')) {
          verseHtml += `<div class="speaker-badge"><span class="fleuron">❧</span> ${this.escapeHtml(speaker)} <span class="fleuron">☙</span></div>`;
        }

        if (isFirstLine) {
          isFirstLine = false;
          if (page.initialLetter) {
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
          } else if (page.isDialogueOpening) {
            verseHtml += `<div class="dialogue-opening-divider"><span class="header-fleuron">❧ ❖ ☙</span></div>`;
            verseHtml += `<div class="verse-line">${this.escapeHtml(line)}</div>`;
          } else {
            verseHtml += `<div class="verse-line">${this.escapeHtml(line)}</div>`;
          }
        } else if (lineIdx === 0 && stanzaIdx > 0) {
          // Rubricated illuminated capital for each subsequent stanza opening line
          const match = line.match(/^([“"']?)([A-Za-z])(.*)$/);
          if (match) {
            const quotePrefix = match[1];
            const capLetter = match[2];
            const rest = match[3];
            const colorClass = `stanza-cap-${stanzaIdx % 5}`;
            verseHtml += `<div class="verse-line">${quotePrefix ? `<span class="verse-quote-prefix">${this.escapeHtml(quotePrefix)}</span>` : ''}<span class="rubricated-cap ${colorClass}">${this.escapeHtml(capLetter)}</span>${this.escapeHtml(rest)}</div>`;
          } else {
            verseHtml += `<div class="verse-line">${this.escapeHtml(line)}</div>`;
          }
        } else {
          verseHtml += `<div class="verse-line">${this.escapeHtml(line)}</div>`;
        }

        globalLineIdx++;
      });
      verseHtml += `</div>`;
    });

    let headerHtml = '';
    const rawTitle = (page.chapterTitle || '').trim();
    if (!rawTitle || rawTitle.toLowerCase().startsWith('chapter ')) {
      headerHtml = `<div class="chapter-title">Chapter ${page.chapter}</div>`;
    } else {
      headerHtml = `
        <div class="chapter-number">Chapter ${page.chapter}</div>
        <div class="chapter-title">${this.escapeHtml(rawTitle)}</div>
      `;
    }

    this.leftPageEl.innerHTML = `
      <img src="${borderFile}" class="page-border-overlay" alt="" />
      <div class="page-content">
        <div class="page-header">
          ${headerHtml}
          <div class="header-divider"><span class="header-fleuron">❧ ❖ ☙</span></div>
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

    // Set Phone subpage visibility
    if (this.isPhone()) {
      if (this.phoneSubPage === 0) {
        this.bookContainer.classList.add('phone-view-words');
        this.bookContainer.classList.remove('phone-view-art');
      } else {
        this.bookContainer.classList.add('phone-view-art');
        this.bookContainer.classList.remove('phone-view-words');
      }
    } else {
      this.bookContainer.classList.remove('phone-view-words', 'phone-view-art');
    }

    this.highlightActiveTOC();
    this.fitVerseText();
  }

  fitVerseText() {
    const container = this.leftPageEl.querySelector('.page-verse-container');
    if (!container) return;

    // Reset styles to baseline
    container.style.removeProperty('font-size');
    container.style.removeProperty('line-height');
    const stanzas = container.querySelectorAll('.stanza');
    stanzas.forEach(st => st.style.removeProperty('margin-bottom'));
    const dividers = container.querySelectorAll('.dialogue-opening-divider');
    dividers.forEach(d => d.style.removeProperty('margin-bottom'));

    const availableHeight = container.clientHeight;
    if (availableHeight <= 0) return;

    // If content exceeds container on laptop or phone, scale down gently to fit perfectly
    if (container.scrollHeight > availableHeight) {
      const currentSize = parseFloat(window.getComputedStyle(container).fontSize);
      const scale = (availableHeight - 6) / container.scrollHeight;
      let fittedSize = Math.max(9.5, Math.floor(currentSize * scale * 10) / 10);
      container.style.setProperty('font-size', fittedSize + 'px', 'important');
      container.style.setProperty('line-height', '1.24', 'important');
      stanzas.forEach(st => {
        st.style.setProperty('margin-bottom', Math.max(2, Math.floor(6 * scale)) + 'px', 'important');
      });
      if (scale < 0.95) {
        dividers.forEach(d => d.style.setProperty('margin-bottom', '1px', 'important'));
      }

      // Refine if still overflowing due to wrapping variations
      let attempts = 0;
      while (container.scrollHeight > availableHeight && fittedSize > 9.0 && attempts < 10) {
        fittedSize = Math.max(9.0, Math.round((fittedSize - 0.3) * 10) / 10);
        container.style.setProperty('font-size', fittedSize + 'px', 'important');
        attempts++;
      }
    }
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
        if (page.isChapterStart) {
          const spreadIdx = this.spreads.findIndex(s => s.pageData.id === page.id);
          let titleDisplay = page.chapterTitle ? `Chapter ${page.chapter}: ${page.chapterTitle}` : `Chapter ${page.chapter}`;
          if (page.chapterTitle && page.chapterTitle.toLowerCase().startsWith('chapter ')) {
            titleDisplay = page.chapterTitle;
          }
          html += `
            <li class="toc-item" data-index="${spreadIdx}" onclick="window.thumperApp.goToSpread(${spreadIdx}); window.thumperApp.closeTOC();">
              <span class="toc-item-title">${this.escapeHtml(titleDisplay)}</span>
              <span class="toc-item-num">Spread ${spreadIdx + 1} · p. ${spreadIdx * 2 + 1}</span>
            </li>
          `;
        }
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
    const curSpread = this.spreads[this.currentSpreadIndex];
    if (!curSpread) return;
    const curBook = curSpread.bookNumber;
    const curChapter = curSpread.pageData.chapter;

    items.forEach((it) => {
      const idx = parseInt(it.getAttribute('data-index'));
      const targetSpread = this.spreads[idx];
      const isActive = targetSpread && targetSpread.bookNumber === curBook && targetSpread.pageData.chapter === curChapter;
      it.classList.toggle('active', isActive);
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
