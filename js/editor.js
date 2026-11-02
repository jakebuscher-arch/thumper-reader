/**
 * Thumper Editorial Studio & Interactive Commenting Controller
 * Lets the author edit any verse line, chapter title, or speaker badge directly on the page,
 * leave spread-level or artwork comments for the AI agent, auto-saves to localStorage,
 * and exports either a formatted AI Agent instruction prompt or a full updated book-data.js.
 */
class ThumperEditorStudio {
  constructor(app) {
    this.app = app;
    this.storageKey = 'thumper_editorial_studio_v1';

    // Clone pristine baseline data before applying any user edits
    this.baselineByPageId = {};
    this.captureBaseline();

    // Load saved edits and comments
    this.state = this.loadState();

    // Apply saved text edits into live in-memory THUMPER_COLLECTION
    this.applyAllEditsToMemory();

    // Hook into app.renderCurrentSpread so every spread render becomes interactive
    const origRender = this.app.renderCurrentSpread.bind(this.app);
    this.app.renderCurrentSpread = () => {
      origRender();
      this.enhanceSpreadDOM();
      this.syncDockToCurrentSpread();
    };

    this.initStudioDOM();
    this.app.renderCurrentSpread();
    this.renderChangesList();
  }

  captureBaseline() {
    this.app.spreads.forEach((spread) => {
      const p = spread.pageData;
      this.baselineByPageId[p.id] = {
        chapterTitle: p.chapterTitle || '',
        initialPrefix: p.initialPrefix || '',
        initialLetter: p.initialLetter || '',
        firstLineRest: p.firstLineRest || '',
        speakerBefore: JSON.parse(JSON.stringify(p.speakerBefore || {})),
        stanzas: p.stanzas.map((st) => ({
          chapter: st.chapter,
          chapterTitle: st.chapterTitle,
          lines: [...st.lines]
        }))
      };
    });
  }

  loadState() {
    const empty = {
      lineEdits: {},      // key: `${pageId}:S${sIdx}:L${lIdx}` -> newLineString
      titleEdits: {},     // key: `${pageId}` -> newChapterTitle
      speakerEdits: {},   // key: `${pageId}:G${globalLineIdx}` -> newSpeakerString
      spreadNotes: {},    // key: `${pageId}` -> general/text note for agent
      artNotes: {}        // key: `${pageId}` -> illustration note for agent
    };
    try {
      const raw = window.localStorage.getItem(this.storageKey);
      if (raw) {
        const parsed = JSON.parse(raw);
        return {
          lineEdits: parsed.lineEdits || {},
          titleEdits: parsed.titleEdits || {},
          speakerEdits: parsed.speakerEdits || {},
          spreadNotes: parsed.spreadNotes || {},
          artNotes: parsed.artNotes || {}
        };
      }
    } catch (e) {
      console.warn('Could not load saved editorial state:', e);
    }
    return empty;
  }

  saveState() {
    try {
      window.localStorage.setItem(this.storageKey, JSON.stringify(this.state));
      const ind = document.getElementById('spreadSaveIndicator');
      if (ind) {
        ind.textContent = '✓ Auto-saved';
        ind.style.opacity = '1';
      }
    } catch (e) {
      console.warn('Could not persist editorial state:', e);
    }
    this.updateCountsUI();
    this.renderChangesList();
  }

