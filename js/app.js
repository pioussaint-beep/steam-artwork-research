/**
 * STEAM Lab Inspiration Suite - Core Application Logic
 * Powers search, filtering, lightbox modals, card rendering, and concept generation.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // State variables
  let allCatalog = [];
  let currentTab = 'all'; // 'all', 'logos', 'artwork', 'moodboard', 'generator'
  let currentCategory = 'all';
  let currentGrade = 'all';
  let currentSearch = '';
  let currentSort = 'featured';
  let activeModalItem = null;

  // DOM References
  const itemsGrid = document.getElementById('itemsGrid');
  const moodboardGrid = document.getElementById('moodboardGrid');
  const emptyState = document.getElementById('emptyState');
  const moodboardEmptyState = document.getElementById('moodboardEmptyState');
  const moodboardSummaryCard = document.getElementById('moodboardSummaryCard');
  
  const searchInput = document.getElementById('searchInput');
  const clearSearchBtn = document.getElementById('clearSearch');
  const gradeFilter = document.getElementById('gradeFilter');
  const sortSelect = document.getElementById('sortSelect');
  const categoryPills = document.getElementById('categoryPills');
  const visibleCountEl = document.getElementById('visibleCount');
  const activeChipsEl = document.getElementById('activeChips');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const resetFromEmptyBtn = document.getElementById('resetFromEmpty');
  
  // Counters in Nav
  const countAll = document.getElementById('countAll');
  const countLogos = document.getElementById('countLogos');
  const countArt = document.getElementById('countArt');
  const countMoodboard = document.getElementById('countMoodboard');

  // Views
  const galleryView = document.getElementById('galleryView');
  const moodboardView = document.getElementById('moodboardView');
  const generatorView = document.getElementById('generatorView');
  const guideView = document.getElementById('guideView');
  const navTabs = document.querySelectorAll('.nav-tab');

  // Lightbox Modal
  const itemModal = document.getElementById('itemModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalImg = document.getElementById('modalImg');
  const modalPaletteSwatches = document.getElementById('modalPaletteSwatches');
  const modalTypeBadge = document.getElementById('modalTypeBadge');
  const modalGradeBadge = document.getElementById('modalGradeBadge');
  const modalCategoryBadge = document.getElementById('modalCategoryBadge');
  const modalTitle = document.getElementById('modalTitle');
  const modalAweFactor = document.getElementById('modalAweFactor');
  const modalTakeaways = document.getElementById('modalTakeaways');
  const modalMotifsList = document.getElementById('modalMotifsList');
  const modalUserNotes = document.getElementById('modalUserNotes');
  const modalShortlistBtn = document.getElementById('modalShortlistBtn');
  const modalShortlistLabel = document.getElementById('modalShortlistLabel');
  const modalSourceLink = document.getElementById('modalSourceLink');

  // Export Modal
  const exportModal = document.getElementById('exportModal');
  const exportBriefBtn = document.getElementById('exportBriefBtn');
  const exportModalCloseBtn = document.getElementById('exportModalCloseBtn');
  const exportContentArea = document.getElementById('exportContentArea');
  const printReportBtn = document.getElementById('printReportBtn');
  const copyMarkdownBtn = document.getElementById('copyMarkdownBtn');
  const downloadJsonBtn = document.getElementById('downloadJsonBtn');
  const clearMoodboardBtn = document.getElementById('clearMoodboardBtn');
  const browseGalleryFromMoodboard = document.getElementById('browseGalleryFromMoodboard');

  // Concept Generator
  const generateConceptBtn = document.getElementById('generateConceptBtn');
  const schoolNameInput = document.getElementById('schoolNameInput');
  const themeFocusSelect = document.getElementById('themeFocusSelect');
  const genResultsArea = document.getElementById('genResultsArea');

  // 1. Load Master Dataset (Supports direct file:// opening and HTTP fetch)
  if (window.STEAM_ITEMS_DATA && Array.isArray(window.STEAM_ITEMS_DATA) && window.STEAM_ITEMS_DATA.length > 0) {
    allCatalog = window.STEAM_ITEMS_DATA;
    console.log(`Loaded ${allCatalog.length} STEAM items directly from bundle.`);
  } else {
    try {
      const response = await fetch('data/steam_items.json');
      allCatalog = await response.json();
      console.log(`Loaded ${allCatalog.length} STEAM items from fetch.`);
    } catch (error) {
      console.error('Failed to load steam_items.json:', error);
      itemsGrid.innerHTML = `<div class="empty-state"><h3>Failed to load database. Please check that data/steam_items.json exists.</h3></div>`;
      return;
    }
  }

  // Update Initial Counters
  updateCounters();

  // 2. Initialize Theme
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('steam_theme_v1') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('steam_theme_v1', next);
      showToast(`Switched to ${next === 'dark' ? 'Cosmic Dark' : 'Clean Light'} mode`);
    });
  }

  // 3. Navigation Tab Switching
  navTabs.forEach(tabBtn => {
    tabBtn.addEventListener('click', () => {
      const targetTab = tabBtn.dataset.tab;
      switchTab(targetTab);
    });
  });

  function switchTab(tabName) {
    currentTab = tabName;
    navTabs.forEach(t => t.classList.toggle('active', t.dataset.tab === tabName));

    if (tabName === 'moodboard') {
      galleryView.style.display = 'none';
      moodboardView.style.display = 'block';
      generatorView.style.display = 'none';
      if (guideView) guideView.style.display = 'none';
      renderMoodboard();
    } else if (tabName === 'generator') {
      galleryView.style.display = 'none';
      moodboardView.style.display = 'none';
      generatorView.style.display = 'block';
      if (guideView) guideView.style.display = 'none';
      runConceptGenerator();
    } else if (tabName === 'guide') {
      galleryView.style.display = 'none';
      moodboardView.style.display = 'none';
      generatorView.style.display = 'none';
      if (guideView) guideView.style.display = 'block';
    } else {
      // 'all', 'logos', 'artwork'
      galleryView.style.display = 'block';
      moodboardView.style.display = 'none';
      generatorView.style.display = 'none';
      if (guideView) guideView.style.display = 'none';
      renderGallery();
    }
  }

  browseGalleryFromMoodboard.addEventListener('click', () => {
    switchTab('all');
  });

  // 4. Search and Filter Event Listeners
  searchInput.addEventListener('input', (e) => {
    currentSearch = e.target.value.trim().toLowerCase();
    renderGallery();
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    currentSearch = '';
    renderGallery();
  });

  gradeFilter.addEventListener('click', (e) => {
    if (e.target.classList.contains('pill-btn')) {
      gradeFilter.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentGrade = e.target.dataset.grade;
      renderGallery();
    }
  });

  sortSelect.addEventListener('change', (e) => {
    currentSort = e.target.value;
    renderGallery();
  });

  categoryPills.addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-pill');
    if (btn) {
      categoryPills.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      renderGallery();
    }
  });

  resetFiltersBtn.addEventListener('click', resetAllFilters);
  resetFromEmptyBtn.addEventListener('click', resetAllFilters);

  function resetAllFilters() {
    currentSearch = '';
    currentCategory = 'all';
    currentGrade = 'all';
    currentSort = 'featured';
    
    searchInput.value = '';
    sortSelect.value = 'featured';
    
    gradeFilter.querySelectorAll('.pill-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.grade === 'all');
    });
    
    categoryPills.querySelectorAll('.cat-pill').forEach(b => {
      b.classList.toggle('active', b.dataset.category === 'all');
    });

    renderGallery();
    showToast('Filters reset to default');
  }

  // 5. Core Filtering & Sorting Engine
  function getFilteredItems() {
    return allCatalog.filter(item => {
      // Type Tab check
      if (currentTab === 'logos' && item.type !== 'logo') return false;
      if (currentTab === 'artwork' && item.type !== 'artwork') return false;

      // Category check
      if (currentCategory !== 'all' && item.category !== currentCategory) return false;

      // Grade check
      if (currentGrade !== 'all' && item.grade_appeal !== currentGrade && item.grade_appeal !== 'K-5') return false;

      // Search Query check
      if (currentSearch) {
        const query = currentSearch;
        const inTitle = (item.title || '').toLowerCase().includes(query);
        const inCategory = (item.category || '').toLowerCase().includes(query);
        const inAwe = (item.awe_factor || '').toLowerCase().includes(query);
        const inTakeaways = (item.design_takeaways || '').toLowerCase().includes(query);
        const inMotifs = (item.key_motifs || []).some(m => m.toLowerCase().includes(query));
        const inColors = (item.color_palette || []).some(c => c.toLowerCase().includes(query));
        const inSource = (item.source_name || '').toLowerCase().includes(query);

        if (!inTitle && !inCategory && !inAwe && !inTakeaways && !inMotifs && !inColors && !inSource) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => {
      if (currentSort === 'name-asc') {
        return a.title.localeCompare(b.title);
      } else if (currentSort === 'category') {
        return a.category.localeCompare(b.category);
      } else if (currentSort === 'grade') {
        return a.grade_appeal.localeCompare(b.grade_appeal);
      }
      return 0; // featured / natural order
    });
  }

  // 6. Gallery Rendering
  function renderGallery() {
    const items = getFilteredItems();
    visibleCountEl.textContent = items.length;
    renderActiveFilterChips();

    if (items.length === 0) {
      itemsGrid.innerHTML = '';
      emptyState.style.display = 'block';
      return;
    }

    emptyState.style.display = 'none';
    itemsGrid.innerHTML = items.map(item => createCardHTML(item)).join('');

    // Attach card listeners
    attachCardListeners(itemsGrid);
  }

  function createCardHTML(item) {
    const isSaved = window.moodboardManager.isSaved(item.id);
    const isArt = item.type === 'artwork';

    return `
      <article class="steam-card ${isArt ? 'is-artwork' : 'is-logo'}" data-id="${item.id}">
        <div class="card-media-wrapper" data-action="open-modal">
          <img class="card-img" src="${item.image_url}" alt="${item.title}" loading="lazy">
          <span class="card-type-tag">${item.type === 'logo' ? '🏷️ Logo' : '🎨 Artwork'}</span>
          <button class="card-heart-btn ${isSaved ? 'is-saved' : ''}" data-action="toggle-heart" title="${isSaved ? 'Remove from Shortlist' : 'Add to Shortlist'}">
            ${isSaved ? '⭐' : '🤍'}
          </button>
        </div>

        <div class="card-content">
          <span class="card-category">${item.category}</span>
          <h3 class="card-title" data-action="open-modal">${item.title}</h3>
          <p class="card-awe-preview">${item.awe_factor}</p>

          <div class="card-palette-row" title="Click color to copy hex">
            ${(item.color_palette || []).slice(0, 5).map(hex => `
              <span class="palette-dot" style="background-color: ${hex};" data-hex="${hex}" title="Copy ${hex}"></span>
            `).join('')}
          </div>

          <div class="card-footer-meta">
            <span class="grade-badge-sm">Grades ${item.grade_appeal}</span>
            <span class="source-credit">${item.source_name ? item.source_name.slice(0, 22) : 'STEAM Lab'}</span>
          </div>
        </div>
      </article>
    `;
  }

  function attachCardListeners(container) {
    container.querySelectorAll('.steam-card').forEach(card => {
      const id = card.dataset.id;
      const item = allCatalog.find(i => i.id === id);
      if (!item) return;

      // Heart / Shortlist button
      const heartBtn = card.querySelector('[data-action="toggle-heart"]');
      if (heartBtn) {
        heartBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          const saved = window.moodboardManager.toggleSave(item);
          heartBtn.classList.toggle('is-saved', saved);
          heartBtn.textContent = saved ? '⭐' : '🤍';
          updateCounters();
          showToast(saved ? `Added "${item.title}" to Shortlist ⭐` : `Removed "${item.title}" from Shortlist`);
          if (currentTab === 'moodboard') {
            renderMoodboard();
          }
        });
      }

      // Card Click -> Lightbox Modal
      card.querySelectorAll('[data-action="open-modal"]').forEach(el => {
        el.addEventListener('click', () => {
          openItemModal(item);
        });
      });

      // Palette Dots Copy
      card.querySelectorAll('.palette-dot').forEach(dot => {
        dot.addEventListener('click', (e) => {
          e.stopPropagation();
          const hex = dot.dataset.hex;
          copyToClipboard(hex, `Copied color ${hex} to clipboard! 🎨`);
        });
      });
    });
  }

  function renderActiveFilterChips() {
    const chips = [];
    if (currentSearch) chips.push(`Search: "${currentSearch}"`);
    if (currentCategory !== 'all') chips.push(`Category: ${currentCategory}`);
    if (currentGrade !== 'all') chips.push(`Grade: ${currentGrade}`);

    activeChipsEl.innerHTML = chips.map(c => `
      <span class="tag-chip" style="background: var(--bg-surface-elevated); color: var(--color-cyan);">${c}</span>
    `).join('');
  }

  // 7. Lightbox Modal
  function openItemModal(item) {
    activeModalItem = item;
    const isSaved = window.moodboardManager.isSaved(item.id);

    modalImg.src = item.image_url;
    modalImg.alt = item.title;
    
    modalTypeBadge.textContent = item.type === 'logo' ? '🏷️ STEAM Logo / Badge' : '🎨 STEAM Artwork / Mural';
    modalGradeBadge.textContent = `Grades: ${item.grade_appeal}`;
    modalCategoryBadge.textContent = item.category;
    modalTitle.textContent = item.title;
    modalAweFactor.textContent = item.awe_factor;
    modalTakeaways.textContent = item.design_takeaways;
    
    // Motifs
    modalMotifsList.innerHTML = (item.key_motifs || []).map(m => `
      <span class="tag-chip">#${m}</span>
    `).join('');

    // Palette Swatches
    modalPaletteSwatches.innerHTML = (item.color_palette || []).map(hex => `
      <button class="swatch-btn" data-hex="${hex}">
        <span class="swatch-color-box" style="background-color: ${hex};"></span>
        <span class="swatch-hex-label">${hex}</span>
      </button>
    `).join('');

    modalPaletteSwatches.querySelectorAll('.swatch-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const hex = btn.dataset.hex;
        copyToClipboard(hex, `Copied ${hex} to clipboard!`);
      });
    });

    // Notes
    modalUserNotes.value = window.moodboardManager.getNotes(item.id);
    modalUserNotes.oninput = () => {
      window.moodboardManager.saveNotes(item.id, modalUserNotes.value);
    };

    // Shortlist Button in Modal
    updateModalShortlistBtn(isSaved);
    modalShortlistBtn.onclick = () => {
      const saved = window.moodboardManager.toggleSave(item);
      updateModalShortlistBtn(saved);
      updateCounters();
      renderGallery();
      showToast(saved ? `Added to Shortlist ⭐` : `Removed from Shortlist`);
    };

    // Source link
    modalSourceLink.href = item.source_url || '#';
    modalSourceLink.textContent = `🔗 View on ${item.source_name || 'Web'}`;

    itemModal.classList.add('is-active');
    document.body.style.overflow = 'hidden';
  }

  function updateModalShortlistBtn(isSaved) {
    modalShortlistLabel.textContent = isSaved ? 'Shortlisted ⭐' : 'Save to Moodboard';
    modalShortlistBtn.classList.toggle('btn-accent', isSaved);
    modalShortlistBtn.classList.toggle('btn-secondary', !isSaved);
  }

  modalCloseBtn.addEventListener('click', closeModal);
  itemModal.addEventListener('click', (e) => {
    if (e.target === itemModal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
      closeExportModal();
    }
  });

  function closeModal() {
    itemModal.classList.remove('is-active');
    document.body.style.overflow = '';
  }

  // 8. Moodboard Rendering
  function renderMoodboard() {
    const savedItems = window.moodboardManager.getSavedItems(allCatalog);
    
    if (savedItems.length === 0) {
      moodboardSummaryCard.style.display = 'none';
      moodboardGrid.innerHTML = '';
      moodboardEmptyState.style.display = 'block';
      return;
    }

    moodboardEmptyState.style.display = 'none';
    moodboardSummaryCard.style.display = 'grid';

    // Summary Card Stats
    const totalLogos = savedItems.filter(i => i.type === 'logo').length;
    const totalArt = savedItems.filter(i => i.type === 'artwork').length;
    const topCategories = [...new Set(savedItems.map(i => i.category))].slice(0, 3);
    const combinedColors = [...new Set(savedItems.flatMap(i => i.color_palette || []))].slice(0, 6);

    moodboardSummaryCard.innerHTML = `
      <div>
        <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Shortlist Size</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-cyan);">${savedItems.length} Items</div>
        <div style="font-size: 0.85rem; color: var(--text-secondary);">${totalLogos} Logos • ${totalArt} Artworks</div>
      </div>
      <div>
        <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Top Themes</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-top: 4px;">
          ${topCategories.join(', ') || 'Various'}
        </div>
      </div>
      <div>
        <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">Palette Swatches</div>
        <div style="display: flex; gap: 6px;">
          ${combinedColors.map(c => `<span style="width: 22px; height: 22px; border-radius: 4px; background-color: ${c}; border: 1px solid rgba(255,255,255,0.2);" title="${c}"></span>`).join('')}
        </div>
      </div>
    `;

    moodboardGrid.innerHTML = savedItems.map(item => createCardHTML(item)).join('');
    attachCardListeners(moodboardGrid);
  }

  clearMoodboardBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear your saved shortlist?')) {
      window.moodboardManager.clearAll();
      updateCounters();
      renderMoodboard();
      renderGallery();
      showToast('Shortlist cleared');
    }
  });

  // 9. Export Brief Modal
  exportBriefBtn.addEventListener('click', () => {
    const savedItems = window.moodboardManager.getSavedItems(allCatalog);
    if (savedItems.length === 0) {
      showToast('Please add items to your shortlist first!');
      return;
    }

    const schoolName = schoolNameInput.value.trim() || 'Elementary STEAM Lab';
    exportContentArea.innerHTML = window.moodboardManager.generateHTMLBrief(savedItems, schoolName);
    exportModal.classList.add('is-active');
    document.body.style.overflow = 'hidden';
  });

  exportModalCloseBtn.addEventListener('click', closeExportModal);
  exportModal.addEventListener('click', (e) => {
    if (e.target === exportModal) closeExportModal();
  });

  function closeExportModal() {
    exportModal.classList.remove('is-active');
    document.body.style.overflow = '';
  }

  printReportBtn.addEventListener('click', () => {
    window.print();
  });

  copyMarkdownBtn.addEventListener('click', () => {
    const savedItems = window.moodboardManager.getSavedItems(allCatalog);
    const schoolName = schoolNameInput.value.trim() || 'Elementary STEAM Lab';
    const md = window.moodboardManager.generateMarkdownBrief(savedItems, schoolName);
    copyToClipboard(md, 'Design Brief Markdown copied to clipboard! 📋');
  });

  downloadJsonBtn.addEventListener('click', () => {
    const savedItems = window.moodboardManager.getSavedItems(allCatalog);
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(savedItems, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", "steam_lab_moodboard.json");
    dlAnchor.click();
    showToast('Downloaded moodboard JSON brief 💾');
  });

  // 10. Concept & Slogan Generator Logic
  generateConceptBtn.addEventListener('click', runConceptGenerator);

  function runConceptGenerator() {
    const name = schoolNameInput.value.trim() || 'Our Elementary STEAM Lab';
    const theme = themeFocusSelect.value;

    const concepts = {
      cosmic: [
        {
          motto: "Where Curiosity Launches Beyond the Stars",
          zones: ["The Starlight Observatory (Robotics)", "Nebula Tinkering Bay", "Astro-Code Launchpad", "Deep Space Bio-Dome"],
          mascot: "Nova the Cosmic Otter / AstroBot Explorer",
          logoIdea: "A glowing retro-refractor telescope emitting a rainbow spectrum rocket into an interlocking gear constellation."
        },
        {
          motto: "Discovering New Worlds, One Invention at a Time",
          zones: ["Apollo Design Studio", "Orbit Maker Core", "Gravitational Physics Arena", "Planetary Art Matrix"],
          mascot: "Pulsar the Red Fox Explorer with fiber-optic tail",
          logoIdea: "A golden record badge with child handprints forming planetary solar rings."
        }
      ],
      tinkering: [
        {
          motto: "Think It. Make It. Glow With It.",
          zones: ["The Curious Cog Workshop", "Kinetic Marble Arena", "Edison Spark Lab", "Cardboard Castle Fab"],
          mascot: "Gizmo the Tinkering Raccoon / Archimedes the Owl",
          logoIdea: "A lightbulb sprouting oak tree roots made of bronze gears and circuit traces."
        },
        {
          motto: "Where Every Mistake is a New Discovery",
          zones: ["Rapid Prototyping Alley", "The Automata Bench", "Circuit Sparks Station", "Invention Testing Tank"],
          mascot: "Byte the Friendly Heart-Eyed Robot",
          logoIdea: "Interlocking primary color gears that create a glowing Eureka plasma spark."
        }
      ],
      nature: [
        {
          motto: "Nature's Genius, Tomorrow's Inventions",
          zones: ["The Honeycomb Makerspace", "Chlorophyll Code Greenhouse", "Nanotech Biomimicry Bay", "Tidal Energy Tank"],
          mascot: "Galileo the Nanofiber Gecko / RoboBee Pollinator",
          logoIdea: "A monarch butterfly with one organic vein wing and one glowing emerald PCB circuit wing."
        }
      ],
      future: [
        {
          motto: "Building Tomorrow's Dreams Today",
          zones: ["The Micro-Bot Arena", "3D Hologram Design Den", "Cyber-Craft Foundry", "AI & Algorithmic Studio"],
          mascot: "Pip the Pixel-Tread Robot / Quantum Quokka",
          logoIdea: "An impossible 3D Necker cube with laser cutouts of gears, atoms, and paintbrushes."
        }
      ],
      creative: [
        {
          motto: "Where Art Meets Algorithm",
          zones: ["The Prismatic Color Lab", "Origami Engineering Deck", "Spirograph Harmonic Lounge", "Pixel-to-Paint Studio"],
          mascot: "Cosmic Chameleon with Fibonacci Spiral Tail",
          logoIdea: "A continuous 3D rainbow ribbon forming S-T-E-A-M over an optical prism."
        }
      ]
    };

    const selectedSet = concepts[theme] || concepts.cosmic;
    
    genResultsArea.innerHTML = selectedSet.map(c => `
      <div class="concept-result-card">
        <div class="concept-motto">✨ "${c.motto}"</div>
        <p style="font-size: 0.95rem; color: var(--text-primary); margin-bottom: 0.75rem;">
          <strong>Concept Identity for:</strong> ${name}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
          <strong>Recommended Lab Zones:</strong> ${c.zones.join(' • ')}
        </p>
        <p style="font-size: 0.9rem; color: var(--color-cyan); margin-bottom: 0.75rem;">
          <strong>Suggested Mascot:</strong> ${c.mascot}
        </p>
        <div style="background: var(--bg-main); padding: 0.85rem; border-radius: 8px; font-size: 0.88rem; color: var(--text-muted); border-left: 3px solid var(--color-cyan);">
          <strong>🎨 Logo Design Prompt Idea:</strong> ${c.logoIdea}
        </div>
      </div>
    `).join('');
  }

  // 11. Helper Functions
  function updateCounters() {
    countAll.textContent = allCatalog.length;
    countLogos.textContent = allCatalog.filter(i => i.type === 'logo').length;
    countArt.textContent = allCatalog.filter(i => i.type === 'artwork').length;
    countMoodboard.textContent = window.moodboardManager.getSavedIds().length;
  }

  function copyToClipboard(text, successMsg) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(successMsg);
      }).catch(() => {
        fallbackCopy(text, successMsg);
      });
    } else {
      fallbackCopy(text, successMsg);
    }
  }

  function fallbackCopy(text, successMsg) {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast(successMsg);
  }

  function showToast(msg) {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.innerHTML = msg;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 3000);
  }

  // Initial Gallery Render
  renderGallery();
});