  syncPageFirstLineProps(page, newLine0) {
    const base = this.baselineByPageId[page.id];
    if (!base) return;
    if (base.initialLetter) {
      // Preserve quote prefix if present
      const m = newLine0.match(/^([“"'‘\s]*)([A-Za-z])(.*)$/);
      if (m) {
        page.initialPrefix = m[1] || '';
        page.initialLetter = m[2];
        page.firstLineRest = m[3];
      } else {
        page.initialPrefix = '';
        page.initialLetter = newLine0.charAt(0) || base.initialLetter;
        page.firstLineRest = newLine0.slice(1);
      }
    } else {
      page.firstLineRest = newLine0;
    }
  }

  applyAllEditsToMemory() {
    this.app.spreads.forEach((spread) => {
      const page = spread.pageData;
      const base = this.baselineByPageId[page.id];
      if (!base) return;

      // Reset to baseline first
      page.chapterTitle = base.chapterTitle;
      page.initialPrefix = base.initialPrefix;
      page.initialLetter = base.initialLetter;
      page.firstLineRest = base.firstLineRest;
      page.speakerBefore = JSON.parse(JSON.stringify(base.speakerBefore));
      page.stanzas.forEach((st, sIdx) => {
        st.lines = [...base.stanzas[sIdx].lines];
      });

      // Apply title edit
      if (Object.prototype.hasOwnProperty.call(this.state.titleEdits, page.id)) {
        page.chapterTitle = this.state.titleEdits[page.id];
      }

      // Apply speaker edits
      Object.keys(this.state.speakerEdits).forEach((k) => {
        if (k.startsWith(page.id + ':G')) {
          const gIdx = k.split(':G')[1];
          page.speakerBefore[gIdx] = this.state.speakerEdits[k];
        }
      });

      // Apply line edits
      page.stanzas.forEach((st, sIdx) => {
        st.lines.forEach((_, lIdx) => {
          const key = `${page.id}:S${sIdx}:L${lIdx}`;
          if (Object.prototype.hasOwnProperty.call(this.state.lineEdits, key)) {
            const newText = this.state.lineEdits[key];
            st.lines[lIdx] = newText;
            if (sIdx === 0 && lIdx === 0) {
              this.syncPageFirstLineProps(page, newText);
            }
          }
        });
      });
    });
  }

  initStudioDOM() {
    this.dockEl = document.getElementById('editorDock');
    this.btnToggleDock = document.getElementById('btnToggleDock');
    this.btnCloseDock = document.getElementById('btnCloseDock');
    this.spreadCommentInput = document.getElementById('spreadCommentInput');
    this.artCommentInput = document.getElementById('artCommentInput');
    this.dockSpreadLabel = document.getElementById('dockSpreadLabel');
    this.changesListEl = document.getElementById('changesList');
    this.editCountPill = document.getElementById('editCountPill');
    this.totalChangesLabel = document.getElementById('totalChangesLabel');
    this.btnResetSpread = document.getElementById('btnResetSpread');
    this.btnCopyForAgent = document.getElementById('btnCopyForAgent');
    this.btnDownloadBookData = document.getElementById('btnDownloadBookData');
    this.btnClearAllEdits = document.getElementById('btnClearAllEdits');
    this.btnExportModal = document.getElementById('btnExportModal');
    this.exportDialog = document.getElementById('exportDialog');
    this.exportSummaryPre = document.getElementById('exportSummaryPre');
    this.btnModalCopy = document.getElementById('btnModalCopy');
    this.btnModalDownloadJson = document.getElementById('btnModalDownloadJson');
    this.btnModalDownloadJs = document.getElementById('btnModalDownloadJs');

    if (this.btnToggleDock) {
      this.btnToggleDock.addEventListener('click', () => {
        this.dockEl.classList.toggle('collapsed');
        setTimeout(() => this.app.fitVerseText(), 320);
      });
    }

    if (this.btnCloseDock) {
      this.btnCloseDock.addEventListener('click', () => {
        this.dockEl.classList.add('collapsed');
        setTimeout(() => this.app.fitVerseText(), 320);
      });
    }

    if (this.spreadCommentInput) {
      this.spreadCommentInput.addEventListener('input', () => {
        const spread = this.app.spreads[this.app.currentSpreadIndex];
        if (!spread) return;
        const pageId = spread.pageData.id;
        const val = this.spreadCommentInput.value;
        if (val.trim()) {
          this.state.spreadNotes[pageId] = val;
        } else {
          delete this.state.spreadNotes[pageId];
        }
        this.saveState();
        this.updateSpreadStatusPills();
      });
    }

    if (this.artCommentInput) {
      this.artCommentInput.addEventListener('input', () => {
        const spread = this.app.spreads[this.app.currentSpreadIndex];
        if (!spread) return;
        const pageId = spread.pageData.id;
        const val = this.artCommentInput.value;
        if (val.trim()) {
          this.state.artNotes[pageId] = val;
        } else {
          delete this.state.artNotes[pageId];
        }
        this.saveState();
        this.updateSpreadStatusPills();
      });
    }

    if (this.btnResetSpread) {
      this.btnResetSpread.addEventListener('click', () => {
        const spread = this.app.spreads[this.app.currentSpreadIndex];
        if (!spread) return;
        const pageId = spread.pageData.id;
        this.resetSpread(pageId);
      });
    }

    if (this.btnCopyForAgent) {
      this.btnCopyForAgent.addEventListener('click', () => {
        this.openExportModal();
      });
    }

    if (this.btnExportModal) {
      this.btnExportModal.addEventListener('click', () => {
        this.openExportModal();
      });
    }

    if (this.btnDownloadBookData) {
      this.btnDownloadBookData.addEventListener('click', () => {
        this.downloadUpdatedBookDataJs();
      });
    }

    if (this.btnClearAllEdits) {
      this.btnClearAllEdits.addEventListener('click', () => {
        if (window.confirm('Clear all saved text edits and comments across all 5 books?')) {
          this.state = {
            lineEdits: {},
            titleEdits: {},
            speakerEdits: {},
            spreadNotes: {},
            artNotes: {}
          };
          this.applyAllEditsToMemory();
          this.saveState();
          this.app.renderCurrentSpread();
          this.showToast('All edits cleared');
        }
      });
    }

    if (this.btnModalCopy) {
      this.btnModalCopy.addEventListener('click', () => {
        const report = this.buildAgentMarkdownReport();
        navigator.clipboard.writeText(report).then(() => {
          this.showToast('Copied report! Paste it in chat to the Agent.');
        });
      });
    }

    if (this.btnModalDownloadJson) {
      this.btnModalDownloadJson.addEventListener('click', () => {
        const report = this.buildAgentMarkdownReport();
        this.triggerDownload('thumper-edits-and-comments.md', report, 'text/markdown;charset=utf-8');
        this.showToast('Downloaded thumper-edits-and-comments.md');
      });
    }

    if (this.btnModalDownloadJs) {
      this.btnModalDownloadJs.addEventListener('click', () => {
        this.downloadUpdatedBookDataJs();
      });
    }

    // Fallback for browsers without <dialog closedby="any"> support (e.g. Safari)
    if (this.exportDialog && !('closedBy' in HTMLDialogElement.prototype)) {
      this.exportDialog.addEventListener('click', (event) => {
        if (event.target !== this.exportDialog) return;
        const rect = this.exportDialog.getBoundingClientRect();
        const isDialogContent = (
          rect.top <= event.clientY &&
          event.clientY <= rect.top + rect.height &&
          rect.left <= event.clientX &&
          event.clientX <= rect.left + rect.width
        );
        if (isDialogContent) return;
        this.exportDialog.close();
      });
    }
  }

  enhanceSpreadDOM() {
    const spread = this.app.spreads[this.app.currentSpreadIndex];
    if (!spread) return;
    const page = spread.pageData;
    const base = this.baselineByPageId[page.id];
    if (!base) return;

    // 1. Make Chapter Title Editable
    const titleEl = this.app.leftPageEl.querySelector('.chapter-title');
    if (titleEl) {
      titleEl.classList.add('editable-text-node');
      titleEl.setAttribute('contenteditable', 'true');
      titleEl.setAttribute('spellcheck', 'true');
      titleEl.setAttribute('title', 'Click to edit chapter title');

      titleEl.addEventListener('blur', () => {
        const rawText = titleEl.innerText.trim();
        let cleaned = rawText;
        if (!base.chapterTitle && rawText.toLowerCase() === `chapter ${page.chapter}`) {
          cleaned = '';
        }
        if (cleaned !== base.chapterTitle) {
          this.state.titleEdits[page.id] = cleaned;
        } else {
          delete this.state.titleEdits[page.id];
        }
        page.chapterTitle = cleaned;
        this.saveState();
        this.app.renderTOC();
        this.updateSpreadStatusPills();
      });

      titleEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          titleEl.blur();
        }
      });
    }

    // 2. Make Speaker Badges Editable
    const speakerEls = this.app.leftPageEl.querySelectorAll('.speaker-badge');
    const speakerKeys = Object.keys(page.speakerBefore || {}).filter(
      (k) => page.speakerBefore[k] && !page.speakerBefore[k].toLowerCase().includes('narrator')
    );
    speakerEls.forEach((badgeEl, idx) => {
      const gKey = speakerKeys[idx];
      if (gKey === undefined) return;
      badgeEl.classList.add('editable-text-node');
      badgeEl.setAttribute('contenteditable', 'true');
      badgeEl.setAttribute('title', 'Click to edit speaker label');

      badgeEl.addEventListener('blur', () => {
        const cleaned = badgeEl.innerText.replace(/[❧☙]/g, '').trim();
        const editKey = `${page.id}:G${gKey}`;
        const origSpeaker = base.speakerBefore[gKey];
        if (cleaned !== origSpeaker) {
          this.state.speakerEdits[editKey] = cleaned;
        } else {
          delete this.state.speakerEdits[editKey];
        }
        page.speakerBefore[gKey] = cleaned;
        this.saveState();
        this.app.renderCurrentSpread();
      });

      badgeEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          badgeEl.blur();
        }
      });
    });

    // 3. Make Every Verse Line Directly Editable with Plain-Text ContentEditable
    const stanzaEls = this.app.leftPageEl.querySelectorAll('.stanza');
    stanzaEls.forEach((stanzaEl, sIdx) => {
      const lineEls = stanzaEl.querySelectorAll('.verse-line');
      lineEls.forEach((lineEl, lIdx) => {
        const key = `${page.id}:S${sIdx}:L${lIdx}`;
        const origLine = base.stanzas[sIdx]?.lines[lIdx] || '';
        const currentLine = page.stanzas[sIdx]?.lines[lIdx] || '';
        const isEdited = Object.prototype.hasOwnProperty.call(this.state.lineEdits, key) && currentLine !== origLine;

        const wrapper = document.createElement('div');
        wrapper.className = `editable-line-wrapper${isEdited ? ' is-edited' : ''}`;

        lineEl.parentNode.insertBefore(wrapper, lineEl);
        wrapper.appendChild(lineEl);

        lineEl.classList.add('editable-text-node');
        lineEl.setAttribute('contenteditable', 'true');
        lineEl.setAttribute('spellcheck', 'true');
        lineEl.setAttribute('title', isEdited ? `Original: "${origLine}"` : 'Click to edit this line directly');

        // When user focuses line 0 (which has fancy illuminated cap spans) or rubricated cap spans,
        // switch to clean text editing on focus so typing anywhere in the line is effortless
        lineEl.addEventListener('focus', () => {
          const latestVal = page.stanzas[sIdx].lines[lIdx];
          if (lineEl.querySelector('.illuminated-cap, .rubricated-cap')) {
            lineEl.textContent = latestVal;
            lineEl.classList.remove('first-verse-line');
          }
        });

        lineEl.addEventListener('blur', () => {
          const newText = lineEl.innerText.replace(/\r?\n/g, ' ').trim();
          if (newText && newText !== origLine) {
            this.state.lineEdits[key] = newText;
            page.stanzas[sIdx].lines[lIdx] = newText;
          } else {
            delete this.state.lineEdits[key];
            page.stanzas[sIdx].lines[lIdx] = origLine;
          }
          if (sIdx === 0 && lIdx === 0) {
            this.syncPageFirstLineProps(page, page.stanzas[0].lines[0]);
          }
          this.saveState();
          // Re-render spread so illuminated caps / rubricated caps re-format cleanly
          this.app.renderCurrentSpread();
        });

        lineEl.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            lineEl.blur();
          } else if (e.key === 'Escape') {
            e.preventDefault();
            lineEl.textContent = page.stanzas[sIdx].lines[lIdx];
            lineEl.blur();
          }
        });

        // Quick Comment button on hover
        const commentBtn = document.createElement('button');
        commentBtn.type = 'button';
        commentBtn.className = 'line-action-btn';
        commentBtn.innerHTML = '💬';
        commentBtn.title = 'Add a comment about this line for the Agent';
        commentBtn.addEventListener('mousedown', (e) => {
          e.preventDefault(); // prevent blur race
          this.promptLineComment(page, sIdx, lIdx);
        });
        wrapper.appendChild(commentBtn);

        // Quick Revert button if edited
        if (isEdited) {
          const revertBtn = document.createElement('button');
          revertBtn.type = 'button';
          revertBtn.className = 'line-action-btn revert-btn always-show';
          revertBtn.innerHTML = '↺';
          revertBtn.title = `Revert to original: "${origLine}"`;
          revertBtn.addEventListener('mousedown', (e) => {
            e.preventDefault();
            delete this.state.lineEdits[key];
            page.stanzas[sIdx].lines[lIdx] = origLine;
            if (sIdx === 0 && lIdx === 0) {
              this.syncPageFirstLineProps(page, origLine);
            }
            this.saveState();
            this.app.renderCurrentSpread();
            this.showToast('Reverted line to original');
          });
          wrapper.appendChild(revertBtn);
        }
      });
    });

    this.updateSpreadStatusPills();
    this.app.fitVerseText();
  }

  promptLineComment(page, sIdx, lIdx) {
    const lineText = page.stanzas[sIdx]?.lines[lIdx] || '';
    this.dockEl.classList.remove('collapsed');
    if (this.spreadCommentInput) {
      const prefix = `[Stanza ${sIdx + 1}, Line ${lIdx + 1} ("${lineText}")]: `;
      const existing = this.spreadCommentInput.value.trim();
      this.spreadCommentInput.value = existing ? `${existing}\n${prefix}` : prefix;
      this.state.spreadNotes[page.id] = this.spreadCommentInput.value;
      this.saveState();
      this.spreadCommentInput.focus();
      this.spreadCommentInput.setSelectionRange(
        this.spreadCommentInput.value.length,
        this.spreadCommentInput.value.length
      );
    }
  }

  updateSpreadStatusPills() {
    const spread = this.app.spreads[this.app.currentSpreadIndex];
    if (!spread) return;
    const pageId = spread.pageData.id;

    // Remove existing status bar if present
    const oldBar = this.app.leftPageEl.querySelector('.spread-edit-status-bar');
    if (oldBar) oldBar.remove();

    const editCount = this.countEditsForPage(pageId);
    const hasNotes = Boolean(
      (this.state.spreadNotes[pageId] && this.state.spreadNotes[pageId].trim()) ||
      (this.state.artNotes[pageId] && this.state.artNotes[pageId].trim())
    );

    if (editCount === 0 && !hasNotes) return;

    const bar = document.createElement('div');
    bar.className = 'spread-edit-status-bar';

    if (editCount > 0) {
      const pill = document.createElement('span');
      pill.className = 'status-pill pill-edited';
      pill.textContent = `✎ ${editCount} Text Edit${editCount > 1 ? 's' : ''}`;
      pill.onclick = () => this.dockEl.classList.remove('collapsed');
      bar.appendChild(pill);
    }

    if (hasNotes) {
      const pill = document.createElement('span');
      pill.className = 'status-pill pill-commented';
      pill.textContent = `💬 Note Added`;
      pill.onclick = () => {
        this.dockEl.classList.remove('collapsed');
        if (this.spreadCommentInput) this.spreadCommentInput.focus();
      };
      bar.appendChild(pill);
    }

    this.app.leftPageEl.appendChild(bar);
  }

  countEditsForPage(pageId) {
    let count = 0;
    if (Object.prototype.hasOwnProperty.call(this.state.titleEdits, pageId)) count++;
    Object.keys(this.state.speakerEdits).forEach((k) => {
      if (k.startsWith(pageId + ':')) count++;
    });
    Object.keys(this.state.lineEdits).forEach((k) => {
      if (k.startsWith(pageId + ':')) count++;
    });
    return count;
  }

  syncDockToCurrentSpread() {
    const spread = this.app.spreads[this.app.currentSpreadIndex];
    if (!spread) return;
    const pageId = spread.pageData.id;

    if (this.dockSpreadLabel) {
      this.dockSpreadLabel.textContent = `Spread ${spread.spreadNumber} (${pageId}) Notes`;
    }
    if (this.spreadCommentInput) {
      this.spreadCommentInput.value = this.state.spreadNotes[pageId] || '';
    }
    if (this.artCommentInput) {
      this.artCommentInput.value = this.state.artNotes[pageId] || '';
    }
    this.updateCountsUI();
  }

  resetSpread(pageId) {
    delete this.state.titleEdits[pageId];
    delete this.state.spreadNotes[pageId];
    delete this.state.artNotes[pageId];
    Object.keys(this.state.speakerEdits).forEach((k) => {
      if (k.startsWith(pageId + ':')) delete this.state.speakerEdits[k];
    });
    Object.keys(this.state.lineEdits).forEach((k) => {
      if (k.startsWith(pageId + ':')) delete this.state.lineEdits[k];
    });
    this.applyAllEditsToMemory();
    this.saveState();
    this.app.renderCurrentSpread();
    this.showToast(`Reset ${pageId} to original`);
  }

  getAllChangeRecords() {
    const records = [];

    this.app.spreads.forEach((spread, spreadIdx) => {
      const page = spread.pageData;
      const pageId = page.id;
      const base = this.baselineByPageId[pageId];
      if (!base) return;

      // Title edit
      if (Object.prototype.hasOwnProperty.call(this.state.titleEdits, pageId)) {
        records.push({
          type: 'title',
          spreadIdx,
          spreadNumber: spread.spreadNumber,
          bookNumber: spread.bookNumber,
          pageId,
          label: `Chapter Title`,
          oldText: base.chapterTitle || `Chapter ${page.chapter}`,
          newText: this.state.titleEdits[pageId]
        });
      }

      // Speaker edits
      Object.keys(this.state.speakerEdits).forEach((k) => {
        if (k.startsWith(pageId + ':G')) {
          const gIdx = k.split(':G')[1];
          records.push({
            type: 'speaker',
            spreadIdx,
            spreadNumber: spread.spreadNumber,
            bookNumber: spread.bookNumber,
            pageId,
            label: `Speaker Badge (Line ${parseInt(gIdx) + 1})`,
            oldText: base.speakerBefore[gIdx],
            newText: this.state.speakerEdits[k]
          });
        }
      });

      // Line edits
      page.stanzas.forEach((st, sIdx) => {
        st.lines.forEach((_, lIdx) => {
          const key = `${pageId}:S${sIdx}:L${lIdx}`;
          if (Object.prototype.hasOwnProperty.call(this.state.lineEdits, key)) {
            records.push({
              type: 'line',
              spreadIdx,
              spreadNumber: spread.spreadNumber,
              bookNumber: spread.bookNumber,
              pageId,
              label: `Stanza ${sIdx + 1}, Line ${lIdx + 1}`,
              oldText: base.stanzas[sIdx].lines[lIdx],
              newText: this.state.lineEdits[key]
            });
          }
        });
      });

      // Spread Note
      if (this.state.spreadNotes[pageId] && this.state.spreadNotes[pageId].trim()) {
        records.push({
          type: 'note',
          spreadIdx,
          spreadNumber: spread.spreadNumber,
          bookNumber: spread.bookNumber,
          pageId,
          label: `Note for Agent`,
          comment: this.state.spreadNotes[pageId].trim()
        });
      }

      // Art Note
      if (this.state.artNotes[pageId] && this.state.artNotes[pageId].trim()) {
        records.push({
          type: 'art-note',
          spreadIdx,
          spreadNumber: spread.spreadNumber,
          bookNumber: spread.bookNumber,
          pageId,
          label: `Artwork Note`,
          comment: this.state.artNotes[pageId].trim()
        });
      }
    });

    return records;
  }

  updateCountsUI() {
    const total = this.getAllChangeRecords().length;
    if (this.editCountPill) {
      this.editCountPill.textContent = String(total);
      this.editCountPill.classList.toggle('zero', total === 0);
    }
    if (this.totalChangesLabel) {
      this.totalChangesLabel.textContent = String(total);
    }
  }

  renderChangesList() {
    if (!this.changesListEl) return;
    const records = this.getAllChangeRecords();
    this.updateCountsUI();

    if (records.length === 0) {
      this.changesListEl.innerHTML = `
        <div class="dock-help-text" style="opacity: 0.7; text-align: center; padding: 14px 4px;">
          No edits or comments yet. Click any line on the page to edit it, or type a note above!
        </div>
      `;
      return;
    }

    this.changesListEl.innerHTML = records.map((rec) => {
      const isComment = rec.type === 'note' || rec.type === 'art-note';
      return `
        <div class="change-card ${isComment ? 'type-comment' : ''}" data-spread-idx="${rec.spreadIdx}">
          <div class="change-card-header">
            <span>Book ${rec.bookNumber} · Spread ${rec.spreadNumber} (${rec.pageId})</span>
            <span>${this.app.escapeHtml(rec.label)}</span>
          </div>
          ${isComment ? `
            <div class="change-comment-preview">“${this.app.escapeHtml(rec.comment)}”</div>
          ` : `
            <div class="change-diff-old">${this.app.escapeHtml(rec.oldText)}</div>
            <div class="change-diff-new">${this.app.escapeHtml(rec.newText)}</div>
          `}
        </div>
      `;
    }).join('');

    this.changesListEl.querySelectorAll('.change-card').forEach((card) => {
      card.addEventListener('click', () => {
        const idx = parseInt(card.getAttribute('data-spread-idx'));
        if (!isNaN(idx)) {
          this.app.goToSpread(idx);
        }
      });
    });
  }

  buildAgentMarkdownReport() {
    const records = this.getAllChangeRecords();
    if (records.length === 0) {
      return `# Thumper E-Reader Editorial Report\n\nNo edits or comments recorded yet.`;
    }

    const lines = [
      `# Thumper E-Reader Editorial Changes & Comments`,
      `Please apply the following ${records.length} edit(s)/comment(s) to the Thumper e-reader and push them live:`,
      ``
    ];

    // Group by spread
    const bySpread = new Map();
    records.forEach((r) => {
      if (!bySpread.has(r.pageId)) {
        bySpread.set(r.pageId, {
          bookNumber: r.bookNumber,
          spreadNumber: r.spreadNumber,
          pageId: r.pageId,
          items: []
        });
      }
      bySpread.get(r.pageId).items.push(r);
    });

    bySpread.forEach((group) => {
      lines.push(`## Book ${group.bookNumber} — Spread ${group.spreadNumber} (\`${group.pageId}\`)`);
      group.items.forEach((item) => {
        if (item.type === 'note') {
          lines.push(`- **Comment for Agent:** ${item.comment}`);
        } else if (item.type === 'art-note') {
          lines.push(`- **Illustration / Art Request:** ${item.comment}`);
        } else {
          lines.push(`- **${item.label} Edit:**`);
          lines.push(`  - Old: \`${item.oldText}\``);
          lines.push(`  - New: \`${item.newText}\``);
        }
      });
      lines.push(``);
    });

    return lines.join('\n');
  }

  openExportModal() {
    if (!this.exportDialog || !this.exportSummaryPre) return;
    this.exportSummaryPre.textContent = this.buildAgentMarkdownReport();
    this.exportDialog.showModal();
  }

  downloadUpdatedBookDataJs() {
    const content = `window.THUMPER_COLLECTION = ${JSON.stringify(this.app.books, null, 2)};\n`;
    this.triggerDownload('book-data.js', content, 'application/javascript;charset=utf-8');
    this.showToast('Downloaded updated book-data.js!');
  }

  triggerDownload(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  }

  showToast(message) {
    const toast = document.getElementById('editorToast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2600);
  }
}

function initEditorialStudio() {
  if (window.thumperApp && !window.thumperEditorStudio) {
    window.thumperEditorStudio = new ThumperEditorStudio(window.thumperApp);
  }
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', initEditorialStudio);
} else {
  initEditorialStudio();
}
